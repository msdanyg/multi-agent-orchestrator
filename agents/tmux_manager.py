"""
TMUX Session Manager
Manages tmux sessions for agent isolation and persistence
"""
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SessionInfo:
    """Information about a tmux session"""
    session_id: str
    agent_name: str
    task_id: str
    created_at: str
    status: str  # active, completed, failed, zombie
    working_dir: str


class TmuxManager:
    """Manages tmux sessions for multi-agent operations"""

    def __init__(self, workspace_dir: str = "workspace"):
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.sessions: Dict[str, SessionInfo] = {}
        self.session_file = self.workspace_dir / "sessions.json"
        self.load_sessions()

    def load_sessions(self):
        """Load session information from disk"""
        if self.session_file.exists():
            with open(self.session_file, 'r') as f:
                data = json.load(f)
                for session_id, session_data in data.items():
                    self.sessions[session_id] = SessionInfo(**session_data)

    def save_sessions(self):
        """Persist session information to disk"""
        data = {sid: vars(info) for sid, info in self.sessions.items()}
        with open(self.session_file, 'w') as f:
            json.dump(data, f, indent=2)

    def create_session(self, agent_name: str, task_id: str, working_dir: Optional[str] = None) -> str:
        """Create a new tmux session for an agent"""
        session_id = f"agent-{agent_name}-{task_id}-{int(time.time())}"
        work_dir = working_dir or str(self.workspace_dir / agent_name)
        Path(work_dir).mkdir(parents=True, exist_ok=True)

        # Create tmux session
        cmd = [
            "tmux", "new-session",
            "-d",  # detached
            "-s", session_id,  # session name
            "-c", work_dir  # working directory
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)

            session_info = SessionInfo(
                session_id=session_id,
                agent_name=agent_name,
                task_id=task_id,
                created_at=datetime.now().isoformat(),
                status="active",
                working_dir=work_dir
            )

            self.sessions[session_id] = session_info
            self.save_sessions()

            return session_id

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to create tmux session: {e.stderr.decode()}")

    def send_command(self, session_id: str, command: str) -> bool:
        """Send a command to a tmux session"""
        if not self.session_exists(session_id):
            return False

        try:
            subprocess.run(
                ["tmux", "send-keys", "-t", session_id, command, "C-m"],
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def capture_output(self, session_id: str, lines: int = 100) -> str:
        """Capture output from a tmux session"""
        if not self.session_exists(session_id):
            return ""

        try:
            result = subprocess.run(
                ["tmux", "capture-pane", "-t", session_id, "-p", "-S", f"-{lines}"],
                check=True,
                capture_output=True,
                text=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""

    def session_exists(self, session_id: str) -> bool:
        """Check if a tmux session exists"""
        try:
            result = subprocess.run(
                ["tmux", "has-session", "-t", session_id],
                capture_output=True
            )
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False

    def list_sessions(self) -> List[SessionInfo]:
        """List all managed sessions"""
        # Update status of all sessions
        for session_id, info in self.sessions.items():
            if not self.session_exists(session_id) and info.status == "active":
                info.status = "zombie"

        self.save_sessions()
        return list(self.sessions.values())

    def get_session_info(self, session_id: str) -> Optional[SessionInfo]:
        """Get information about a specific session"""
        return self.sessions.get(session_id)

    def kill_session(self, session_id: str) -> bool:
        """Terminate a tmux session"""
        try:
            subprocess.run(
                ["tmux", "kill-session", "-t", session_id],
                check=True,
                capture_output=True
            )

            if session_id in self.sessions:
                self.sessions[session_id].status = "completed"
                self.save_sessions()

            return True
        except subprocess.CalledProcessError:
            return False

    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Clean up old completed sessions"""
        now = datetime.now()
        to_remove = []

        for session_id, info in self.sessions.items():
            created = datetime.fromisoformat(info.created_at)
            age_hours = (now - created).total_seconds() / 3600

            if age_hours > max_age_hours and info.status in ["completed", "failed", "zombie"]:
                if self.session_exists(session_id):
                    self.kill_session(session_id)
                to_remove.append(session_id)

        for session_id in to_remove:
            del self.sessions[session_id]

        self.save_sessions()
        return len(to_remove)

    def get_active_sessions(self) -> List[SessionInfo]:
        """Get all currently active sessions"""
        return [info for info in self.sessions.values() if info.status == "active"]

    def attach_session(self, session_id: str) -> bool:
        """Attach to a tmux session (for debugging)"""
        if not self.session_exists(session_id):
            return False

        try:
            subprocess.run(["tmux", "attach-session", "-t", session_id])
            return True
        except subprocess.CalledProcessError:
            return False

    def mark_session_completed(self, session_id: str, success: bool = True):
        """Mark a session as completed or failed"""
        if session_id in self.sessions:
            self.sessions[session_id].status = "completed" if success else "failed"
            self.save_sessions()

    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics about managed sessions"""
        status_counts = {}
        for info in self.sessions.values():
            status_counts[info.status] = status_counts.get(info.status, 0) + 1

        agent_counts = {}
        for info in self.sessions.values():
            agent_counts[info.agent_name] = agent_counts.get(info.agent_name, 0) + 1

        return {
            "total_sessions": len(self.sessions),
            "status_distribution": status_counts,
            "agent_distribution": agent_counts,
            "active_sessions": len(self.get_active_sessions())
        }

    def check_tmux_installed(self) -> bool:
        """Verify tmux is installed"""
        try:
            subprocess.run(["tmux", "-V"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
