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

# Import project management
import importlib.util
_project_cli_path = Path(__file__).parent.parent / "system" / "project-cli.py"
_spec = importlib.util.spec_from_file_location("project_cli", _project_cli_path)
_project_cli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_project_cli)
ProjectManager = _project_cli.ProjectManager


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
        workflow_match_threshold: int = 5,  # Minimum score to use workflow
        execution_mode: str = "independent"  # "independent" or "interactive"
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
        self.execution_mode = execution_mode

        if self.enable_workflows:
            self.workflow_executor = WorkflowExecutor()
            self.workflow_history = WorkflowHistory()
            self.workflow_learner = WorkflowLearner()
            self.project_manager = ProjectManager()

            mode_emoji = "🤖" if execution_mode == "independent" else "👤"
            print(f"✅ Workflow system enabled ({mode_emoji} {execution_mode} mode)")

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
                # Find matching workflows using keyword scoring
                matches = self.workflow_executor.match_workflow(task_description, top_n=1)

                if matches and matches[0]['score'] >= self.workflow_match_threshold:
                    workflow_match = matches[0]
                else:
                    # No keyword match - use intelligent analysis
                    print(f"ℹ️  No keyword match found (threshold: {self.workflow_match_threshold})")
                    print(f"🧠 Analyzing task to determine best workflow...\n")
                    workflow_match = await self._intelligent_workflow_selection(task_description)

            # Execute with workflow if matched
            if workflow_match:
                return await self._execute_with_workflow(
                    workflow_name=workflow_match['workflow']['name'],
                    task_description=task_description,
                    context=context,
                    use_tmux=use_tmux
                )
            else:
                print(f"ℹ️  No suitable workflow found")
                print(f"   Using direct agent selection\n")

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

        # Present plan and ask for approval in interactive mode
        if not self._present_plan({'workflow': workflow}):
            return {
                'task_id': 'rejected',
                'success': False,
                'error': 'User rejected execution plan',
                'execution_mode': 'workflow'
            }

        # Start tracking
        exec_id = self.workflow_history.start_execution(
            workflow_name=workflow['name'],
            workflow_version=workflow.get('version', '1.0.0'),
            task_description=task_description,
            project_path=context.get('project_path') if context else None
        )

        # Handle project setup if project context provided
        project_workspace = None
        if context and context.get('project_name'):
            project_name = context['project_name']

            # Check if project exists, create if needed
            project_info = self.project_manager.get_project_info(project_name)
            if not project_info:
                print(f"📁 Creating new project: {project_name}")
                self.project_manager.create_project(
                    name=project_name,
                    template="web-app",
                    init_git=True
                )
                print(f"   ✅ Project created at: projects/{project_name}/\n")
            else:
                print(f"📁 Using existing project: {project_name}\n")

            # Set workspace to project directory
            project_workspace = Path(self.workspace_dir).parent / "projects" / project_name

        # Execute workflow steps
        steps = workflow.get('steps', [])
        completed_steps = 0
        failed_steps = 0
        results = {'outputs': [], 'step_results': []}

        # Track iteration count per step to prevent infinite loops
        step_iterations = {}

        for i, step in enumerate(steps, 1):
            step_id = step['id']
            step_name = step['name']
            agent_name = step['agent']
            required = step.get('required', True)
            max_retries = step.get('max_retries', 0)  # Default: no retries

            # Initialize iteration counter
            if step_id not in step_iterations:
                step_iterations[step_id] = 0

            print(f"{'─'*80}")
            print(f"📍 Step {i}/{len(steps)}: {step_name}")
            print(f"   Agent: {agent_name} | Required: {'Yes' if required else 'No'}")
            if max_retries > 0:
                print(f"   Max Retries: {max_retries} | Current Iteration: {step_iterations[step_id] + 1}")

            # Check if we should skip optional steps
            if not required and context and context.get('skip_optional_steps'):
                print(f"   ⏩ Skipping optional step")
                self.workflow_history.skip_step(exec_id, step_id, "Optional step skipped by user")
                continue

            # Ask for step approval in interactive mode
            step_approval = self._ask_step_approval(step, i, len(steps))
            if step_approval is None:  # User chose to skip
                print(f"   ⏩ Skipping step (user request)")
                self.workflow_history.skip_step(exec_id, step_id, "Skipped by user in interactive mode")
                continue
            elif step_approval is False:  # User rejected
                print(f"   ❌ Step rejected by user")
                failed_steps += 1
                break

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

            # Retry loop for this step
            step_success = False
            step_validation_passed = False
            last_error = None

            while step_iterations[step_id] <= max_retries:
                # Prepare context with previous iteration info
                step_context = context.copy() if context else {}

                # Add feedback from previous iteration
                if step_iterations[step_id] > 0:
                    print(f"\n   🔄 Retry attempt {step_iterations[step_id]}/{max_retries}")
                    step_context['retry_attempt'] = step_iterations[step_id]
                    step_context['previous_error'] = last_error

                    # If there's a QA report with bugs, pass it as context
                    if project_workspace and (project_workspace / 'QA_REPORT.md').exists():
                        qa_report = (project_workspace / 'QA_REPORT.md').read_text()
                        step_context['qa_feedback'] = qa_report
                        step_context['task_context'] = f"""
Previous iteration failed validation. QA Report:
---
{qa_report[:1000]}...

Please fix the issues mentioned above and regenerate the files.
"""

                # Execute step with agent
                try:
                    # Enhance task description with context on retries
                    enhanced_task = step.get('action', task_description)
                    if step_iterations[step_id] > 0 and step_context.get('task_context'):
                        enhanced_task = step_context['task_context'] + "\n\n" + enhanced_task

                    step_result = await self._execute_single_agent(
                        task_id=exec_id,
                        agent=agent,
                        task_description=enhanced_task,
                        context=step_context,
                        use_tmux=use_tmux
                    )

                    if step_result.get('success'):
                        # Validate outputs
                        outputs = step.get('outputs', [])
                        created_files = step_result.get('files_created', [])

                        # Run validation if rules exist
                        validation = step.get('validation', [])
                        if validation and project_workspace:
                            validation_result = self.workflow_executor._validate_step_outputs(
                                step, created_files, project_workspace
                            )
                            step_validation_passed = validation_result['passed']

                            if step_validation_passed:
                                print(f"   ✅ Step completed and validated successfully")
                            else:
                                print(f"   ⚠️  Step completed but validation failed:")
                                for error in validation_result['errors']:
                                    print(f"      • {error}")
                                last_error = '; '.join(validation_result['errors'])
                        else:
                            # No validation rules, consider it passed
                            step_validation_passed = True
                            print(f"   ✅ Step completed successfully")

                        # If validation passed or no more retries, record success
                        if step_validation_passed:
                            self.workflow_history.complete_step(
                                exec_id, step_id,
                                outputs=outputs,
                                validation_passed=True
                            )
                            results['step_results'].append(step_result)
                            results['outputs'].extend(outputs)
                            completed_steps += 1
                            step_success = True
                            break  # Exit retry loop
                        else:
                            # Validation failed, will retry if attempts remaining
                            step_iterations[step_id] += 1
                            if step_iterations[step_id] > max_retries:
                                # No more retries
                                self.workflow_history.fail_step(
                                    exec_id, step_id,
                                    f"Validation failed after {max_retries + 1} attempts: {last_error}"
                                )
                                failed_steps += 1
                                break

                    else:
                        # Execution failed
                        error = step_result.get('error', 'Unknown error')
                        last_error = error
                        print(f"   ❌ Step execution failed: {error}")

                        step_iterations[step_id] += 1
                        if step_iterations[step_id] > max_retries:
                            # No more retries
                            self.workflow_history.fail_step(exec_id, step_id, error)
                            failed_steps += 1
                            break

                except Exception as e:
                    last_error = str(e)
                    print(f"   ❌ Step failed with exception: {e}")

                    step_iterations[step_id] += 1
                    if step_iterations[step_id] > max_retries:
                        # No more retries
                        self.workflow_history.fail_step(exec_id, step_id, str(e))
                        failed_steps += 1
                        break

            # Check if we should stop workflow due to failed required step
            if not step_success and required:
                print(f"   ⛔ Required step failed after {step_iterations[step_id]} attempts. Stopping workflow.")
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

    async def _intelligent_workflow_selection(self, task_description: str) -> Optional[Dict[str, Any]]:
        """
        Intelligently analyze task and select best workflow using semantic understanding.

        Args:
            task_description: The task to analyze

        Returns:
            Workflow match dictionary or None if no suitable workflow
        """
        # Get all available workflows
        all_workflows = self.workflow_executor.workflow_manager.list_workflows(detailed=True)

        if not all_workflows:
            return None

        # Create analysis prompt
        workflows_info = []
        for wf in all_workflows:
            workflows_info.append(
                f"- {wf['name']}: {wf.get('description', 'No description')}\n"
                f"  Typical tasks: {', '.join(wf.get('task_types', [])[:3])}"
            )

        workflows_text = "\n".join(workflows_info)

        # Use task router to analyze
        analysis = self.router.analyze_task(task_description)

        # Determine best workflow based on task characteristics
        task_lower = task_description.lower()

        # Pattern matching with semantic understanding
        if any(keyword in task_lower for keyword in ['build', 'create', 'develop', 'implement', 'make']):
            if any(keyword in task_lower for keyword in ['web', 'website', 'app', 'application', 'ui', 'interface', 'frontend', 'game', 'page']):
                print(f"   💡 Task involves building a web application")
                print(f"   ✓ Selected: web-app-development workflow\n")
                return {'workflow': {'name': 'web-app-development'}, 'score': 8, 'relevance': 'intelligent'}

            elif any(keyword in task_lower for keyword in ['api', 'endpoint', 'rest', 'graphql', 'service', 'backend']):
                print(f"   💡 Task involves API development")
                print(f"   ✓ Selected: api-development workflow\n")
                return {'workflow': {'name': 'api-development'}, 'score': 8, 'relevance': 'intelligent'}

        elif any(keyword in task_lower for keyword in ['test', 'qa', 'quality', 'verify', 'check', 'validate']):
            print(f"   💡 Task involves testing and quality assurance")
            print(f"   ✓ Selected: testing-suite workflow\n")
            return {'workflow': {'name': 'testing-suite'}, 'score': 8, 'relevance': 'intelligent'}

        elif any(keyword in task_lower for keyword in ['security', 'audit', 'vulnerability', 'penetration', 'secure']):
            print(f"   💡 Task involves security analysis")
            print(f"   ✓ Selected: security-audit workflow\n")
            return {'workflow': {'name': 'security-audit'}, 'score': 8, 'relevance': 'intelligent'}

        elif any(keyword in task_lower for keyword in ['document', 'docs', 'readme', 'guide', 'documentation']):
            print(f"   💡 Task involves documentation")
            print(f"   ✓ Selected: documentation workflow\n")
            return {'workflow': {'name': 'documentation'}, 'score': 8, 'relevance': 'intelligent'}

        # No suitable workflow found
        print(f"   ℹ️  Task doesn't clearly match any workflow pattern")
        return None

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

    # Interactive Mode Methods

    def _ask_clarification(self, question: str, options: List[str] = None) -> str:
        """Ask user for clarification in interactive mode."""
        if self.execution_mode != "interactive":
            return options[0] if options else ""

        print(f"\n❓ {question}")

        if options:
            for i, option in enumerate(options, 1):
                print(f"   {i}. {option}")

            while True:
                try:
                    choice = input("\n👤 Your choice (number or text): ").strip()

                    # Check if numeric choice
                    if choice.isdigit():
                        idx = int(choice) - 1
                        if 0 <= idx < len(options):
                            return options[idx]

                    # Check if text matches an option
                    for option in options:
                        if choice.lower() in option.lower():
                            return option

                    print("   ❌ Invalid choice. Please try again.")
                except KeyboardInterrupt:
                    print("\n   ⚠️  Using default option")
                    return options[0]
        else:
            return input("\n👤 Your answer: ").strip()

    def _present_plan(self, plan: Dict[str, Any]) -> bool:
        """Present execution plan and ask for approval in interactive mode."""
        if self.execution_mode == "independent":
            return True  # Auto-approve in independent mode

        print(f"\n{'='*80}")
        print("📋 EXECUTION PLAN")
        print(f"{'='*80}")

        # Show workflow if applicable
        if 'workflow' in plan:
            workflow = plan['workflow']
            print(f"Workflow: {workflow.get('name', 'N/A')}")
            print(f"Description: {workflow.get('description', 'N/A')}")
            print(f"Estimated Duration: {self._format_duration(workflow.get('estimated_duration', 0))}")
            print(f"\nSteps ({len(workflow.get('steps', []))}):")
            for i, step in enumerate(workflow.get('steps', []), 1):
                required = "✓ Required" if step.get('required') else "○ Optional"
                print(f"  {i}. {step.get('name')} ({step.get('agent')}) - {required}")

        # Show agents if no workflow
        elif 'agents' in plan:
            print("Agents to be used:")
            for agent in plan['agents']:
                print(f"  • {agent.get('name')}: {agent.get('description')}")

        print(f"{'='*80}")

        while True:
            response = input("\n👤 Approve this plan? (yes/no/modify): ").strip().lower()

            if response in ['y', 'yes']:
                print("   ✅ Plan approved!")
                return True
            elif response in ['n', 'no']:
                print("   ❌ Plan rejected. Exiting.")
                return False
            elif response in ['m', 'modify']:
                print("   💡 Modification not yet implemented. Proceeding with plan.")
                return True
            else:
                print("   ❌ Invalid input. Please answer yes, no, or modify.")

    def _ask_step_approval(self, step: Dict[str, Any], step_num: int, total_steps: int) -> bool:
        """Ask for approval before executing a step in interactive mode."""
        if self.execution_mode != "interactive":
            return True  # Auto-approve in independent mode

        print(f"\n{'─'*80}")
        print(f"📍 Step {step_num}/{total_steps}: {step.get('name')}")
        print(f"   Agent: {step.get('agent')}")
        print(f"   Action: {step.get('action', 'N/A')[:150]}...")
        print(f"{'─'*80}")

        while True:
            response = input("\n👤 Proceed with this step? (yes/no/skip): ").strip().lower()

            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                print("   ❌ Step rejected. Stopping workflow.")
                return False
            elif response in ['s', 'skip']:
                if not step.get('required', True):
                    print("   ⏩ Skipping optional step.")
                    return None  # None means skip
                else:
                    print("   ⚠️  Cannot skip required step.")
            else:
                print("   ❌ Invalid input. Please answer yes, no, or skip.")

    def _show_step_result(self, step: Dict[str, Any], result: Dict[str, Any]):
        """Show step result and ask for feedback in interactive mode."""
        if self.execution_mode != "interactive":
            return

        success = result.get('success', False)
        status_emoji = "✅" if success else "❌"

        print(f"\n{status_emoji} Step Result: {step.get('name')}")

        if success:
            files_created = result.get('files_created', [])
            if files_created:
                print(f"   📄 Files created: {', '.join(files_created)}")

            # Ask if user wants to review
            review = input("\n👤 Review output before continuing? (yes/no): ").strip().lower()
            if review in ['y', 'yes']:
                if result.get('output'):
                    print(f"\n{'─'*80}")
                    print(result['output'][:500])
                    print(f"{'─'*80}")
                    input("\nPress Enter to continue...")
        else:
            error = result.get('error', 'Unknown error')
            print(f"   ❌ Error: {error}")

            # Ask how to proceed
            response = input("\n👤 How to proceed? (retry/skip/abort): ").strip().lower()
            return response


# Backwards compatibility alias
OrchestratorWorkflow = WorkflowOrchestrator
