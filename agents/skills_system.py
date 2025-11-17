"""
Skills System
Tracks agent performance and enables continuous learning
"""
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict


@dataclass
class TaskOutcome:
    """Record of a completed task"""
    task_id: str
    agent_name: str
    task_description: str
    task_type: str
    success: bool
    execution_time: float
    tokens_used: int
    cost: float
    error_message: Optional[str]
    prompt_used: str
    timestamp: str


@dataclass
class PromptPattern:
    """Successful prompt pattern"""
    pattern_id: str
    task_type: str
    template: str
    success_count: int
    avg_execution_time: float
    last_used: str


class SkillsSystem:
    """Manages agent learning and improvement"""

    def __init__(self, history_path: str = "agents/skills_history.json"):
        self.history_path = Path(history_path)
        self.outcomes: List[TaskOutcome] = []
        self.prompt_patterns: Dict[str, PromptPattern] = {}
        self.agent_insights: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self.load_history()

    def load_history(self):
        """Load skills history from disk"""
        if self.history_path.exists():
            with open(self.history_path, 'r') as f:
                data = json.load(f)

                # Load outcomes
                for outcome_data in data.get('outcomes', []):
                    self.outcomes.append(TaskOutcome(**outcome_data))

                # Load prompt patterns
                for pattern_id, pattern_data in data.get('prompt_patterns', {}).items():
                    self.prompt_patterns[pattern_id] = PromptPattern(**pattern_data)

                # Load insights
                self.agent_insights = defaultdict(dict, data.get('agent_insights', {}))

    def save_history(self):
        """Persist skills history to disk"""
        self.history_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            'outcomes': [asdict(outcome) for outcome in self.outcomes],
            'prompt_patterns': {pid: asdict(pattern) for pid, pattern in self.prompt_patterns.items()},
            'agent_insights': dict(self.agent_insights)
        }

        with open(self.history_path, 'w') as f:
            json.dump(data, f, indent=2)

    def record_outcome(self, outcome: TaskOutcome):
        """Record a task outcome"""
        self.outcomes.append(outcome)

        # Limit history size to last 1000 tasks
        if len(self.outcomes) > 1000:
            self.outcomes = self.outcomes[-1000:]

        # Update insights
        self._update_agent_insights(outcome)

        # Learn from successful outcomes
        if outcome.success:
            self._learn_from_success(outcome)

        self.save_history()

    def _update_agent_insights(self, outcome: TaskOutcome):
        """Update agent-specific insights"""
        agent_name = outcome.agent_name

        if agent_name not in self.agent_insights:
            self.agent_insights[agent_name] = {
                'task_types': defaultdict(lambda: {'count': 0, 'success': 0}),
                'common_errors': defaultdict(int),
                'best_tasks': [],
                'worst_tasks': []
            }

        insights = self.agent_insights[agent_name]

        # Update task type performance
        task_type = outcome.task_type
        insights['task_types'][task_type]['count'] += 1
        if outcome.success:
            insights['task_types'][task_type]['success'] += 1

        # Track errors
        if outcome.error_message:
            error_key = outcome.error_message[:100]  # First 100 chars
            insights['common_errors'][error_key] += 1

        # Track best/worst tasks (by execution time for successful tasks)
        if outcome.success:
            task_record = {
                'task_id': outcome.task_id,
                'description': outcome.task_description[:100],
                'execution_time': outcome.execution_time,
                'timestamp': outcome.timestamp
            }

            best = insights.get('best_tasks', [])
            best.append(task_record)
            best.sort(key=lambda x: x['execution_time'])
            insights['best_tasks'] = best[:10]  # Keep top 10

    def _learn_from_success(self, outcome: TaskOutcome):
        """Extract patterns from successful outcomes"""
        # Create or update prompt pattern
        pattern_key = f"{outcome.task_type}_{outcome.agent_name}"

        if pattern_key in self.prompt_patterns:
            pattern = self.prompt_patterns[pattern_key]
            pattern.success_count += 1

            # Update rolling average execution time
            total_time = pattern.avg_execution_time * (pattern.success_count - 1) + outcome.execution_time
            pattern.avg_execution_time = total_time / pattern.success_count
            pattern.last_used = outcome.timestamp

        else:
            # Create new pattern
            self.prompt_patterns[pattern_key] = PromptPattern(
                pattern_id=pattern_key,
                task_type=outcome.task_type,
                template=outcome.prompt_used,
                success_count=1,
                avg_execution_time=outcome.execution_time,
                last_used=outcome.timestamp
            )

    def get_agent_performance(self, agent_name: str) -> Dict[str, Any]:
        """Get comprehensive performance data for an agent"""
        agent_outcomes = [o for o in self.outcomes if o.agent_name == agent_name]

        if not agent_outcomes:
            return {
                'total_tasks': 0,
                'success_rate': 0.0,
                'avg_execution_time': 0.0,
                'total_cost': 0.0
            }

        total = len(agent_outcomes)
        successful = sum(1 for o in agent_outcomes if o.success)
        total_time = sum(o.execution_time for o in agent_outcomes)
        total_cost = sum(o.cost for o in agent_outcomes)

        return {
            'total_tasks': total,
            'success_rate': (successful / total * 100) if total > 0 else 0.0,
            'avg_execution_time': total_time / total if total > 0 else 0.0,
            'total_cost': total_cost,
            'task_type_performance': dict(self.agent_insights.get(agent_name, {}).get('task_types', {}))
        }

    def get_best_prompt_for_task(self, task_type: str, agent_name: str) -> Optional[str]:
        """Get the most successful prompt pattern for a task type"""
        pattern_key = f"{task_type}_{agent_name}"
        pattern = self.prompt_patterns.get(pattern_key)

        if pattern and pattern.success_count >= 3:
            return pattern.template

        return None

    def suggest_improvements(self, agent_name: str) -> List[str]:
        """Generate improvement suggestions for an agent"""
        suggestions = []

        insights = self.agent_insights.get(agent_name)
        if not insights:
            return ["No performance data available yet"]

        # Analyze task type performance
        task_types = insights.get('task_types', {})
        for task_type, stats in task_types.items():
            if stats['count'] >= 5:
                success_rate = (stats['success'] / stats['count']) * 100
                if success_rate < 70:
                    suggestions.append(
                        f"Low success rate ({success_rate:.1f}%) on {task_type} tasks. "
                        f"Consider additional training or tool access."
                    )

        # Analyze common errors
        common_errors = insights.get('common_errors', {})
        if common_errors:
            most_common = sorted(common_errors.items(), key=lambda x: x[1], reverse=True)[0]
            error_msg, count = most_common
            if count >= 3:
                suggestions.append(
                    f"Recurring error (x{count}): {error_msg}. "
                    f"Review error handling or tool permissions."
                )

        # Performance comparison
        agent_perf = self.get_agent_performance(agent_name)
        if agent_perf['total_tasks'] >= 10:
            avg_time = agent_perf['avg_execution_time']
            if avg_time > 300:  # 5 minutes
                suggestions.append(
                    f"Average execution time is high ({avg_time:.1f}s). "
                    f"Consider task decomposition or tool optimization."
                )

        if not suggestions:
            suggestions.append("Performance is good! Continue current approach.")

        return suggestions

    def get_learning_report(self) -> Dict[str, Any]:
        """Generate comprehensive learning report"""
        total_outcomes = len(self.outcomes)
        if total_outcomes == 0:
            return {"status": "No data available"}

        successful = sum(1 for o in self.outcomes if o.success)
        total_cost = sum(o.cost for o in self.outcomes)
        total_time = sum(o.execution_time for o in self.outcomes)

        # Task type distribution
        task_type_dist = defaultdict(int)
        for outcome in self.outcomes:
            task_type_dist[outcome.task_type] += 1

        # Agent performance ranking
        agent_rankings = {}
        for agent_name in set(o.agent_name for o in self.outcomes):
            perf = self.get_agent_performance(agent_name)
            agent_rankings[agent_name] = perf['success_rate']

        agent_rankings = dict(sorted(agent_rankings.items(), key=lambda x: x[1], reverse=True))

        return {
            'total_tasks': total_outcomes,
            'overall_success_rate': (successful / total_outcomes * 100),
            'total_cost': total_cost,
            'total_time': total_time,
            'avg_time_per_task': total_time / total_outcomes,
            'task_type_distribution': dict(task_type_dist),
            'agent_rankings': agent_rankings,
            'learned_patterns': len(self.prompt_patterns),
            'agents_tracked': len(self.agent_insights)
        }

    def export_insights(self, output_path: str):
        """Export insights to a readable format"""
        report = self.get_learning_report()

        output = ["# Multi-Agent Skills Report\n"]
        output.append(f"Generated: {datetime.now().isoformat()}\n")
        output.append(f"## Overall Statistics\n")
        output.append(f"- Total Tasks: {report['total_tasks']}")
        output.append(f"- Success Rate: {report['overall_success_rate']:.2f}%")
        output.append(f"- Total Cost: ${report['total_cost']:.2f}")
        output.append(f"- Average Time per Task: {report['avg_time_per_task']:.1f}s\n")

        output.append(f"## Agent Performance Rankings\n")
        for agent, success_rate in report['agent_rankings'].items():
            output.append(f"- {agent}: {success_rate:.1f}% success rate")

        output.append(f"\n## Task Type Distribution\n")
        for task_type, count in report['task_type_distribution'].items():
            output.append(f"- {task_type}: {count} tasks")

        output.append(f"\n## Improvement Suggestions\n")
        for agent_name in self.agent_insights.keys():
            suggestions = self.suggest_improvements(agent_name)
            output.append(f"\n### {agent_name}")
            for suggestion in suggestions:
                output.append(f"- {suggestion}")

        Path(output_path).write_text('\n'.join(output))
