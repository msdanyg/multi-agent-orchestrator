#!/usr/bin/env python3
"""
Workflow Execution History System

Tracks workflow executions for learning, optimization, and analytics.
"""

import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class StepStatus(Enum):
    """Status of a workflow step."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowStatus(Enum):
    """Status of workflow execution."""
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


@dataclass
class StepExecution:
    """Record of a single step execution."""
    step_id: str
    step_name: str
    agent: str
    status: str
    start_time: str
    end_time: Optional[str] = None
    duration: float = 0.0
    outputs: List[str] = None
    validation_passed: bool = True
    validation_errors: List[str] = None
    error_message: Optional[str] = None

    def __post_init__(self):
        if self.outputs is None:
            self.outputs = []
        if self.validation_errors is None:
            self.validation_errors = []


@dataclass
class WorkflowExecution:
    """Record of a workflow execution."""
    execution_id: str
    workflow_name: str
    workflow_version: str
    task_description: str
    status: str
    start_time: str
    end_time: Optional[str] = None
    duration: float = 0.0
    steps: List[StepExecution] = None
    total_steps: int = 0
    completed_steps: int = 0
    failed_steps: int = 0
    skipped_steps: int = 0
    quality_gates_passed: List[str] = None
    quality_gates_failed: List[str] = None
    user_interventions: int = 0
    outputs_generated: List[str] = None
    project_path: Optional[str] = None

    def __post_init__(self):
        if self.steps is None:
            self.steps = []
        if self.quality_gates_passed is None:
            self.quality_gates_passed = []
        if self.quality_gates_failed is None:
            self.quality_gates_failed = []
        if self.outputs_generated is None:
            self.outputs_generated = []


class WorkflowHistory:
    """Manages workflow execution history."""

    def __init__(self, base_dir: str = None):
        """Initialize workflow history manager."""
        if base_dir is None:
            self.base_dir = Path(__file__).parent.parent
        else:
            self.base_dir = Path(base_dir)

        self.history_dir = self.base_dir / "workflows" / "history"
        self.history_dir.mkdir(parents=True, exist_ok=True)

        self.current_executions: Dict[str, WorkflowExecution] = {}

    def start_execution(self, workflow_name: str, workflow_version: str,
                       task_description: str, project_path: Optional[str] = None) -> str:
        """Start tracking a new workflow execution."""
        execution_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        execution = WorkflowExecution(
            execution_id=execution_id,
            workflow_name=workflow_name,
            workflow_version=workflow_version,
            task_description=task_description,
            status=WorkflowStatus.RUNNING.value,
            start_time=datetime.now().isoformat(),
            project_path=project_path
        )

        self.current_executions[execution_id] = execution
        return execution_id

    def start_step(self, execution_id: str, step_id: str, step_name: str, agent: str):
        """Start tracking a workflow step."""
        if execution_id not in self.current_executions:
            return

        step = StepExecution(
            step_id=step_id,
            step_name=step_name,
            agent=agent,
            status=StepStatus.RUNNING.value,
            start_time=datetime.now().isoformat()
        )

        self.current_executions[execution_id].steps.append(step)
        self.current_executions[execution_id].total_steps += 1

    def complete_step(self, execution_id: str, step_id: str,
                     outputs: List[str] = None, validation_passed: bool = True,
                     validation_errors: List[str] = None):
        """Mark a step as completed."""
        if execution_id not in self.current_executions:
            return

        execution = self.current_executions[execution_id]

        # Find the step
        for step in execution.steps:
            if step.step_id == step_id:
                step.status = StepStatus.COMPLETED.value
                step.end_time = datetime.now().isoformat()

                # Calculate duration
                start = datetime.fromisoformat(step.start_time)
                end = datetime.fromisoformat(step.end_time)
                step.duration = (end - start).total_seconds()

                if outputs:
                    step.outputs = outputs
                    execution.outputs_generated.extend(outputs)

                step.validation_passed = validation_passed
                if validation_errors:
                    step.validation_errors = validation_errors

                execution.completed_steps += 1
                break

    def fail_step(self, execution_id: str, step_id: str, error_message: str):
        """Mark a step as failed."""
        if execution_id not in self.current_executions:
            return

        execution = self.current_executions[execution_id]

        # Find the step
        for step in execution.steps:
            if step.step_id == step_id:
                step.status = StepStatus.FAILED.value
                step.end_time = datetime.now().isoformat()
                step.error_message = error_message

                # Calculate duration
                start = datetime.fromisoformat(step.start_time)
                end = datetime.fromisoformat(step.end_time)
                step.duration = (end - start).total_seconds()

                execution.failed_steps += 1
                break

    def skip_step(self, execution_id: str, step_id: str, reason: str = "Optional step"):
        """Mark a step as skipped."""
        if execution_id not in self.current_executions:
            return

        execution = self.current_executions[execution_id]

        # Find the step (or add if not exists)
        found = False
        for step in execution.steps:
            if step.step_id == step_id:
                step.status = StepStatus.SKIPPED.value
                step.error_message = reason
                found = True
                break

        if found:
            execution.skipped_steps += 1

    def record_quality_gate(self, execution_id: str, gate_name: str, passed: bool):
        """Record quality gate result."""
        if execution_id not in self.current_executions:
            return

        execution = self.current_executions[execution_id]

        if passed:
            execution.quality_gates_passed.append(gate_name)
        else:
            execution.quality_gates_failed.append(gate_name)

    def record_user_intervention(self, execution_id: str):
        """Record that user intervened in workflow."""
        if execution_id not in self.current_executions:
            return

        self.current_executions[execution_id].user_interventions += 1

    def complete_execution(self, execution_id: str, success: bool = True):
        """Complete a workflow execution."""
        if execution_id not in self.current_executions:
            return

        execution = self.current_executions[execution_id]
        execution.end_time = datetime.now().isoformat()

        # Calculate duration
        start = datetime.fromisoformat(execution.start_time)
        end = datetime.fromisoformat(execution.end_time)
        execution.duration = (end - start).total_seconds()

        # Determine status
        if success and execution.failed_steps == 0:
            execution.status = WorkflowStatus.COMPLETED.value
        elif execution.failed_steps > 0 and execution.completed_steps > 0:
            execution.status = WorkflowStatus.PARTIAL.value
        else:
            execution.status = WorkflowStatus.FAILED.value

        # Save to file
        self._save_execution(execution)

        # Remove from current executions
        del self.current_executions[execution_id]

    def _save_execution(self, execution: WorkflowExecution):
        """Save execution to history file."""
        # Create filename with date and workflow name
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_str}_{execution.workflow_name}_{execution.execution_id}.json"
        filepath = self.history_dir / filename

        # Convert to dict
        execution_dict = asdict(execution)

        # Save as JSON
        try:
            with open(filepath, 'w') as f:
                json.dump(execution_dict, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving execution history: {e}")

    def get_execution_history(self, workflow_name: Optional[str] = None,
                             limit: int = 100) -> List[WorkflowExecution]:
        """Get execution history."""
        history = []

        # Get all history files
        files = sorted(self.history_dir.glob("*.json"), reverse=True)

        for filepath in files[:limit]:
            if workflow_name and workflow_name not in filepath.name:
                continue

            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    execution = WorkflowExecution(**data)

                    # Convert step dicts back to StepExecution objects
                    execution.steps = [StepExecution(**step) for step in data['steps']]

                    history.append(execution)
            except Exception as e:
                print(f"⚠️  Error loading {filepath.name}: {e}")

        return history

    def get_workflow_statistics(self, workflow_name: str) -> Dict[str, Any]:
        """Get statistics for a specific workflow."""
        history = self.get_execution_history(workflow_name=workflow_name)

        if not history:
            return {
                'workflow_name': workflow_name,
                'total_executions': 0,
                'success_rate': 0.0,
                'avg_duration': 0.0,
                'total_duration': 0.0
            }

        total = len(history)
        completed = sum(1 for e in history if e.status == WorkflowStatus.COMPLETED.value)
        partial = sum(1 for e in history if e.status == WorkflowStatus.PARTIAL.value)
        failed = sum(1 for e in history if e.status == WorkflowStatus.FAILED.value)

        total_duration = sum(e.duration for e in history)
        avg_duration = total_duration / total if total > 0 else 0.0

        # Step statistics
        all_steps = []
        for execution in history:
            all_steps.extend(execution.steps)

        step_stats = {}
        for step in all_steps:
            if step.step_id not in step_stats:
                step_stats[step.step_id] = {
                    'step_name': step.step_name,
                    'agent': step.agent,
                    'total_executions': 0,
                    'completed': 0,
                    'failed': 0,
                    'skipped': 0,
                    'avg_duration': 0.0,
                    'total_duration': 0.0
                }

            stats = step_stats[step.step_id]
            stats['total_executions'] += 1

            if step.status == StepStatus.COMPLETED.value:
                stats['completed'] += 1
            elif step.status == StepStatus.FAILED.value:
                stats['failed'] += 1
            elif step.status == StepStatus.SKIPPED.value:
                stats['skipped'] += 1

            if step.duration > 0:
                stats['total_duration'] += step.duration

        # Calculate averages
        for step_id, stats in step_stats.items():
            if stats['completed'] > 0:
                stats['avg_duration'] = stats['total_duration'] / stats['completed']
            stats['success_rate'] = stats['completed'] / stats['total_executions'] if stats['total_executions'] > 0 else 0.0

        return {
            'workflow_name': workflow_name,
            'total_executions': total,
            'completed': completed,
            'partial': partial,
            'failed': failed,
            'success_rate': completed / total if total > 0 else 0.0,
            'avg_duration': avg_duration,
            'total_duration': total_duration,
            'step_statistics': step_stats,
            'last_execution': history[0].start_time if history else None
        }

    def get_global_statistics(self) -> Dict[str, Any]:
        """Get global workflow system statistics."""
        all_history = self.get_execution_history()

        if not all_history:
            return {
                'total_executions': 0,
                'workflows_used': 0,
                'success_rate': 0.0,
                'avg_duration': 0.0
            }

        # Group by workflow
        by_workflow = {}
        for execution in all_history:
            name = execution.workflow_name
            if name not in by_workflow:
                by_workflow[name] = []
            by_workflow[name].append(execution)

        total = len(all_history)
        completed = sum(1 for e in all_history if e.status == WorkflowStatus.COMPLETED.value)

        total_duration = sum(e.duration for e in all_history)
        avg_duration = total_duration / total if total > 0 else 0.0

        # Most used workflows
        most_used = sorted(
            [(name, len(execs)) for name, execs in by_workflow.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return {
            'total_executions': total,
            'workflows_used': len(by_workflow),
            'success_rate': completed / total if total > 0 else 0.0,
            'avg_duration': avg_duration,
            'total_duration': total_duration,
            'most_used_workflows': most_used,
            'by_workflow': {name: len(execs) for name, execs in by_workflow.items()}
        }


def format_duration(seconds: float) -> str:
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
    history = WorkflowHistory()

    # Start execution
    exec_id = history.start_execution(
        workflow_name="web-app-development",
        workflow_version="1.0.0",
        task_description="Build a weather app"
    )

    # Execute steps
    history.start_step(exec_id, "design", "Create Design", "designer")
    history.complete_step(exec_id, "design", outputs=["DESIGN.md"])

    history.start_step(exec_id, "implement", "Implement App", "code_writer")
    history.complete_step(exec_id, "implement", outputs=["index.html"])

    # Complete execution
    history.complete_execution(exec_id, success=True)

    # Get statistics
    stats = history.get_workflow_statistics("web-app-development")
    print(json.dumps(stats, indent=2))
