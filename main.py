#!/usr/bin/env python3
"""
Multi-Agent Manager - Main Entry Point
Orchestrates multiple specialized Claude agents for complex tasks
"""
import asyncio
import argparse
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, skip
    pass

from agents import Orchestrator
from agents.orchestrator_workflow import WorkflowOrchestrator


async def run_task(task: str, max_agents: int = 3, use_tmux: bool = True,
                  enable_workflows: bool = True, force_workflow: str = None,
                  project_name: str = None):
    """Execute a task using the multi-agent system"""
    try:
        # Use workflow-enabled orchestrator if workflows are enabled
        if enable_workflows:
            orchestrator = WorkflowOrchestrator(
                workspace_dir="workspace",
                registry_path="agents/registry.json",
                skills_path="agents/skills_history.json",
                max_parallel_agents=5,
                enable_workflows=True
            )
        else:
            orchestrator = Orchestrator(
                workspace_dir="workspace",
                registry_path="agents/registry.json",
                skills_path="agents/skills_history.json",
                max_parallel_agents=5
            )

        # Prepare context with project information
        context = {}
        if project_name:
            context['project_name'] = project_name
            context['project_path'] = f"projects/{project_name}"

        # Execute task with appropriate parameters based on orchestrator type
        if enable_workflows:
            result = await orchestrator.execute_task(
                task_description=task,
                max_agents=max_agents,
                use_tmux=use_tmux,
                force_workflow=force_workflow,
                context=context if project_name else None
            )
        else:
            result = await orchestrator.execute_task(
                task_description=task,
                max_agents=max_agents,
                use_tmux=use_tmux,
                context=context if project_name else None
            )

        return result

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return {'success': False, 'error': str(e)}


async def show_status():
    """Show system status"""
    try:
        orchestrator = Orchestrator()
        status = orchestrator.get_system_status()

        print("\n" + "="*80)
        print("📊 MULTI-AGENT SYSTEM STATUS")
        print("="*80)

        print("\n🤖 Agent Registry:")
        print(f"  Total agents: {status['registry']['total_agents']}")
        print(f"  Tasks completed: {status['registry']['total_tasks_completed']}")
        print(f"  Total cost: ${status['registry']['total_cost']:.2f}")

        print("\n📦 TMUX Sessions:")
        print(f"  Total sessions: {status['tmux']['total_sessions']}")
        print(f"  Active sessions: {status['tmux']['active_sessions']}")

        if status['skills'].get('total_tasks', 0) > 0:
            print("\n📚 Learning System:")
            print(f"  Total tasks: {status['skills']['total_tasks']}")
            print(f"  Success rate: {status['skills']['overall_success_rate']:.2f}%")
            print(f"  Learned patterns: {status['skills']['learned_patterns']}")

        print("\n" + "="*80 + "\n")

    except Exception as e:
        print(f"❌ Error getting status: {e}")


async def list_agents():
    """List all registered agents"""
    try:
        orchestrator = Orchestrator()
        agents = orchestrator.registry.get_all_agents()

        print("\n" + "="*80)
        print("🤖 REGISTERED AGENTS")
        print("="*80 + "\n")

        for agent in agents:
            print(f"📌 {agent.name}")
            print(f"   Description: {agent.description}")
            print(f"   Role: {agent.role}")
            print(f"   Skill level: {agent.skill_level}")
            print(f"   Capabilities: {', '.join(agent.capabilities[:5])}")
            print(f"   Tools: {', '.join(agent.tools)}")

            if agent.metrics:
                print(f"   Performance:")
                print(f"     • Tasks: {agent.metrics.total_tasks}")
                print(f"     • Success rate: {agent.metrics.success_rate:.1f}%")
                if agent.metrics.avg_completion_time > 0:
                    print(f"     • Avg time: {agent.metrics.avg_completion_time:.1f}s")

            print()

        print("="*80 + "\n")

    except Exception as e:
        print(f"❌ Error listing agents: {e}")


async def generate_report(output_path: str = "logs/system_report.md"):
    """Generate system report"""
    try:
        orchestrator = Orchestrator()
        orchestrator.generate_report(output_path)
        orchestrator.skills_system.export_insights("logs/skills_report.md")
        print("✅ Reports generated successfully")

    except Exception as e:
        print(f"❌ Error generating report: {e}")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Multi-Agent Manager - Orchestrate specialized Claude agents for complex tasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Execute a task in a project (creates if needed)
  python main.py task "Build a web application" --project my-app

  # Execute with workflow matching
  python main.py task "Build a web application"

  # Execute in project with specific workflow
  python main.py task "Build calculator" --project calculator-app --workflow web-app-development

  # Force use of specific workflow
  python main.py task "Build calculator app" --workflow web-app-development

  # Execute without workflow matching (direct agent selection)
  python main.py task "Debug authentication" --no-workflows

  # Show system status
  python main.py status

  # List all agents
  python main.py agents

  # Generate reports
  python main.py report

  # Execute without TMUX (direct execution)
  python main.py task "Fix bugs in the payment system" --no-tmux
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Task command
    task_parser = subparsers.add_parser('task', help='Execute a task')
    task_parser.add_argument('description', type=str, help='Task description')
    task_parser.add_argument(
        '--max-agents',
        type=int,
        default=3,
        help='Maximum number of agents to use (default: 3)'
    )
    task_parser.add_argument(
        '--no-tmux',
        action='store_true',
        help='Execute without TMUX sessions'
    )
    task_parser.add_argument(
        '--no-workflows',
        action='store_true',
        help='Disable workflow matching (use direct agent selection)'
    )
    task_parser.add_argument(
        '--workflow',
        type=str,
        help='Force use of specific workflow (by name)'
    )
    task_parser.add_argument(
        '--project',
        type=str,
        help='Execute in specific project directory (creates if needed)'
    )

    # Status command
    subparsers.add_parser('status', help='Show system status')

    # Agents command
    subparsers.add_parser('agents', help='List all registered agents')

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate system report')
    report_parser.add_argument(
        '--output',
        type=str,
        default='logs/system_report.md',
        help='Output path for report (default: logs/system_report.md)'
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute command
    if args.command == 'task':
        result = asyncio.run(run_task(
            task=args.description,
            max_agents=args.max_agents,
            use_tmux=not args.no_tmux,
            enable_workflows=not args.no_workflows,
            force_workflow=args.workflow,
            project_name=args.project
        ))
        sys.exit(0 if result.get('success') else 1)

    elif args.command == 'status':
        asyncio.run(show_status())

    elif args.command == 'agents':
        asyncio.run(list_agents())

    elif args.command == 'report':
        asyncio.run(generate_report(args.output))


if __name__ == "__main__":
    main()
