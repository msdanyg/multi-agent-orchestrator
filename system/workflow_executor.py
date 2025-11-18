#!/usr/bin/env python3
"""
Workflow Executor

Executes workflow templates by coordinating multiple agents,
validating outputs, and tracking execution history.
"""

import sys
import yaml
import importlib.util
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Import workflow management modules
sys.path.insert(0, str(Path(__file__).parent))

# Import workflow-cli using importlib (has hyphen in filename)
_workflow_cli_path = Path(__file__).parent / "workflow-cli.py"
_spec = importlib.util.spec_from_file_location("workflow_cli", _workflow_cli_path)
_workflow_cli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_workflow_cli)
WorkflowManager = _workflow_cli.WorkflowManager
format_duration = _workflow_cli.format_duration

from workflow_history import WorkflowHistory, StepStatus, WorkflowStatus
from workflow_learning import WorkflowLearner


class WorkflowExecutor:
    """Executes workflow templates with agent coordination."""

    def __init__(self, base_dir: str = None):
        """Initialize workflow executor."""
        if base_dir is None:
            self.base_dir = Path(__file__).parent.parent
        else:
            self.base_dir = Path(base_dir)

        self.workflow_manager = WorkflowManager(base_dir)
        self.history = WorkflowHistory(base_dir)
        self.learner = WorkflowLearner(base_dir)

    def match_workflow(self, task_description: str, top_n: int = 3) -> List[Dict[str, Any]]:
        """Find workflows matching a task description."""
        matches = self.workflow_manager.match_workflow(task_description)

        # Return top N matches
        return matches[:top_n]

    def select_best_workflow(self, task_description: str) -> Optional[Dict[str, Any]]:
        """Select the best workflow for a task."""
        matches = self.match_workflow(task_description, top_n=1)

        if not matches:
            return None

        # Get the highest-scoring workflow
        best_match = matches[0]

        # Load full workflow data
        workflow_data = self.workflow_manager.show_workflow(best_match['workflow']['name'])

        if not workflow_data:
            return None

        return {
            'workflow': workflow_data,
            'match_score': best_match['score'],
            'relevance': best_match['relevance']
        }

    def execute_workflow(self, workflow_name: str, task_description: str,
                        orchestrator: Any = None, project_path: Optional[str] = None) -> Dict[str, Any]:
        """Execute a workflow template."""
        # Load workflow
        workflow = self.workflow_manager.show_workflow(workflow_name)

        if not workflow:
            return {
                'success': False,
                'error': f"Workflow '{workflow_name}' not found"
            }

        print(f"\n{'='*80}")
        print(f"🔄 Executing Workflow: {workflow['name']}")
        print(f"{'='*80}")
        print(f"📝 Description: {workflow.get('description', 'N/A')}")
        print(f"⏱️  Estimated Duration: {format_duration(workflow.get('estimated_duration', 0))}")
        print(f"👥 Required Agents: {', '.join(workflow.get('agents_required', []))}")
        print(f"📋 Steps: {len(workflow.get('steps', []))}")
        print()

        # Start tracking execution
        exec_id = self.history.start_execution(
            workflow_name=workflow['name'],
            workflow_version=workflow.get('version', '1.0.0'),
            task_description=task_description,
            project_path=project_path
        )

        # Execute pre-workflow hooks
        self._execute_hooks(workflow.get('hooks', {}).get('pre_workflow', []))

        # Execute steps
        steps = workflow.get('steps', [])
        completed_steps = 0
        failed_steps = 0

        for i, step in enumerate(steps, 1):
            step_id = step['id']
            step_name = step['name']
            agent = step['agent']
            required = step.get('required', True)

            print(f"{'─'*80}")
            print(f"Step {i}/{len(steps)}: {step_name}")
            print(f"Agent: {agent} | Required: {'Yes' if required else 'No'}")

            # Check dependencies
            depends_on = step.get('depends_on', [])
            if depends_on:
                print(f"Dependencies: {', '.join(depends_on)}")

            # Start tracking step
            self.history.start_step(exec_id, step_id, step_name, agent)

            # Execute step
            try:
                # In a real implementation, this would call the orchestrator
                # to execute the agent with the given action
                if orchestrator:
                    result = self._execute_step_with_orchestrator(
                        orchestrator, step, task_description
                    )
                else:
                    # Simulated execution
                    result = self._simulate_step_execution(step)

                if result['success']:
                    # Validate outputs
                    validation = self._validate_step_outputs(step, result.get('outputs', []))

                    self.history.complete_step(
                        exec_id, step_id,
                        outputs=result.get('outputs', []),
                        validation_passed=validation['passed'],
                        validation_errors=validation.get('errors', [])
                    )

                    completed_steps += 1
                    print(f"✅ Step completed successfully")

                    if not validation['passed']:
                        print(f"⚠️  Validation warnings: {', '.join(validation['errors'])}")

                else:
                    self.history.fail_step(exec_id, step_id, result.get('error', 'Unknown error'))
                    failed_steps += 1
                    print(f"❌ Step failed: {result.get('error', 'Unknown error')}")

                    if required:
                        print(f"⛔ Required step failed. Stopping workflow.")
                        break

            except Exception as e:
                self.history.fail_step(exec_id, step_id, str(e))
                failed_steps += 1
                print(f"❌ Step failed with exception: {e}")

                if required:
                    print(f"⛔ Required step failed. Stopping workflow.")
                    break

            # Check quality gates
            quality_gates = workflow.get('quality_gates', [])
            for gate in quality_gates:
                if gate.get('after_step') == step_id:
                    gate_passed = self._check_quality_gate(gate)
                    self.history.record_quality_gate(exec_id, gate['name'], gate_passed)

                    if not gate_passed and gate.get('required', False):
                        print(f"⛔ Quality gate '{gate['name']}' failed. Stopping workflow.")
                        break

        # Execute post-workflow hooks
        self._execute_hooks(workflow.get('hooks', {}).get('post_workflow', []))

        # Complete execution
        success = failed_steps == 0 or (completed_steps > 0 and failed_steps < len(steps))
        self.history.complete_execution(exec_id, success=success)

        print(f"\n{'='*80}")
        print(f"📊 WORKFLOW EXECUTION SUMMARY")
        print(f"{'='*80}")
        print(f"Status: {'✅ Success' if success else '❌ Failed'}")
        print(f"Steps Completed: {completed_steps}/{len(steps)}")
        print(f"Steps Failed: {failed_steps}")
        print(f"{'='*80}\n")

        return {
            'success': success,
            'execution_id': exec_id,
            'completed_steps': completed_steps,
            'failed_steps': failed_steps,
            'total_steps': len(steps)
        }

    def _execute_hooks(self, hooks: List[Dict[str, Any]]):
        """Execute workflow hooks."""
        for hook in hooks:
            action = hook.get('action', '')
            description = hook.get('description', '')

            print(f"🪝 Hook: {description or action}")

            # TODO: Implement actual hook execution
            # For now, just log

    def _execute_step_with_orchestrator(self, orchestrator: Any, step: Dict[str, Any],
                                       task_description: str) -> Dict[str, Any]:
        """Execute a step using the orchestrator."""
        # This would integrate with the actual orchestrator
        # For now, return simulated result
        return self._simulate_step_execution(step)

    def _simulate_step_execution(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate step execution for testing."""
        import time
        import random

        # Simulate some processing time
        time.sleep(random.uniform(0.5, 2.0))

        # Simulate success/failure
        success = random.random() > 0.1  # 90% success rate

        if success:
            outputs = step.get('outputs', [])
            return {
                'success': True,
                'outputs': outputs
            }
        else:
            return {
                'success': False,
                'error': 'Simulated failure'
            }

    def _validate_step_outputs(self, step: Dict[str, Any],
                               actual_outputs: List[str],
                               workspace_path: Path = None) -> Dict[str, Any]:
        """Validate step outputs against validation rules."""
        validation_rules = step.get('validation', [])

        if not validation_rules:
            return {'passed': True, 'errors': []}

        errors = []

        for rule in validation_rules:
            rule_type = rule.get('type', '')

            if rule_type == 'output_exists':
                filename = rule.get('file', '')
                if filename not in actual_outputs:
                    errors.append(f"Expected output file '{filename}' not generated")
                elif workspace_path:
                    file_path = workspace_path / filename
                    if not file_path.exists():
                        errors.append(f"Output file '{filename}' listed but doesn't exist")

            elif rule_type == 'min_lines':
                filename = rule.get('file', '')
                min_lines = rule.get('value', 0)
                if workspace_path:
                    file_path = workspace_path / filename
                    if file_path.exists():
                        try:
                            line_count = len(file_path.read_text().splitlines())
                            if line_count < min_lines:
                                errors.append(f"File '{filename}' has {line_count} lines, expected at least {min_lines}")
                        except Exception as e:
                            errors.append(f"Error reading '{filename}': {str(e)}")
                    else:
                        errors.append(f"Cannot validate '{filename}': file not found")

            elif rule_type == 'syntax_valid':
                language = rule.get('language', '')
                filename = rule.get('file', '')
                if workspace_path and filename:
                    file_path = workspace_path / filename
                    if file_path.exists():
                        # Basic syntax validation
                        if language == 'html':
                            if not self._validate_html_syntax(file_path):
                                errors.append(f"HTML syntax error in '{filename}'")
                        elif language == 'json':
                            if not self._validate_json_syntax(file_path):
                                errors.append(f"JSON syntax error in '{filename}'")
                    else:
                        errors.append(f"Cannot validate '{filename}': file not found")

            elif rule_type == 'custom':
                check_name = rule.get('check', '')
                if check_name == 'all_tests_pass':
                    # This would check QA report for test results
                    # For now, check if QA_REPORT.md mentions failures
                    if workspace_path:
                        qa_report = workspace_path / 'QA_REPORT.md'
                        if qa_report.exists():
                            content = qa_report.read_text().lower()
                            if 'fail' in content or 'bug' in content or 'issue' in content:
                                errors.append("QA testing found issues - check QA_REPORT.md")

        return {
            'passed': len(errors) == 0,
            'errors': errors
        }

    def _validate_html_syntax(self, file_path: Path) -> bool:
        """Basic HTML syntax validation."""
        try:
            content = file_path.read_text()
            # Check for basic HTML structure
            has_doctype = '<!doctype' in content.lower() or '<!DOCTYPE' in content
            has_html_tag = '<html' in content
            has_body_tag = '<body' in content
            # Check for balanced tags (basic check)
            open_tags = content.count('<html')
            close_tags = content.count('</html>')
            return has_doctype and has_html_tag and has_body_tag and open_tags == close_tags
        except Exception:
            return False

    def _validate_json_syntax(self, file_path: Path) -> bool:
        """Validate JSON syntax."""
        try:
            import json
            content = file_path.read_text()
            json.loads(content)
            return True
        except Exception:
            return False

    def _check_quality_gate(self, gate: Dict[str, Any]) -> bool:
        """Check a quality gate."""
        gate_type = gate.get('type', 'manual')

        if gate_type == 'manual':
            # Manual gates require user approval
            response = input(f"\n🚧 Quality Gate: {gate['description']}\nPass? (y/n): ").lower()
            return response == 'y'

        elif gate_type == 'automatic':
            condition = gate.get('condition', '')
            # TODO: Evaluate condition
            return True

        return True

    def print_workflow_preview(self, workflow_name: str):
        """Print a preview of workflow execution."""
        workflow = self.workflow_manager.show_workflow(workflow_name)

        if not workflow:
            print(f"❌ Workflow '{workflow_name}' not found")
            return

        print(f"\n{'='*80}")
        print(f"🔄 Workflow Preview: {workflow['name']}")
        print(f"{'='*80}")
        print(f"📝 {workflow.get('description', 'No description')}\n")

        print(f"⏱️  Estimated Duration: {format_duration(workflow.get('estimated_duration', 0))}")
        print(f"👥 Required Agents: {', '.join(workflow.get('agents_required', []))}")
        print(f"🏷️  Tags: {', '.join(workflow.get('tags', []))}")
        print()

        steps = workflow.get('steps', [])
        print(f"📋 Workflow Steps ({len(steps)}):\n")

        for i, step in enumerate(steps, 1):
            required_badge = "✓" if step.get('required', True) else "○"
            print(f"  {i}. {required_badge} {step.get('name', 'Unnamed')}")
            print(f"     Agent: {step.get('agent', 'N/A')}")

            if step.get('depends_on'):
                print(f"     Depends on: {', '.join(step['depends_on'])}")

            if step.get('outputs'):
                print(f"     Outputs: {', '.join(step['outputs'])}")

            print()

        hooks = workflow.get('hooks', {})
        if any(hooks.values()):
            print(f"🪝 Hooks:")
            if hooks.get('pre_workflow'):
                print(f"   Pre: {len(hooks['pre_workflow'])} action(s)")
            if hooks.get('post_workflow'):
                print(f"   Post: {len(hooks['post_workflow'])} action(s)")
            print()

        print(f"{'='*80}\n")


def main():
    """CLI interface for workflow executor."""
    import argparse

    parser = argparse.ArgumentParser(description="Workflow Executor")
    subparsers = parser.add_subparsers(dest='command')

    # Match command
    match_parser = subparsers.add_parser('match', help='Match workflow to task')
    match_parser.add_argument('task', help='Task description')

    # Execute command
    exec_parser = subparsers.add_parser('execute', help='Execute workflow')
    exec_parser.add_argument('workflow', help='Workflow name')
    exec_parser.add_argument('task', help='Task description')
    exec_parser.add_argument('--project', help='Project path')

    # Preview command
    preview_parser = subparsers.add_parser('preview', help='Preview workflow')
    preview_parser.add_argument('workflow', help='Workflow name')

    args = parser.parse_args()

    executor = WorkflowExecutor()

    if args.command == 'match':
        matches = executor.match_workflow(args.task, top_n=5)

        if matches:
            print(f"\n🎯 Found {len(matches)} matching workflows:\n")
            for match in matches:
                workflow = match['workflow']
                relevance_icon = {'high': '🟢', 'medium': '🟡', 'low': '🔴'}.get(match['relevance'], '⚪')
                print(f"{relevance_icon} {workflow['name']} (Score: {match['score']}, Relevance: {match['relevance']})")
                print(f"   {workflow['description']}")
                print()
        else:
            print("❌ No matching workflows found")

    elif args.command == 'execute':
        result = executor.execute_workflow(
            workflow_name=args.workflow,
            task_description=args.task,
            project_path=args.project
        )

        sys.exit(0 if result['success'] else 1)

    elif args.command == 'preview':
        executor.print_workflow_preview(args.workflow)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
