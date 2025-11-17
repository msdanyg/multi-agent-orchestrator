"""
Simplified Orchestrator (v2)
Delegation-only coordinator without TMUX dependencies
"""
import asyncio
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .registry import AgentRegistry, AgentDefinition
from .task_router import TaskRouter, TaskAnalysis, AgentAssignment
from .skills_system import SkillsSystem, TaskOutcome


class OrchestratorV2:
    """Simplified central coordinator - delegation only, no execution"""

    def __init__(
        self,
        workspace_dir: str = "workspace",
        registry_path: str = "agents/registry.json",
        agents_dir: str = ".claude/agents",
        skills_path: str = "agents/skills_history.json"
    ):
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.registry = AgentRegistry(registry_path, agents_dir)
        self.router = TaskRouter(self.registry)
        self.skills_system = SkillsSystem(skills_path)

        self.active_tasks: Dict[str, Dict[str, Any]] = {}

    async def delegate_task(
        self,
        task_description: str,
        context: Optional[Dict[str, Any]] = None,
        max_agents: int = 3
    ) -> Dict[str, Any]:
        """
        Analyze task and delegate to optimal agents

        Args:
            task_description: Natural language description of the task
            context: Optional context (files, constraints, etc.)
            max_agents: Maximum number of agents to use

        Returns:
            Dictionary with delegation plan and agent assignments
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

        # Create delegation plan
        delegation_plan = self._create_delegation_plan(
            task_id=task_id,
            task_description=task_description,
            analysis=analysis,
            assignments=assignments,
            context=context
        )

        execution_time = time.time() - start_time

        # Store task info for tracking
        self.active_tasks[task_id] = {
            'description': task_description,
            'analysis': analysis,
            'assignments': assignments,
            'plan': delegation_plan,
            'start_time': start_time
        }

        result = {
            'task_id': task_id,
            'success': True,
            'execution_time': execution_time,
            'delegation_plan': delegation_plan,
            'agents_assigned': [a.agent.name for a in assignments],
            'analysis': {
                'task_type': analysis.task_type,
                'complexity': analysis.complexity,
                'can_parallelize': analysis.can_parallelize,
                'capabilities_required': analysis.required_capabilities
            }
        }

        self._print_plan(delegation_plan)

        return result

    def _create_delegation_plan(
        self,
        task_id: str,
        task_description: str,
        analysis: TaskAnalysis,
        assignments: List[AgentAssignment],
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create a detailed delegation plan"""

        # Separate primary and supporting agents
        primary_agents = [a for a in assignments if a.priority == "primary"]
        supporting_agents = [a for a in assignments if a.priority in ["supporting", "optional"]]

        # Create execution steps
        steps = []

        # Step 1: Primary agents (sequential)
        for i, assignment in enumerate(primary_agents, 1):
            agent = assignment.agent
            prompt = self.router.generate_agent_prompt(agent, task_description, context)

            step = {
                'step': i,
                'type': 'primary',
                'agent': agent.name,
                'agent_description': agent.description,
                'tools': agent.tools,
                'prompt': prompt,
                'confidence': assignment.confidence_score,
                'reasoning': assignment.reason
            }
            steps.append(step)

        # Step 2: Supporting agents (can be parallel)
        if supporting_agents:
            if analysis.can_parallelize:
                # Parallel execution
                parallel_steps = []
                for assignment in supporting_agents:
                    agent = assignment.agent
                    prompt = self.router.generate_agent_prompt(agent, task_description, context)

                    parallel_steps.append({
                        'agent': agent.name,
                        'agent_description': agent.description,
                        'tools': agent.tools,
                        'prompt': prompt,
                        'confidence': assignment.confidence_score,
                        'reasoning': assignment.reasoning
                    })

                steps.append({
                    'step': len(steps) + 1,
                    'type': 'parallel',
                    'parallel_steps': parallel_steps
                })
            else:
                # Sequential execution
                for assignment in supporting_agents:
                    agent = assignment.agent
                    prompt = self.router.generate_agent_prompt(agent, task_description, context)

                    steps.append({
                        'step': len(steps) + 1,
                        'type': 'supporting',
                        'agent': agent.name,
                        'agent_description': agent.description,
                        'tools': agent.tools,
                        'prompt': prompt,
                        'confidence': assignment.confidence_score,
                        'reasoning': assignment.reasoning
                    })

        plan = {
            'task_id': task_id,
            'task_description': task_description,
            'execution_strategy': 'parallel' if analysis.can_parallelize else 'sequential',
            'total_steps': len(steps),
            'steps': steps,
            'context': context or {}
        }

        return plan

    def record_agent_outcome(
        self,
        task_id: str,
        agent_name: str,
        success: bool,
        execution_time: float,
        tokens_used: int = 0,
        cost: float = 0.0
    ):
        """Record outcome of an agent's task execution"""
        if task_id not in self.active_tasks:
            print(f"Warning: Unknown task_id {task_id}")
            return

        task_info = self.active_tasks[task_id]

        # Create outcome
        outcome = TaskOutcome(
            task_id=task_id,
            agent_name=agent_name,
            task_type=task_info['analysis'].task_type,
            success=success,
            execution_time=execution_time,
            tokens_used=tokens_used,
            cost=cost
        )

        # Record in skills system
        self.skills_system.record_outcome(outcome)

        # Update agent metrics
        self.registry.update_metrics(
            agent_name=agent_name,
            success=success,
            tokens=tokens_used,
            cost=cost,
            duration=execution_time
        )

        print(f"✅ Recorded outcome for {agent_name}: {'Success' if success else 'Failed'}")

    def get_agent_prompt(self, agent_name: str, task_description: str) -> Optional[str]:
        """Get the specialized prompt for an agent"""
        agent = self.registry.get_agent(agent_name)
        if not agent:
            return None

        return self.router.generate_agent_prompt(agent, task_description, None)

    def list_agents(self) -> List[Dict[str, Any]]:
        """List all available agents with their capabilities"""
        agents = []
        for agent in self.registry.get_all_agents():
            agents.append({
                'name': agent.name,
                'description': agent.description,
                'role': agent.role,
                'tools': agent.tools,
                'capabilities': agent.capabilities,
                'skill_level': agent.skill_level,
                'success_rate': agent.metrics.success_rate if agent.metrics else 0.0,
                'total_tasks': agent.metrics.total_tasks if agent.metrics else 0
            })
        return agents

    def get_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics"""
        registry_stats = self.registry.get_agent_stats()
        skills_stats = self.skills_system.get_insights()

        return {
            'registry': registry_stats,
            'skills': {
                'total_insights': len(skills_stats.get('agent_insights', {})),
                'patterns_learned': len(skills_stats.get('prompt_patterns', []))
            },
            'active_tasks': len(self.active_tasks)
        }

    def _print_analysis(self, analysis: TaskAnalysis):
        """Print task analysis"""
        print(f"  Task Type: {analysis.task_type}")
        print(f"  Complexity: {analysis.complexity}")
        print(f"  Can Parallelize: {analysis.can_parallelize}")
        print(f"  Required Capabilities: {', '.join(analysis.required_capabilities)}")

    def _print_assignments(self, assignments: List[AgentAssignment]):
        """Print agent assignments"""
        for assignment in assignments:
            agent = assignment.agent
            print(f"\n  {assignment.priority.upper()}: {agent.name}")
            print(f"    Description: {agent.description}")
            print(f"    Confidence: {assignment.confidence_score:.2f}")
            print(f"    Reasoning: {assignment.reason}")

    def _print_plan(self, plan: Dict[str, Any]):
        """Print delegation plan"""
        print(f"\n{'='*80}")
        print(f"📋 DELEGATION PLAN")
        print(f"{'='*80}")
        print(f"Strategy: {plan['execution_strategy']}")
        print(f"Total Steps: {plan['total_steps']}\n")

        for step in plan['steps']:
            if step['type'] == 'parallel':
                print(f"Step {step['step']}: PARALLEL EXECUTION")
                for p_step in step['parallel_steps']:
                    print(f"  ⚡ {p_step['agent']}: {p_step['agent_description'][:50]}...")
            else:
                print(f"Step {step['step']}: {step['agent']}")
                print(f"  Type: {step['type']}")
                print(f"  Tools: {', '.join(step['tools'])}")
                print(f"  Confidence: {step['confidence']:.2f}")

        print(f"\n{'='*80}\n")
