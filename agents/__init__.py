"""
Multi-Agent Management Framework
Automatic task delegation and orchestration using Claude Agent SDK and TMUX
"""

from .orchestrator import Orchestrator
from .registry import AgentRegistry, AgentDefinition, SkillLevel
from .task_router import TaskRouter, TaskAnalysis, AgentAssignment
from .tmux_manager import TmuxManager
from .skills_system import SkillsSystem, TaskOutcome

__version__ = "1.0.0"
__all__ = [
    "Orchestrator",
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
