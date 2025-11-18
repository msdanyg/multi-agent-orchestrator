"""
Orchestrator Agent
Main coordinator for multi-agent task execution
"""
import asyncio
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .registry import AgentRegistry, AgentDefinition
from .task_router import TaskRouter, TaskAnalysis, AgentAssignment
from .tmux_manager import TmuxManager
from .skills_system import SkillsSystem, TaskOutcome
import subprocess
import json


class Orchestrator:
    """Central coordinator for multi-agent system"""

    def __init__(
        self,
        workspace_dir: str = "workspace",
        registry_path: str = "agents/registry.json",
        skills_path: str = "agents/skills_history.json",
        max_parallel_agents: int = 5
    ):
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

        # Paths
        self.base_dir = Path(__file__).parent.parent
        self.agents_instructions_dir = self.base_dir / ".claude" / "agents"

        # Initialize components
        self.registry = AgentRegistry(registry_path)
        self.router = TaskRouter(self.registry)
        self.tmux_manager = TmuxManager(workspace_dir)
        self.skills_system = SkillsSystem(skills_path)

        self.max_parallel_agents = max_parallel_agents
        self.active_tasks: Dict[str, Dict[str, Any]] = {}

        # Check tmux availability
        if not self.tmux_manager.check_tmux_installed():
            raise RuntimeError("TMUX is not installed. Please install tmux to use this framework.")

    async def execute_task(
        self,
        task_description: str,
        context: Optional[Dict[str, Any]] = None,
        max_agents: int = 3,
        use_tmux: bool = True
    ) -> Dict[str, Any]:
        """
        Execute a task using optimal agent selection and coordination

        Args:
            task_description: Natural language description of the task
            context: Optional context (files, constraints, etc.)
            max_agents: Maximum number of agents to use
            use_tmux: Whether to use TMUX sessions for agents

        Returns:
            Dictionary with execution results
        """
        task_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        print(f"\n{'='*80}")
        print(f"🎯 Task ID: {task_id}")
        print(f"📋 Task: {task_description}")
        print(f"{'='*80}\n")

        # Analyze task
        print("🔍 Analyzing task...")
        analysis = self.router.analyze_task(task_description)
        self._print_analysis(analysis)

        # Select agents
        print("\n🤖 Selecting agents...")
        assignments = self.router.select_agents(task_description, max_agents=max_agents)

        if not assignments:
            return {
                'task_id': task_id,
                'success': False,
                'error': 'No suitable agents found for this task',
                'execution_time': time.time() - start_time
            }

        self._print_assignments(assignments)

        # Execute with agents
        results = await self._execute_with_agents(
            task_id=task_id,
            task_description=task_description,
            analysis=analysis,
            assignments=assignments,
            context=context,
            use_tmux=use_tmux
        )

        execution_time = time.time() - start_time

        # Record outcomes
        self._record_outcomes(
            task_id=task_id,
            task_description=task_description,
            analysis=analysis,
            results=results,
            execution_time=execution_time
        )

        # Prepare final result
        final_result = {
            'task_id': task_id,
            'success': results.get('success', False),
            'execution_time': execution_time,
            'agents_used': [a.agent.name for a in assignments],
            'results': results,
            'analysis': {
                'task_type': analysis.task_type,
                'complexity': analysis.complexity,
                'capabilities_required': analysis.required_capabilities
            }
        }

        self._print_summary(final_result)

        return final_result

    async def _execute_with_agents(
        self,
        task_id: str,
        task_description: str,
        analysis: TaskAnalysis,
        assignments: List[AgentAssignment],
        context: Optional[Dict[str, Any]],
        use_tmux: bool
    ) -> Dict[str, Any]:
        """Execute task with assigned agents"""

        # Separate primary and supporting agents
        primary_agents = [a for a in assignments if a.priority == "primary"]
        supporting_agents = [a for a in assignments if a.priority in ["supporting", "optional"]]

        results = {
            'success': False,
            'primary_results': [],
            'supporting_results': [],
            'errors': []
        }

        # Execute primary agents (sequential for dependencies)
        print("\n🚀 Executing primary agents...")
        for assignment in primary_agents:
            agent_result = await self._execute_single_agent(
                task_id=task_id,
                agent=assignment.agent,
                task_description=task_description,
                context=context,
                use_tmux=use_tmux
            )
            results['primary_results'].append(agent_result)

            if not agent_result.get('success'):
                results['errors'].append(f"{assignment.agent.name}: {agent_result.get('error')}")

        # Execute supporting agents (can be parallel if task allows)
        if supporting_agents and analysis.can_parallelize:
            print("\n⚡ Executing supporting agents in parallel...")
            tasks = [
                self._execute_single_agent(
                    task_id=task_id,
                    agent=a.agent,
                    task_description=task_description,
                    context=context,
                    use_tmux=use_tmux
                )
                for a in supporting_agents
            ]
            supporting_results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in supporting_results:
                if isinstance(result, Exception):
                    results['errors'].append(str(result))
                else:
                    results['supporting_results'].append(result)

        elif supporting_agents:
            print("\n🔄 Executing supporting agents sequentially...")
            for assignment in supporting_agents:
                agent_result = await self._execute_single_agent(
                    task_id=task_id,
                    agent=assignment.agent,
                    task_description=task_description,
                    context=context,
                    use_tmux=use_tmux
                )
                results['supporting_results'].append(agent_result)

        # Determine overall success
        primary_success = all(r.get('success', False) for r in results['primary_results'])
        results['success'] = primary_success

        return results

    def _load_agent_instructions(self, agent_name: str) -> Optional[str]:
        """Load agent instructions from .claude/agents/ directory."""
        instruction_file = self.agents_instructions_dir / f"{agent_name}.md"

        if instruction_file.exists():
            return instruction_file.read_text()

        return None

    async def _execute_single_agent(
        self,
        task_id: str,
        agent: AgentDefinition,
        task_description: str,
        context: Optional[Dict[str, Any]],
        use_tmux: bool
    ) -> Dict[str, Any]:
        """Execute task with a single agent"""
        print(f"\n  → {agent.name}: {agent.description}")

        agent_start_time = time.time()

        # Create agent workspace
        # Check if context specifies a project workspace
        if context and context.get('project_path'):
            agent_workspace = Path(context['project_path'])
            agent_workspace.mkdir(parents=True, exist_ok=True)
        else:
            agent_workspace = self.workspace_dir / agent.name / task_id
            agent_workspace.mkdir(parents=True, exist_ok=True)

        # Generate specialized prompt
        prompt = self.router.generate_agent_prompt(agent, task_description, context)

        # Write prompt to workspace
        prompt_file = agent_workspace / "prompt.txt"
        prompt_file.write_text(prompt)

        result = {
            'agent': agent.name,
            'success': False,
            'execution_time': 0,
            'workspace': str(agent_workspace)
        }

        try:
            if use_tmux:
                # Execute in TMUX session
                session_id = self.tmux_manager.create_session(
                    agent_name=agent.name,
                    task_id=task_id,
                    working_dir=str(agent_workspace)
                )

                result['session_id'] = session_id

                print(f"    📦 TMUX Session: {session_id}")
                print(f"    📁 Workspace: {agent_workspace}")
                print(f"    🛠️  Tools: {', '.join(agent.tools)}")

                # Load agent instructions
                agent_instructions = self._load_agent_instructions(agent.name)

                if not agent_instructions:
                    print(f"    ⚠️  No instructions found for agent: {agent.name}")
                    agent_instructions = f"You are {agent.name}: {agent.description}"

                # Combine instructions with task
                full_prompt = f"""{agent_instructions}

## Task

{prompt}

## Requirements

- Work in the current directory: {agent_workspace}
- Create all necessary files and implement the solution
- Follow best practices and write clean, well-documented code
- Ensure the implementation is complete and functional
"""

                # Write combined prompt
                full_prompt_file = agent_workspace / "full_prompt.txt"
                full_prompt_file.write_text(full_prompt)

                # Execute Claude CLI
                print(f"    🤖 Executing agent...")

                try:
                    # Build command arguments
                    cmd_args = ['claude', '--print']

                    # Add tool restrictions
                    if agent.tools:
                        cmd_args.append('--allowed-tools')
                        cmd_args.append(' '.join(agent.tools))

                    # Execute claude with stdin
                    process = await asyncio.create_subprocess_exec(
                        *cmd_args,
                        stdin=asyncio.subprocess.PIPE,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        cwd=str(agent_workspace)
                    )

                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(input=full_prompt.encode('utf-8')),
                        timeout=300  # 5 minute timeout
                    )

                    if process.returncode == 0:
                        # DEBUG: Log what Claude returned
                        stdout_text = stdout.decode('utf-8', errors='ignore')
                        stderr_text = stderr.decode('utf-8', errors='ignore')
                        print(f"    📤 Claude stdout ({len(stdout_text)} chars): {stdout_text[:500]}")
                        if stderr_text:
                            print(f"    📤 Claude stderr: {stderr_text[:500]}")
                        print(f"    📁 Working dir: {agent_workspace.absolute()}")

                        # Success - check for created files
                        created_files = list(agent_workspace.glob('**/*'))
                        created_files = [f for f in created_files if f.is_file() and f.name not in ['prompt.txt', 'full_prompt.txt']]

                        result['success'] = True
                        result['output'] = stdout_text
                        result['files_created'] = [str(f.relative_to(agent_workspace)) for f in created_files]

                        print(f"    ✅ Agent completed successfully")
                        print(f"    📄 Files created: {len(created_files)}")
                        if created_files:
                            for f in created_files[:5]:  # Show first 5
                                print(f"       - {f.name}")

                    else:
                        result['success'] = False
                        result['error'] = stderr.decode('utf-8', errors='ignore')
                        print(f"    ❌ Agent failed (return code: {process.returncode})")
                        print(f"    📤 stdout: {stdout.decode('utf-8', errors='ignore')[:500]}")
                        print(f"    📤 stderr: {result['error'][:500]}")

                except asyncio.TimeoutError:
                    result['success'] = False
                    result['error'] = "Execution timeout (5 minutes)"
                    print(f"    ⏱️  Timeout after 5 minutes")

                except Exception as e:
                    result['success'] = False
                    result['error'] = str(e)
                    print(f"    ❌ Execution error: {e}")

                # Mark session as completed
                self.tmux_manager.mark_session_completed(session_id, success=result['success'])

            else:
                # Direct execution (without TMUX) - use same Claude CLI approach
                # This would integrate with Claude Agent SDK directly
                print(f"    📁 Workspace: {agent_workspace}")
                print(f"    🛠️  Tools: {', '.join(agent.tools)}")

                await asyncio.sleep(1)  # Placeholder

                result['success'] = True
                result['output'] = f"Task executed successfully by {agent.name}"

        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
            print(f"    ❌ Error: {e}")

        result['execution_time'] = time.time() - agent_start_time
        print(f"    ✅ Completed in {result['execution_time']:.2f}s")

        return result

    def _record_outcomes(
        self,
        task_id: str,
        task_description: str,
        analysis: TaskAnalysis,
        results: Dict[str, Any],
        execution_time: float
    ):
        """Record task outcomes for learning"""
        all_results = results.get('primary_results', []) + results.get('supporting_results', [])

        for agent_result in all_results:
            agent_name = agent_result['agent']

            outcome = TaskOutcome(
                task_id=task_id,
                agent_name=agent_name,
                task_description=task_description,
                task_type=analysis.task_type,
                success=agent_result.get('success', False),
                execution_time=agent_result.get('execution_time', 0),
                tokens_used=0,  # Would come from SDK
                cost=0.0,  # Would come from SDK
                error_message=agent_result.get('error'),
                prompt_used="",  # Would store actual prompt
                timestamp=datetime.now().isoformat()
            )

            self.skills_system.record_outcome(outcome)

            # Update agent metrics in registry
            self.registry.update_metrics(
                agent_name=agent_name,
                success=outcome.success,
                tokens=outcome.tokens_used,
                cost=outcome.cost,
                duration=outcome.execution_time
            )

    def _print_analysis(self, analysis: TaskAnalysis):
        """Print task analysis"""
        print(f"  Type: {analysis.task_type}")
        print(f"  Complexity: {analysis.complexity}")
        print(f"  Required capabilities: {', '.join(analysis.required_capabilities)}")
        print(f"  Can parallelize: {'Yes' if analysis.can_parallelize else 'No'}")
        print(f"  Estimated subtasks: {analysis.estimated_subtasks}")

    def _print_assignments(self, assignments: List[AgentAssignment]):
        """Print agent assignments"""
        for assignment in assignments:
            priority_emoji = "🥇" if assignment.priority == "primary" else "🥈" if assignment.priority == "supporting" else "🥉"
            print(f"  {priority_emoji} {assignment.agent.name} ({assignment.priority})")
            print(f"     Confidence: {assignment.confidence_score:.0%}")
            print(f"     Reason: {assignment.reason}")
            print(f"     Skill level: {assignment.agent.skill_level}")

    def _print_summary(self, result: Dict[str, Any]):
        """Print execution summary"""
        print(f"\n{'='*80}")
        print(f"📊 EXECUTION SUMMARY")
        print(f"{'='*80}")
        print(f"Status: {'✅ Success' if result['success'] else '❌ Failed'}")
        print(f"Execution time: {result['execution_time']:.2f}s")
        print(f"Agents used: {', '.join(result['agents_used'])}")
        print(f"{'='*80}\n")

    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        return {
            'registry': self.registry.get_agent_stats(),
            'tmux': self.tmux_manager.get_session_stats(),
            'skills': self.skills_system.get_learning_report()
        }

    def generate_report(self, output_path: str = "logs/system_report.md"):
        """Generate comprehensive system report"""
        status = self.get_system_status()

        output = ["# Multi-Agent System Report\n"]
        output.append(f"Generated: {datetime.now().isoformat()}\n")

        # Registry stats
        output.append("## Agent Registry\n")
        output.append(f"- Total agents: {status['registry']['total_agents']}")
        output.append(f"- Total tasks completed: {status['registry']['total_tasks_completed']}")
        output.append(f"- Total cost: ${status['registry']['total_cost']:.2f}\n")

        # TMUX stats
        output.append("## TMUX Sessions\n")
        output.append(f"- Total sessions: {status['tmux']['total_sessions']}")
        output.append(f"- Active sessions: {status['tmux']['active_sessions']}\n")

        # Skills stats
        if status['skills'].get('total_tasks', 0) > 0:
            output.append("## Learning System\n")
            output.append(f"- Total tasks tracked: {status['skills']['total_tasks']}")
            output.append(f"- Overall success rate: {status['skills']['overall_success_rate']:.2f}%")
            output.append(f"- Learned patterns: {status['skills']['learned_patterns']}\n")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text('\n'.join(output))

        print(f"📄 Report generated: {output_path}")
