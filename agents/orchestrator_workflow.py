"""
Workflow-Enhanced Orchestrator

Extends the base Orchestrator with workflow template support.
Automatically matches tasks to workflows and executes them with full tracking.
"""
import asyncio
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add system path for workflow imports
sys.path.insert(0, str(Path(__file__).parent.parent / "system"))

from .orchestrator import Orchestrator
from system.workflow_executor import WorkflowExecutor
from system.workflow_history import WorkflowHistory
from system.workflow_learning import WorkflowLearner


class WorkflowOrchestrator(Orchestrator):
    """
    Enhanced orchestrator with workflow template support.

    Automatically detects when a task matches a workflow template
    and executes the workflow instead of manual agent selection.
    """

    def __init__(
        self,
        workspace_dir: str = "workspace",
        registry_path: str = "agents/registry.json",
        skills_path: str = "agents/skills_history.json",
        max_parallel_agents: int = 5,
        enable_workflows: bool = True,
        workflow_match_threshold: int = 5  # Minimum score to use workflow
    ):
        # Initialize base orchestrator
        super().__init__(
            workspace_dir=workspace_dir,
            registry_path=registry_path,
            skills_path=skills_path,
            max_parallel_agents=max_parallel_agents
        )

        # Initialize workflow components
        self.enable_workflows = enable_workflows
        self.workflow_match_threshold = workflow_match_threshold

        if self.enable_workflows:
            self.workflow_executor = WorkflowExecutor()
            self.workflow_history = WorkflowHistory()
            self.workflow_learner = WorkflowLearner()

            print("✅ Workflow system enabled")

    async def execute_task(
        self,
        task_description: str,
        context: Optional[Dict[str, Any]] = None,
        max_agents: int = 3,
        use_tmux: bool = True,
        force_workflow: Optional[str] = None,
        skip_workflow: bool = False
    ) -> Dict[str, Any]:
        """
        Execute a task with workflow support.

        Args:
            task_description: Natural language description of the task
            context: Optional context (files, constraints, etc.)
            max_agents: Maximum number of agents to use (if not using workflow)
            use_tmux: Whether to use TMUX sessions for agents
            force_workflow: Force use of specific workflow (by name)
            skip_workflow: Skip workflow matching and use agent selection

        Returns:
            Dictionary with execution results
        """
        # Check if workflows are enabled and should be used
        if self.enable_workflows and not skip_workflow:
            # Try to match workflow
            workflow_match = None

            if force_workflow:
                # Use specified workflow
                print(f"\n🔄 Using forced workflow: {force_workflow}")
                workflow_match = {'workflow': {'name': force_workflow}, 'score': 100, 'relevance': 'forced'}

            else:
                # Find matching workflows
                matches = self.workflow_executor.match_workflow(task_description, top_n=1)

                if matches and matches[0]['score'] >= self.workflow_match_threshold:
                    workflow_match = matches[0]

            # Execute with workflow if matched
            if workflow_match:
                return await self._execute_with_workflow(
                    workflow_name=workflow_match['workflow']['name'],
                    task_description=task_description,
                    context=context,
                    use_tmux=use_tmux
                )
            else:
                print(f"ℹ️  No matching workflow found (threshold: {self.workflow_match_threshold})")
                print(f"   Falling back to agent selection\n")

        # Fall back to standard agent selection
        return await super().execute_task(
            task_description=task_description,
            context=context,
            max_agents=max_agents,
            use_tmux=use_tmux
        )

    async def _execute_with_workflow(
        self,
        workflow_name: str,
        task_description: str,
        context: Optional[Dict[str, Any]],
        use_tmux: bool
    ) -> Dict[str, Any]:
        """
        Execute a task using a workflow template.

        Args:
            workflow_name: Name of workflow to execute
            task_description: Task description
            context: Optional context
            use_tmux: Whether to use TMUX

        Returns:
            Execution results
        """
        print(f"\n{'='*80}")
        print(f"🔄 WORKFLOW EXECUTION MODE")
        print(f"{'='*80}")
        print(f"📋 Task: {task_description}")
        print(f"🔄 Workflow: {workflow_name}")
        print(f"{'='*80}\n")

        # Load workflow
        workflow = self.workflow_executor.workflow_manager.show_workflow(workflow_name)

        if not workflow:
            print(f"❌ Workflow '{workflow_name}' not found")
            print(f"   Falling back to agent selection\n")

            return await super().execute_task(
                task_description=task_description,
                context=context,
                max_agents=3,
                use_tmux=use_tmux
            )

        # Show workflow info
        print(f"📝 Description: {workflow.get('description', 'N/A')}")
        print(f"👥 Required Agents: {', '.join(workflow.get('agents_required', []))}")
        print(f"📋 Steps: {len(workflow.get('steps', []))}")
        print(f"⏱️  Est. Duration: {self._format_duration(workflow.get('estimated_duration', 0))}\n")

        # Start tracking
        exec_id = self.workflow_history.start_execution(
            workflow_name=workflow['name'],
            workflow_version=workflow.get('version', '1.0.0'),
            task_description=task_description,
            project_path=context.get('project_path') if context else None
        )

        # Execute workflow steps
        steps = workflow.get('steps', [])
        completed_steps = 0
        failed_steps = 0
        results = {'outputs': [], 'step_results': []}

        for i, step in enumerate(steps, 1):
            step_id = step['id']
            step_name = step['name']
            agent_name = step['agent']
            required = step.get('required', True)

            print(f"{'─'*80}")
            print(f"📍 Step {i}/{len(steps)}: {step_name}")
            print(f"   Agent: {agent_name} | Required: {'Yes' if required else 'No'}")

            # Check if we should skip optional steps
            if not required and context and context.get('skip_optional_steps'):
                print(f"   ⏩ Skipping optional step")
                self.workflow_history.skip_step(exec_id, step_id, "Optional step skipped by user")
                continue

            # Start step tracking
            self.workflow_history.start_step(exec_id, step_id, step_name, agent_name)

            # Get agent
            agent = self.registry.get_agent(agent_name)

            if not agent:
                print(f"   ❌ Agent '{agent_name}' not found in registry")
                self.workflow_history.fail_step(exec_id, step_id, f"Agent '{agent_name}' not found")
                failed_steps += 1

                if required:
                    print(f"   ⛔ Required step failed. Stopping workflow.")
                    break
                continue

            # Execute step with agent
            try:
                step_result = await self._execute_single_agent(
                    task_id=exec_id,
                    agent=agent,
                    task_description=step.get('action', task_description),
                    context=context,
                    use_tmux=use_tmux
                )

                if step_result.get('success'):
                    # Record success
                    outputs = step.get('outputs', [])
                    self.workflow_history.complete_step(
                        exec_id, step_id,
                        outputs=outputs,
                        validation_passed=True
                    )

                    results['step_results'].append(step_result)
                    results['outputs'].extend(outputs)

                    completed_steps += 1
                    print(f"   ✅ Step completed successfully")

                else:
                    # Record failure
                    error = step_result.get('error', 'Unknown error')
                    self.workflow_history.fail_step(exec_id, step_id, error)
                    failed_steps += 1
                    print(f"   ❌ Step failed: {error}")

                    if required:
                        print(f"   ⛔ Required step failed. Stopping workflow.")
                        break

            except Exception as e:
                self.workflow_history.fail_step(exec_id, step_id, str(e))
                failed_steps += 1
                print(f"   ❌ Step failed with exception: {e}")

                if required:
                    print(f"   ⛔ Required step failed. Stopping workflow.")
                    break

        # Complete workflow execution
        success = failed_steps == 0 or (completed_steps > 0 and failed_steps < len(steps))
        self.workflow_history.complete_execution(exec_id, success=success)

        # Print summary
        print(f"\n{'='*80}")
        print(f"📊 WORKFLOW EXECUTION SUMMARY")
        print(f"{'='*80}")
        print(f"Status: {'✅ Success' if success else '❌ Failed'}")
        print(f"Steps Completed: {completed_steps}/{len(steps)}")
        print(f"Steps Failed: {failed_steps}")
        print(f"Outputs Generated: {len(results['outputs'])}")
        print(f"{'='*80}\n")

        return {
            'task_id': exec_id,
            'success': success,
            'workflow_name': workflow_name,
            'execution_mode': 'workflow',
            'completed_steps': completed_steps,
            'failed_steps': failed_steps,
            'total_steps': len(steps),
            'outputs': results['outputs'],
            'results': results
        }

    def get_workflow_statistics(self) -> Dict[str, Any]:
        """Get workflow system statistics."""
        if not self.enable_workflows:
            return {'error': 'Workflows not enabled'}

        return self.workflow_history.get_global_statistics()

    def analyze_workflow_performance(self, workflow_name: str) -> Dict[str, Any]:
        """Analyze performance of a specific workflow."""
        if not self.enable_workflows:
            return {'error': 'Workflows not enabled'}

        return self.workflow_learner.analyze_workflow(workflow_name)

    def detect_workflow_patterns(self, min_occurrences: int = 3) -> List[Dict[str, Any]]:
        """Detect repeated task patterns that could become workflows."""
        if not self.enable_workflows:
            return []

        return self.workflow_learner.detect_task_patterns(min_occurrences=min_occurrences)

    def export_learning_report(self, output_path: str = "workflows/LEARNING_REPORT.md") -> str:
        """Export workflow learning report."""
        if not self.enable_workflows:
            return ""

        return self.workflow_learner.export_learning_report(output_path=output_path)

    def _format_duration(self, seconds: float) -> str:
        """Format duration in seconds to human-readable string."""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = seconds % 60
            return f"{minutes}m {secs:.0f}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"

    def _print_analysis(self, analysis):
        """Override to add workflow info."""
        super()._print_analysis(analysis)

        if self.enable_workflows:
            # Show matching workflows
            matches = self.workflow_executor.match_workflow(
                analysis.task_description if hasattr(analysis, 'task_description') else "",
                top_n=3
            )

            if matches:
                print(f"\n💡 Matching Workflows ({len(matches)}):")
                for match in matches:
                    workflow = match['workflow']
                    relevance_icon = {'high': '🟢', 'medium': '🟡', 'low': '🔴'}.get(match['relevance'], '⚪')
                    print(f"   {relevance_icon} {workflow['name']} (Score: {match['score']}, Relevance: {match['relevance']})")


# Backwards compatibility alias
OrchestratorWorkflow = WorkflowOrchestrator
