"""
Multi-Agent Management Framework
Automatic task delegation and orchestration
Now with native .claude/agents/*.md support!
"""

from .orchestrator import Orchestrator
from .orchestrator_v2 import OrchestratorV2
from .orchestrator_workflow import WorkflowOrchestrator
from .registry import AgentRegistry, AgentDefinition, SkillLevel
from .task_router import TaskRouter, TaskAnalysis, AgentAssignment
from .tmux_manager import TmuxManager
from .skills_system import SkillsSystem, TaskOutcome

__version__ = "2.1.0"
__all__ = [
    "Orchestrator",
    "OrchestratorV2",
    "WorkflowOrchestrator",
    "AgentRegistry",
    "AgentDefinition",
    "SkillLevel",
    "TaskRouter",
    "TaskAnalysis",
    "AgentAssignment",
    "TmuxManager",
    "SkillsSystem",
    "TaskOutcome"
]
