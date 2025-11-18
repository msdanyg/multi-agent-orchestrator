#!/usr/bin/env python3
"""
GitHub Repository Manager
Automatically creates and manages GitHub repositories for projects
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, Tuple


class GitHubManager:
    """Manages GitHub repository creation and configuration"""

    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = root_dir or Path(__file__).parent.parent
        self.projects_dir = self.root_dir / "projects"

    def check_gh_cli(self) -> bool:
        """Check if GitHub CLI is installed and authenticated"""
        try:
            result = subprocess.run(
                ["gh", "auth", "status"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def create_github_repo(self, project_name: str, description: str = "",
                          private: bool = False, project_path: Optional[Path] = None) -> Tuple[bool, str]:
        """
        Create a GitHub repository for a project

        Args:
            project_name: Name of the project/repository
            description: Repository description
            private: Whether to create a private repository
            project_path: Path to the project directory

        Returns:
            Tuple of (success: bool, repo_url: str or error_message: str)
        """
        if not self.check_gh_cli():
            return False, "GitHub CLI not installed or not authenticated. Run: gh auth login"

        if project_path is None:
            project_path = self.projects_dir / project_name

        if not project_path.exists():
            return False, f"Project path {project_path} does not exist"

        try:
            # Build gh repo create command
            cmd = [
                "gh", "repo", "create", project_name,
                "--source", str(project_path),
                "--push"
            ]

            if description:
                cmd.extend(["--description", description])

            if private:
                cmd.append("--private")
            else:
                cmd.append("--public")

            # Create the repository
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=project_path
            )

            if result.returncode == 0:
                # Extract repository URL from output
                repo_url = self._get_repo_url(project_name)

                # Update project config
                self._update_project_config(project_path, repo_url)

                return True, repo_url
            else:
                return False, f"Failed to create repository: {result.stderr}"

        except Exception as e:
            return False, f"Error creating GitHub repository: {str(e)}"

    def _get_repo_url(self, repo_name: str) -> str:
        """Get the URL of a repository"""
        try:
            result = subprocess.run(
                ["gh", "repo", "view", repo_name, "--json", "url"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data.get("url", "")
            return ""
        except:
            return ""

    def _update_project_config(self, project_path: Path, repo_url: str):
        """Update project configuration with GitHub repository URL"""
        config_path = project_path / ".project" / "config.json"

        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)

            if "git" not in config:
                config["git"] = {}

            config["git"]["remote"] = repo_url
            config["git"]["github_created"] = True

            with open(config_path, 'w') as f:
                json.dump(config, indent=2, fp=f)

    def push_to_github(self, project_path: Path, branch: str = "main") -> Tuple[bool, str]:
        """
        Push project changes to GitHub

        Args:
            project_path: Path to the project directory
            branch: Branch to push to

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Check if remote exists
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=project_path,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return False, "No git remote configured"

            # Push to GitHub
            result = subprocess.run(
                ["git", "push", "-u", "origin", branch],
                cwd=project_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return True, f"Successfully pushed to {branch}"
            else:
                return False, f"Failed to push: {result.stderr}"

        except Exception as e:
            return False, f"Error pushing to GitHub: {str(e)}"

    def commit_and_push(self, project_path: Path, message: str = None) -> Tuple[bool, str]:
        """
        Commit all changes and push to GitHub

        Args:
            project_path: Path to the project directory
            message: Commit message (auto-generated if not provided)

        Returns:
            Tuple of (success: bool, message: str)
        """
        if message is None:
            message = "Update project via Multi-Agent Orchestrator"

        try:
            # Stage all changes
            subprocess.run(
                ["git", "add", "."],
                cwd=project_path,
                check=True,
                capture_output=True
            )

            # Commit changes
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=project_path,
                capture_output=True,
                text=True
            )

            # If nothing to commit, that's ok
            if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                return True, "No changes to commit"

            if result.returncode != 0:
                return False, f"Failed to commit: {result.stderr}"

            # Push to GitHub
            return self.push_to_github(project_path)

        except subprocess.CalledProcessError as e:
            return False, f"Error committing changes: {str(e)}"

    def get_repo_info(self, project_path: Path) -> Optional[Dict]:
        """Get information about the project's GitHub repository"""
        config_path = project_path / ".project" / "config.json"

        if not config_path.exists():
            return None

        with open(config_path, 'r') as f:
            config = json.load(f)

        return config.get("git", {})

    def setup_repo_for_existing_project(self, project_name: str, description: str = "",
                                       private: bool = False) -> Tuple[bool, str]:
        """
        Set up GitHub repository for an existing project

        Args:
            project_name: Name of the project
            description: Repository description
            private: Whether to create a private repository

        Returns:
            Tuple of (success: bool, repo_url: str or error_message: str)
        """
        project_path = self.projects_dir / project_name

        if not project_path.exists():
            return False, f"Project '{project_name}' does not exist"

        # Check if git is initialized
        git_dir = project_path / ".git"
        if not git_dir.exists():
            # Initialize git
            try:
                subprocess.run(
                    ["git", "init"],
                    cwd=project_path,
                    check=True,
                    capture_output=True
                )
                subprocess.run(
                    ["git", "add", "."],
                    cwd=project_path,
                    check=True,
                    capture_output=True
                )
                subprocess.run(
                    ["git", "commit", "-m", "Initial commit"],
                    cwd=project_path,
                    check=True,
                    capture_output=True
                )
            except subprocess.CalledProcessError as e:
                return False, f"Failed to initialize git: {str(e)}"

        # Create GitHub repository
        return self.create_github_repo(project_name, description, private, project_path)


def main():
    """CLI interface for GitHub management"""
    import argparse

    parser = argparse.ArgumentParser(description="GitHub Repository Manager")
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Create repo command
    create_parser = subparsers.add_parser('create', help='Create GitHub repository for project')
    create_parser.add_argument('project', help='Project name')
    create_parser.add_argument('--description', '-d', default='', help='Repository description')
    create_parser.add_argument('--private', action='store_true', help='Create private repository')

    # Push command
    push_parser = subparsers.add_parser('push', help='Push project to GitHub')
    push_parser.add_argument('project', help='Project name')
    push_parser.add_argument('--message', '-m', help='Commit message')

    # Status command
    status_parser = subparsers.add_parser('status', help='Check GitHub repository status')
    status_parser.add_argument('project', help='Project name')

    # Setup command (for existing projects)
    setup_parser = subparsers.add_parser('setup', help='Setup GitHub repo for existing project')
    setup_parser.add_argument('project', help='Project name')
    setup_parser.add_argument('--description', '-d', default='', help='Repository description')
    setup_parser.add_argument('--private', action='store_true', help='Create private repository')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    manager = GitHubManager()

    if args.command == 'create':
        success, result = manager.create_github_repo(
            args.project,
            args.description,
            args.private
        )

        if success:
            print(f"✅ GitHub repository created successfully!")
            print(f"🔗 URL: {result}")
        else:
            print(f"❌ Failed to create repository: {result}")

    elif args.command == 'push':
        project_path = manager.projects_dir / args.project
        success, message = manager.commit_and_push(project_path, args.message)

        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")

    elif args.command == 'status':
        project_path = manager.projects_dir / args.project
        info = manager.get_repo_info(project_path)

        if info:
            print("\n📊 GitHub Repository Status:")
            print(f"   Remote: {info.get('remote', 'Not configured')}")
            print(f"   Branch: {info.get('branch', 'main')}")
            print(f"   Initialized: {info.get('initialized', False)}")
            print(f"   GitHub Created: {info.get('github_created', False)}")
        else:
            print("❌ No project configuration found")

    elif args.command == 'setup':
        success, result = manager.setup_repo_for_existing_project(
            args.project,
            args.description,
            args.private
        )

        if success:
            print(f"✅ GitHub repository setup successfully!")
            print(f"🔗 URL: {result}")
        else:
            print(f"❌ Failed to setup repository: {result}")


if __name__ == '__main__':
    main()
