#!/usr/bin/env python3
"""
Workflow Management CLI

Command-line tool for managing workflow templates in the multi-agent orchestrator system.
Allows users to list, view, create, edit, validate, and execute workflows.
"""

import os
import sys
import json
import yaml
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import subprocess

class WorkflowManager:
    """Manages workflow templates and execution."""

    def __init__(self, base_dir: str = None):
        """Initialize workflow manager."""
        if base_dir is None:
            # Get the Multi-agent-v2 directory
            self.base_dir = Path(__file__).parent.parent
        else:
            self.base_dir = Path(base_dir)

        self.workflows_dir = self.base_dir / "workflows"
        self.templates_dir = self.workflows_dir / "templates"
        self.custom_dir = self.templates_dir / "custom"
        self.learned_dir = self.workflows_dir / "learned"
        self.history_dir = self.workflows_dir / "history"

        # Ensure directories exist
        for dir_path in [self.workflows_dir, self.templates_dir, self.custom_dir,
                         self.learned_dir, self.history_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def list_workflows(self, detailed: bool = False, custom_only: bool = False) -> List[Dict]:
        """List all available workflows."""
        workflows = []

        # Search directories
        search_dirs = [self.custom_dir] if custom_only else [self.templates_dir, self.custom_dir]

        for search_dir in search_dirs:
            if not search_dir.exists():
                continue

            for workflow_file in search_dir.glob("*.yaml"):
                try:
                    with open(workflow_file, 'r') as f:
                        workflow_data = yaml.safe_load(f)

                    workflow_info = {
                        'name': workflow_data.get('name', workflow_file.stem),
                        'version': workflow_data.get('version', '1.0.0'),
                        'description': workflow_data.get('description', 'No description'),
                        'file': str(workflow_file.relative_to(self.base_dir)),
                        'custom': search_dir == self.custom_dir,
                        'steps': len(workflow_data.get('steps', [])),
                        'priority': workflow_data.get('priority', 'medium'),
                        'tags': workflow_data.get('tags', []),
                        'usage_count': workflow_data.get('usage_count', 0),
                        'success_rate': workflow_data.get('success_rate', 0.0),
                        'estimated_duration': workflow_data.get('estimated_duration', 0)
                    }

                    if detailed:
                        workflow_info['agents_required'] = workflow_data.get('agents_required', [])
                        workflow_info['agents_optional'] = workflow_data.get('agents_optional', [])
                        workflow_info['task_types'] = workflow_data.get('task_types', [])

                    workflows.append(workflow_info)

                except Exception as e:
                    print(f"⚠️  Error loading {workflow_file.name}: {e}", file=sys.stderr)

        # Sort by priority and name
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        workflows.sort(key=lambda w: (priority_order.get(w['priority'], 3), w['name']))

        return workflows

    def show_workflow(self, name: str) -> Optional[Dict]:
        """Show detailed information about a specific workflow."""
        workflow_file = self._find_workflow_file(name)
        if not workflow_file:
            print(f"❌ Workflow '{name}' not found", file=sys.stderr)
            return None

        try:
            with open(workflow_file, 'r') as f:
                workflow_data = yaml.safe_load(f)
            return workflow_data
        except Exception as e:
            print(f"❌ Error loading workflow: {e}", file=sys.stderr)
            return None

    def _find_workflow_file(self, name: str) -> Optional[Path]:
        """Find workflow file by name."""
        # Check custom first, then templates
        for search_dir in [self.custom_dir, self.templates_dir]:
            workflow_file = search_dir / f"{name}.yaml"
            if workflow_file.exists():
                return workflow_file

        return None

    def create_workflow(self, name: str, template: str = "base",
                       description: str = "", interactive: bool = True) -> bool:
        """Create a new workflow."""
        # Validate name
        if not name or not name.replace('-', '').replace('_', '').isalnum():
            print("❌ Invalid workflow name. Use alphanumeric characters, hyphens, and underscores only.",
                  file=sys.stderr)
            return False

        # Check if exists
        if self._find_workflow_file(name):
            print(f"❌ Workflow '{name}' already exists", file=sys.stderr)
            return False

        # Create workflow structure
        workflow_data = {
            'name': name,
            'version': '1.0.0',
            'description': description or f"Custom workflow: {name}",
            'author': 'user',
            'created': datetime.now().strftime('%Y-%m-%d'),
            'updated': datetime.now().strftime('%Y-%m-%d'),
            'task_types': [],
            'agents_required': [],
            'agents_optional': [],
            'steps': [],
            'hooks': {
                'pre_workflow': [],
                'post_workflow': [],
                'on_error': []
            },
            'quality_gates': [],
            'learning': {
                'enabled': True,
                'track_metrics': ['step_duration', 'step_success_rate'],
                'improve_on': ['step_order_optimization']
            },
            'tags': [],
            'priority': 'medium',
            'usage_count': 0,
            'success_rate': 0.0,
            'estimated_duration': 600
        }

        # Save workflow
        workflow_file = self.custom_dir / f"{name}.yaml"
        try:
            with open(workflow_file, 'w') as f:
                yaml.dump(workflow_data, f, default_flow_style=False, sort_keys=False)

            print(f"✅ Workflow '{name}' created successfully")
            print(f"📄 File: {workflow_file.relative_to(self.base_dir)}")
            print(f"\n💡 Edit the workflow file to add steps and configuration")

            if interactive:
                response = input("\n📝 Open in editor now? (y/n): ").lower()
                if response == 'y':
                    self.edit_workflow(name)

            return True

        except Exception as e:
            print(f"❌ Error creating workflow: {e}", file=sys.stderr)
            return False

    def edit_workflow(self, name: str) -> bool:
        """Open workflow in default editor."""
        workflow_file = self._find_workflow_file(name)
        if not workflow_file:
            print(f"❌ Workflow '{name}' not found", file=sys.stderr)
            return False

        # Determine editor
        editor = os.environ.get('EDITOR', 'nano')

        try:
            subprocess.call([editor, str(workflow_file)])
            print(f"✅ Workflow '{name}' edited")
            return True
        except Exception as e:
            print(f"❌ Error opening editor: {e}", file=sys.stderr)
            return False

    def validate_workflow(self, name: str) -> bool:
        """Validate workflow structure and syntax."""
        workflow_data = self.show_workflow(name)
        if not workflow_data:
            return False

        errors = []
        warnings = []

        # Required fields
        required_fields = ['name', 'version', 'description', 'steps']
        for field in required_fields:
            if field not in workflow_data:
                errors.append(f"Missing required field: {field}")

        # Validate steps
        if 'steps' in workflow_data:
            steps = workflow_data['steps']
            if not steps:
                warnings.append("No steps defined")

            step_ids = set()
            for i, step in enumerate(steps):
                # Check required step fields
                if 'id' not in step:
                    errors.append(f"Step {i}: Missing 'id' field")
                else:
                    if step['id'] in step_ids:
                        errors.append(f"Step {i}: Duplicate step ID '{step['id']}'")
                    step_ids.add(step['id'])

                if 'agent' not in step:
                    errors.append(f"Step {i} ({step.get('id', 'unknown')}): Missing 'agent' field")

                if 'action' not in step:
                    errors.append(f"Step {i} ({step.get('id', 'unknown')}): Missing 'action' field")

                # Validate dependencies
                if 'depends_on' in step:
                    for dep in step['depends_on']:
                        if dep not in step_ids:
                            errors.append(f"Step {step['id']}: Invalid dependency '{dep}'")

        # Validate agents
        if 'agents_required' in workflow_data:
            if not workflow_data['agents_required']:
                warnings.append("No required agents specified")

        # Print results
        print(f"🔍 Validating workflow: {name}")
        print(f"{'='*60}")

        if errors:
            print(f"\n❌ ERRORS ({len(errors)}):")
            for error in errors:
                print(f"  • {error}")

        if warnings:
            print(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for warning in warnings:
                print(f"  • {warning}")

        if not errors and not warnings:
            print("\n✅ Workflow is valid!")
            return True
        elif not errors:
            print("\n✅ Workflow is valid (with warnings)")
            return True
        else:
            print(f"\n❌ Workflow validation failed with {len(errors)} error(s)")
            return False

    def delete_workflow(self, name: str, force: bool = False) -> bool:
        """Delete a workflow (custom workflows only)."""
        workflow_file = self.custom_dir / f"{name}.yaml"

        if not workflow_file.exists():
            print(f"❌ Custom workflow '{name}' not found", file=sys.stderr)
            return False

        if not force:
            response = input(f"⚠️  Delete workflow '{name}'? (y/n): ").lower()
            if response != 'y':
                print("❌ Cancelled")
                return False

        try:
            workflow_file.unlink()
            print(f"✅ Workflow '{name}' deleted")
            return True
        except Exception as e:
            print(f"❌ Error deleting workflow: {e}", file=sys.stderr)
            return False

    def export_workflow(self, name: str, output_format: str = "yaml", output_file: str = None) -> bool:
        """Export workflow to file."""
        workflow_data = self.show_workflow(name)
        if not workflow_data:
            return False

        if output_file is None:
            output_file = f"{name}.{output_format}"

        try:
            with open(output_file, 'w') as f:
                if output_format == 'json':
                    json.dump(workflow_data, f, indent=2)
                else:  # yaml
                    yaml.dump(workflow_data, f, default_flow_style=False, sort_keys=False)

            print(f"✅ Workflow exported to: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Error exporting workflow: {e}", file=sys.stderr)
            return False

    def import_workflow(self, file_path: str, custom: bool = True) -> bool:
        """Import workflow from file."""
        file_path = Path(file_path)

        if not file_path.exists():
            print(f"❌ File not found: {file_path}", file=sys.stderr)
            return False

        try:
            with open(file_path, 'r') as f:
                if file_path.suffix == '.json':
                    workflow_data = json.load(f)
                else:
                    workflow_data = yaml.safe_load(f)

            # Validate required fields
            if 'name' not in workflow_data:
                print("❌ Workflow missing 'name' field", file=sys.stderr)
                return False

            # Determine destination
            dest_dir = self.custom_dir if custom else self.templates_dir
            dest_file = dest_dir / f"{workflow_data['name']}.yaml"

            # Check if exists
            if dest_file.exists():
                response = input(f"⚠️  Workflow '{workflow_data['name']}' exists. Overwrite? (y/n): ").lower()
                if response != 'y':
                    print("❌ Cancelled")
                    return False

            # Save
            with open(dest_file, 'w') as f:
                yaml.dump(workflow_data, f, default_flow_style=False, sort_keys=False)

            print(f"✅ Workflow '{workflow_data['name']}' imported successfully")
            return True

        except Exception as e:
            print(f"❌ Error importing workflow: {e}", file=sys.stderr)
            return False

    def show_stats(self) -> Dict[str, Any]:
        """Show workflow system statistics."""
        workflows = self.list_workflows(detailed=True)

        total = len(workflows)
        custom = sum(1 for w in workflows if w['custom'])
        system = total - custom

        # Calculate stats
        total_usage = sum(w['usage_count'] for w in workflows)
        avg_success_rate = sum(w['success_rate'] for w in workflows) / total if total > 0 else 0

        # Group by priority
        by_priority = {}
        for w in workflows:
            priority = w['priority']
            by_priority[priority] = by_priority.get(priority, 0) + 1

        # Group by tags
        all_tags = {}
        for w in workflows:
            for tag in w['tags']:
                all_tags[tag] = all_tags.get(tag, 0) + 1

        stats = {
            'total_workflows': total,
            'system_workflows': system,
            'custom_workflows': custom,
            'total_usage': total_usage,
            'avg_success_rate': avg_success_rate,
            'by_priority': by_priority,
            'tags': all_tags,
            'most_used': sorted(workflows, key=lambda w: w['usage_count'], reverse=True)[:5]
        }

        return stats

    def match_workflow(self, task: str) -> List[Dict]:
        """Match workflows to a task description."""
        task_lower = task.lower()
        workflows = self.list_workflows(detailed=True)

        matches = []
        for workflow in workflows:
            score = 0

            # Check task_types
            for task_type in workflow.get('task_types', []):
                if task_type.lower() in task_lower:
                    score += 10

            # Check name
            if workflow['name'].replace('-', ' ') in task_lower:
                score += 5

            # Check description
            if any(word in task_lower for word in workflow['description'].lower().split()):
                score += 2

            # Check tags
            for tag in workflow.get('tags', []):
                if tag in task_lower:
                    score += 3

            if score > 0:
                matches.append({
                    'workflow': workflow,
                    'score': score,
                    'relevance': 'high' if score >= 10 else 'medium' if score >= 5 else 'low'
                })

        # Sort by score
        matches.sort(key=lambda m: m['score'], reverse=True)
        return matches


def format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable string."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def print_workflows_table(workflows: List[Dict], detailed: bool = False):
    """Print workflows in a formatted table."""
    if not workflows:
        print("No workflows found")
        return

    print(f"\n{'='*80}")
    print(f"📋 Available Workflows ({len(workflows)})")
    print(f"{'='*80}\n")

    for workflow in workflows:
        # Priority indicator
        priority_icon = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }.get(workflow['priority'], '⚪')

        # Custom indicator
        custom_badge = " [CUSTOM]" if workflow['custom'] else ""

        print(f"{priority_icon} {workflow['name']}{custom_badge}")
        print(f"   {workflow['description']}")
        print(f"   📊 {workflow['steps']} steps • {format_duration(workflow['estimated_duration'])}")

        if workflow['usage_count'] > 0:
            print(f"   📈 Used {workflow['usage_count']} times • {workflow['success_rate']:.1%} success rate")

        if detailed and workflow.get('task_types'):
            print(f"   🏷️  Triggers: {', '.join(workflow['task_types'][:3])}")

        if workflow.get('tags'):
            print(f"   🏷️  Tags: {', '.join(workflow['tags'])}")

        print()


def print_workflow_details(workflow: Dict):
    """Print detailed workflow information."""
    print(f"\n{'='*80}")
    print(f"📋 Workflow: {workflow['name']}")
    print(f"{'='*80}\n")

    print(f"📝 Description: {workflow.get('description', 'N/A')}")
    print(f"🔢 Version: {workflow.get('version', 'N/A')}")
    print(f"👤 Author: {workflow.get('author', 'N/A')}")
    print(f"📅 Created: {workflow.get('created', 'N/A')}")
    print(f"🔄 Updated: {workflow.get('updated', 'N/A')}")
    print(f"⏱️  Estimated Duration: {format_duration(workflow.get('estimated_duration', 0))}")
    print(f"🎯 Priority: {workflow.get('priority', 'N/A')}")

    # Task types
    if workflow.get('task_types'):
        print(f"\n🏷️  Task Types:")
        for task_type in workflow['task_types']:
            print(f"   • {task_type}")

    # Agents
    if workflow.get('agents_required'):
        print(f"\n👥 Required Agents:")
        for agent in workflow['agents_required']:
            print(f"   ✓ {agent}")

    if workflow.get('agents_optional'):
        print(f"\n👥 Optional Agents:")
        for agent in workflow['agents_optional']:
            print(f"   ○ {agent}")

    # Steps
    if workflow.get('steps'):
        print(f"\n📋 Workflow Steps ({len(workflow['steps'])}):")
        for i, step in enumerate(workflow['steps'], 1):
            required_badge = "✓" if step.get('required', True) else "○"
            print(f"\n   {i}. {required_badge} {step.get('name', 'Unnamed')}")
            print(f"      Agent: {step.get('agent', 'N/A')}")
            print(f"      ID: {step.get('id', 'N/A')}")

            if step.get('depends_on'):
                print(f"      Depends on: {', '.join(step['depends_on'])}")

            if step.get('outputs'):
                print(f"      Outputs: {', '.join(step['outputs'])}")

            if step.get('timeout'):
                print(f"      Timeout: {step['timeout']}s")

    # Hooks
    hooks = workflow.get('hooks', {})
    if any(hooks.values()):
        print(f"\n🪝 Hooks:")
        if hooks.get('pre_workflow'):
            print(f"   Pre-workflow: {len(hooks['pre_workflow'])} action(s)")
        if hooks.get('post_workflow'):
            print(f"   Post-workflow: {len(hooks['post_workflow'])} action(s)")
        if hooks.get('on_error'):
            print(f"   On error: {len(hooks['on_error'])} action(s)")

    # Quality gates
    if workflow.get('quality_gates'):
        print(f"\n🚧 Quality Gates:")
        for gate in workflow['quality_gates']:
            print(f"   • {gate.get('name', 'Unnamed')}: {gate.get('description', 'N/A')}")

    # Tags
    if workflow.get('tags'):
        print(f"\n🏷️  Tags: {', '.join(workflow['tags'])}")

    # Stats
    if workflow.get('usage_count', 0) > 0:
        print(f"\n📈 Statistics:")
        print(f"   Usage Count: {workflow['usage_count']}")
        print(f"   Success Rate: {workflow.get('success_rate', 0):.1%}")

    print()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Workflow Management CLI for Multi-Agent Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # List command
    list_parser = subparsers.add_parser('list', help='List all workflows')
    list_parser.add_argument('-d', '--detailed', action='store_true', help='Show detailed information')
    list_parser.add_argument('-c', '--custom', action='store_true', help='Show only custom workflows')

    # Show command
    show_parser = subparsers.add_parser('show', help='Show workflow details')
    show_parser.add_argument('name', help='Workflow name')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create new workflow')
    create_parser.add_argument('name', help='Workflow name')
    create_parser.add_argument('-d', '--description', default='', help='Workflow description')
    create_parser.add_argument('--no-interactive', action='store_true', help='Skip interactive prompts')

    # Edit command
    edit_parser = subparsers.add_parser('edit', help='Edit workflow')
    edit_parser.add_argument('name', help='Workflow name')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate workflow')
    validate_parser.add_argument('name', help='Workflow name')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete workflow')
    delete_parser.add_argument('name', help='Workflow name')
    delete_parser.add_argument('-f', '--force', action='store_true', help='Skip confirmation')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export workflow')
    export_parser.add_argument('name', help='Workflow name')
    export_parser.add_argument('-f', '--format', choices=['yaml', 'json'], default='yaml', help='Output format')
    export_parser.add_argument('-o', '--output', help='Output file')

    # Import command
    import_parser = subparsers.add_parser('import', help='Import workflow')
    import_parser.add_argument('file', help='Workflow file path')
    import_parser.add_argument('--system', action='store_true', help='Import as system workflow')

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show workflow statistics')

    # Match command
    match_parser = subparsers.add_parser('match', help='Find workflows matching a task')
    match_parser.add_argument('task', help='Task description')

    args = parser.parse_args()

    # Create workflow manager
    manager = WorkflowManager()

    # Execute command
    if args.command == 'list':
        workflows = manager.list_workflows(detailed=args.detailed, custom_only=args.custom)
        print_workflows_table(workflows, detailed=args.detailed)

    elif args.command == 'show':
        workflow = manager.show_workflow(args.name)
        if workflow:
            print_workflow_details(workflow)

    elif args.command == 'create':
        manager.create_workflow(args.name, description=args.description,
                               interactive=not args.no_interactive)

    elif args.command == 'edit':
        manager.edit_workflow(args.name)

    elif args.command == 'validate':
        manager.validate_workflow(args.name)

    elif args.command == 'delete':
        manager.delete_workflow(args.name, force=args.force)

    elif args.command == 'export':
        manager.export_workflow(args.name, output_format=args.format, output_file=args.output)

    elif args.command == 'import':
        manager.import_workflow(args.file, custom=not args.system)

    elif args.command == 'stats':
        stats = manager.show_stats()
        print(f"\n{'='*80}")
        print(f"📊 Workflow System Statistics")
        print(f"{'='*80}\n")
        print(f"Total Workflows: {stats['total_workflows']}")
        print(f"  • System: {stats['system_workflows']}")
        print(f"  • Custom: {stats['custom_workflows']}")
        print(f"\nTotal Usage: {stats['total_usage']}")
        print(f"Average Success Rate: {stats['avg_success_rate']:.1%}")

        if stats['by_priority']:
            print(f"\nBy Priority:")
            for priority, count in stats['by_priority'].items():
                print(f"  • {priority}: {count}")

        if stats['tags']:
            print(f"\nTop Tags:")
            sorted_tags = sorted(stats['tags'].items(), key=lambda x: x[1], reverse=True)[:5]
            for tag, count in sorted_tags:
                print(f"  • {tag}: {count}")

        if stats['most_used']:
            print(f"\nMost Used Workflows:")
            for workflow in stats['most_used']:
                if workflow['usage_count'] > 0:
                    print(f"  • {workflow['name']}: {workflow['usage_count']} times")
        print()

    elif args.command == 'match':
        matches = manager.match_workflow(args.task)
        if matches:
            print(f"\n{'='*80}")
            print(f"🎯 Matching Workflows for: \"{args.task}\"")
            print(f"{'='*80}\n")

            for match in matches:
                workflow = match['workflow']
                relevance_icon = {'high': '🟢', 'medium': '🟡', 'low': '🔴'}.get(match['relevance'], '⚪')
                print(f"{relevance_icon} {workflow['name']} (Score: {match['score']}, Relevance: {match['relevance']})")
                print(f"   {workflow['description']}")
                print(f"   {workflow['steps']} steps • {format_duration(workflow['estimated_duration'])}")
                print()
        else:
            print(f"❌ No workflows found matching: \"{args.task}\"")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
