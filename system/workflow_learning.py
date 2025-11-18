#!/usr/bin/env python3
"""
Workflow Learning System

Analyzes workflow execution history to learn patterns, optimize workflows,
and auto-generate new workflow templates.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict, Counter
from datetime import datetime

from workflow_history import WorkflowHistory, WorkflowExecution, StepStatus


class WorkflowLearner:
    """Learns from workflow execution history."""

    def __init__(self, base_dir: str = None):
        """Initialize workflow learner."""
        if base_dir is None:
            self.base_dir = Path(__file__).parent.parent
        else:
            self.base_dir = Path(base_dir)

        self.history = WorkflowHistory(base_dir)
        self.learned_dir = self.base_dir / "workflows" / "learned"
        self.learned_dir.mkdir(parents=True, exist_ok=True)

    def analyze_workflow(self, workflow_name: str) -> Dict[str, Any]:
        """Analyze a workflow and suggest improvements."""
        stats = self.history.get_workflow_statistics(workflow_name)

        if stats['total_executions'] == 0:
            return {
                'workflow_name': workflow_name,
                'error': 'No execution history found'
            }

        improvements = []
        step_stats = stats.get('step_statistics', {})

        # Analyze step performance
        for step_id, step_data in step_stats.items():
            # Check failure rate
            failure_rate = step_data['failed'] / step_data['total_executions']
            if failure_rate > 0.2:  # More than 20% failures
                improvements.append({
                    'type': 'high_failure_rate',
                    'step_id': step_id,
                    'step_name': step_data['step_name'],
                    'failure_rate': failure_rate,
                    'recommendation': f"Step '{step_data['step_name']}' has high failure rate ({failure_rate:.1%}). "
                                    f"Consider adding more validation or breaking into smaller steps."
                })

            # Check if step is always skipped
            skip_rate = step_data['skipped'] / step_data['total_executions']
            if skip_rate > 0.8:  # Skipped more than 80% of the time
                improvements.append({
                    'type': 'frequently_skipped',
                    'step_id': step_id,
                    'step_name': step_data['step_name'],
                    'skip_rate': skip_rate,
                    'recommendation': f"Step '{step_data['step_name']}' is skipped {skip_rate:.1%} of the time. "
                                    f"Consider making it optional or removing it."
                })

            # Check if actual duration differs significantly from expected
            avg_duration = step_data['avg_duration']
            # TODO: Compare with expected timeout from workflow template

        # Check overall success rate
        if stats['success_rate'] < 0.7:  # Less than 70% success
            improvements.append({
                'type': 'low_success_rate',
                'success_rate': stats['success_rate'],
                'recommendation': f"Workflow has low success rate ({stats['success_rate']:.1%}). "
                                f"Review failed steps and add better error handling."
            })

        return {
            'workflow_name': workflow_name,
            'statistics': stats,
            'improvements': improvements,
            'recommendation_count': len(improvements)
        }

    def detect_task_patterns(self, min_occurrences: int = 3) -> List[Dict[str, Any]]:
        """Detect repeated task patterns that could become workflows."""
        all_history = self.history.get_execution_history(limit=500)

        # Group by task keywords
        task_patterns = defaultdict(list)

        for execution in all_history:
            # Extract keywords from task description
            keywords = self._extract_keywords(execution.task_description)

            # Group executions with similar keywords
            key = " ".join(sorted(keywords)[:5])  # Use first 5 keywords
            task_patterns[key].append(execution)

        # Find patterns with enough occurrences
        potential_workflows = []

        for keywords, executions in task_patterns.items():
            if len(executions) < min_occurrences:
                continue

            # Analyze common agent sequences
            agent_sequences = self._find_common_agent_sequences(executions)

            if agent_sequences:
                potential_workflows.append({
                    'keywords': keywords,
                    'occurrences': len(executions),
                    'agent_sequence': agent_sequences[0],  # Most common sequence
                    'avg_duration': sum(e.duration for e in executions) / len(executions),
                    'success_rate': sum(1 for e in executions if e.status == 'completed') / len(executions),
                    'sample_tasks': [e.task_description for e in executions[:3]]
                })

        # Sort by occurrences
        potential_workflows.sort(key=lambda x: x['occurrences'], reverse=True)

        return potential_workflows

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        # Simple keyword extraction - remove common words
        stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                     'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                     'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
                     'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'}

        words = text.lower().split()
        keywords = [w.strip('.,!?;:') for w in words if w not in stop_words and len(w) > 3]

        return keywords

    def _find_common_agent_sequences(self, executions: List[WorkflowExecution]) -> List[List[str]]:
        """Find common agent sequences across executions."""
        sequences = []

        for execution in executions:
            # Extract agent sequence (only completed steps)
            sequence = [
                step.agent for step in execution.steps
                if step.status == StepStatus.COMPLETED.value
            ]
            if sequence:
                sequences.append(tuple(sequence))

        # Count sequences
        sequence_counts = Counter(sequences)

        # Return most common sequences
        return [list(seq) for seq, count in sequence_counts.most_common(5)]

    def generate_workflow_template(self, pattern: Dict[str, Any], name: str) -> Dict[str, Any]:
        """Generate a workflow template from a detected pattern."""
        workflow = {
            'name': name,
            'version': '1.0.0',
            'description': f"Auto-generated workflow based on {pattern['occurrences']} similar tasks",
            'author': 'learning-system',
            'created': datetime.now().strftime('%Y-%m-%d'),
            'updated': datetime.now().strftime('%Y-%m-%d'),
            'task_types': pattern['keywords'].split(),
            'agents_required': [],
            'agents_optional': [],
            'steps': [],
            'hooks': {
                'pre_workflow': [],
                'post_workflow': [
                    {
                        'action': 'git_commit',
                        'description': 'Commit generated files'
                    }
                ],
                'on_error': []
            },
            'quality_gates': [],
            'learning': {
                'enabled': True,
                'track_metrics': ['step_duration', 'step_success_rate'],
                'improve_on': ['step_order_optimization', 'timeout_adjustment']
            },
            'tags': ['auto-generated', 'learned'],
            'priority': 'medium',
            'usage_count': 0,
            'success_rate': pattern['success_rate'],
            'estimated_duration': int(pattern['avg_duration'])
        }

        # Generate steps from agent sequence
        agent_sequence = pattern['agent_sequence']
        workflow['agents_required'] = list(set(agent_sequence))

        for i, agent in enumerate(agent_sequence):
            step_id = f"step{i+1}"
            depends_on = [f"step{i}"] if i > 0 else []

            step = {
                'id': step_id,
                'name': f"{agent.replace('_', ' ').title()} Task",
                'agent': agent,
                'action': f"Perform {agent} tasks based on requirements",
                'required': True,
                'depends_on': depends_on,
                'outputs': [],
                'timeout': 300
            }

            workflow['steps'].append(step)

        return workflow

    def save_learned_workflow(self, workflow: Dict[str, Any]) -> str:
        """Save a learned workflow template."""
        filename = f"{workflow['name']}.yaml"
        filepath = self.learned_dir / filename

        try:
            with open(filepath, 'w') as f:
                yaml.dump(workflow, f, default_flow_style=False, sort_keys=False)

            return str(filepath)
        except Exception as e:
            print(f"❌ Error saving learned workflow: {e}")
            return ""

    def optimize_workflow_timeouts(self, workflow_name: str) -> Dict[str, int]:
        """Suggest optimized timeouts based on actual execution times."""
        stats = self.history.get_workflow_statistics(workflow_name)

        if stats['total_executions'] == 0:
            return {}

        optimized_timeouts = {}
        step_stats = stats.get('step_statistics', {})

        for step_id, step_data in step_stats.items():
            if step_data['completed'] > 0:
                avg_duration = step_data['avg_duration']

                # Add 50% buffer to average duration
                suggested_timeout = int(avg_duration * 1.5)

                # Minimum 60 seconds
                suggested_timeout = max(60, suggested_timeout)

                optimized_timeouts[step_id] = suggested_timeout

        return optimized_timeouts

    def suggest_step_reordering(self, workflow_name: str) -> List[Tuple[str, str, str]]:
        """Suggest step reordering for better efficiency."""
        # Get workflow execution history
        executions = self.history.get_execution_history(workflow_name=workflow_name)

        if not executions:
            return []

        # Analyze dependencies and parallelization opportunities
        suggestions = []

        # TODO: Implement dependency analysis and parallel execution suggestions

        return suggestions

    def export_learning_report(self, output_path: str = "workflows/LEARNING_REPORT.md"):
        """Export a comprehensive learning report."""
        report = []
        report.append("# Workflow Learning Report\n")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Global statistics
        global_stats = self.history.get_global_statistics()
        report.append("## Global Statistics\n\n")
        report.append(f"- **Total Executions**: {global_stats['total_executions']}\n")
        report.append(f"- **Workflows Used**: {global_stats['workflows_used']}\n")
        report.append(f"- **Overall Success Rate**: {global_stats['success_rate']:.1%}\n")
        report.append(f"- **Average Duration**: {self._format_duration(global_stats['avg_duration'])}\n\n")

        # Most used workflows
        if global_stats.get('most_used_workflows'):
            report.append("## Most Used Workflows\n\n")
            for name, count in global_stats['most_used_workflows']:
                report.append(f"1. **{name}**: {count} executions\n")
            report.append("\n")

        # Analyze each workflow
        report.append("## Workflow Analysis\n\n")
        for workflow_name in global_stats.get('by_workflow', {}).keys():
            analysis = self.analyze_workflow(workflow_name)

            if 'error' in analysis:
                continue

            stats = analysis['statistics']
            improvements = analysis['improvements']

            report.append(f"### {workflow_name}\n\n")
            report.append(f"- **Executions**: {stats['total_executions']}\n")
            report.append(f"- **Success Rate**: {stats['success_rate']:.1%}\n")
            report.append(f"- **Average Duration**: {self._format_duration(stats['avg_duration'])}\n")

            if improvements:
                report.append(f"\n**Recommendations ({len(improvements)}):**\n\n")
                for improvement in improvements:
                    report.append(f"- {improvement['recommendation']}\n")

            report.append("\n")

        # Detected patterns
        patterns = self.detect_task_patterns(min_occurrences=2)

        if patterns:
            report.append("## Detected Task Patterns\n\n")
            report.append("These patterns could become new workflow templates:\n\n")

            for i, pattern in enumerate(patterns, 1):
                report.append(f"### Pattern {i}: {pattern['keywords']}\n\n")
                report.append(f"- **Occurrences**: {pattern['occurrences']}\n")
                report.append(f"- **Success Rate**: {pattern['success_rate']:.1%}\n")
                report.append(f"- **Agent Sequence**: {' → '.join(pattern['agent_sequence'])}\n")
                report.append(f"- **Sample Tasks**:\n")
                for task in pattern['sample_tasks']:
                    report.append(f"  - {task}\n")
                report.append("\n")

        # Write report
        output_file = self.base_dir / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(output_file, 'w') as f:
                f.write(''.join(report))

            print(f"✅ Learning report saved to: {output_file}")
            return str(output_file)

        except Exception as e:
            print(f"❌ Error saving learning report: {e}")
            return ""

    def _format_duration(self, seconds: float) -> str:
        """Format duration in seconds to human-readable string."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = seconds % 60
            return f"{minutes}m {secs:.0f}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"


if __name__ == "__main__":
    # Example usage
    learner = WorkflowLearner()

    # Detect patterns
    patterns = learner.detect_task_patterns(min_occurrences=2)

    if patterns:
        print(f"\n🔍 Found {len(patterns)} potential workflow patterns:\n")
        for i, pattern in enumerate(patterns, 1):
            print(f"{i}. Keywords: {pattern['keywords']}")
            print(f"   Occurrences: {pattern['occurrences']}")
            print(f"   Agent Sequence: {' → '.join(pattern['agent_sequence'])}")
            print()

    # Export learning report
    learner.export_learning_report()
