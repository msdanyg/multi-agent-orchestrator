#!/usr/bin/env python3
"""
Project Management CLI for Multi-Agent Orchestrator
Manage multiple isolated projects with shared agents
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import shutil

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import GitHub manager
try:
    from system.github_manager import GitHubManager
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False

class ProjectManager:
    """Manage multiple isolated projects"""

    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = root_dir or Path(__file__).parent.parent
        self.projects_dir = self.root_dir / "projects"
        self.templates_dir = self.root_dir / "templates"
        self.shared_knowledge_dir = self.root_dir / "shared-knowledge"

        # Ensure directories exist
        self.projects_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
        self.shared_knowledge_dir.mkdir(exist_ok=True)

        # Initialize GitHub manager if available
        self.github_manager = GitHubManager(root_dir) if GITHUB_AVAILABLE else None

    def create_project(self, name: str, template: str = "web-app",
                      description: str = "", init_git: bool = True,
                      create_github: bool = False, github_private: bool = False) -> bool:
        """Create a new project from template"""

        project_path = self.projects_dir / name

        if project_path.exists():
            print(f"❌ Error: Project '{name}' already exists")
            return False

        print(f"\n📁 Creating project: {name}")
        print(f"├── Template: {template}")

        # Check if template exists
        template_path = self.templates_dir / template
        if not template_path.exists():
            print(f"├── ⚠️  Template '{template}' not found, using default structure")
            template_path = None

        # Create project directory
        project_path.mkdir(parents=True)

        # Copy template if exists
        if template_path:
            print(f"├── Copying template files...")
            self._copy_template(template_path, project_path)
        else:
            print(f"├── Creating default structure...")
            self._create_default_structure(project_path)

        # Create .project directory
        print(f"├── Creating .project/ metadata...")
        project_meta_dir = project_path / ".project"
        project_meta_dir.mkdir(exist_ok=True)

        # Create agent-memory directory
        (project_meta_dir / "agent-memory").mkdir(exist_ok=True)

        # Create project config
        config = {
            "name": name,
            "type": template,
            "created": datetime.now().isoformat(),
            "description": description,
            "version": "0.1.0",
            "git": {
                "remote": None,
                "branch": "main",
                "initialized": False
            },
            "tech_stack": {},
            "agents": {
                "preferences": {},
                "memory_enabled": True
            },
            "shared_knowledge": [],
            "phases_completed": [],
            "status": "initialized"
        }

        config_path = project_meta_dir / "config.json"
        with open(config_path, 'w') as f:
            json.dump(config, indent=2, fp=f)

        print(f"├── Project configuration saved")

        # Initialize git if requested
        if init_git:
            print(f"├── Initializing git repository...")
            if self._init_git(project_path):
                config["git"]["initialized"] = True
                with open(config_path, 'w') as f:
                    json.dump(config, indent=2, fp=f)
                print(f"├── Git repository initialized")

        print(f"└── ✅ Project created successfully!\n")
        print(f"📂 Location: {project_path}")

        # Create GitHub repository if requested
        if create_github and self.github_manager:
            print(f"\n🔄 Creating GitHub repository...")
            success, result = self.github_manager.create_github_repo(
                name, description, github_private, project_path
            )

            if success:
                print(f"✅ GitHub repository created!")
                print(f"🔗 URL: {result}")
            else:
                print(f"⚠️  GitHub repository creation failed: {result}")
                print(f"   You can create it later with: python system/github_manager.py create {name}")

        print(f"\n💡 Next steps:")
        print(f"   cd {project_path}")
        print(f"   python ../../main.py task \"Your task here\"")

        return True

    def _copy_template(self, template_path: Path, project_path: Path):
        """Copy template files to project"""
        for item in template_path.iterdir():
            if item.name in ['.git', '__pycache__', '.DS_Store']:
                continue

            dest = project_path / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

    def _create_default_structure(self, project_path: Path):
        """Create default project structure"""
        # Create standard directories
        (project_path / "src").mkdir()
        (project_path / "tests").mkdir()
        (project_path / "docs").mkdir()

        # Create README.md
        readme_content = f"""# {project_path.name}

## Description

[Add your project description here]

## Setup

```bash
# Add setup instructions
```

## Usage

```bash
# Add usage instructions
```

## Development

This project is managed by the Multi-Agent Orchestrator system.

### Running Tasks

```bash
python ../../main.py task "Your task description"
```

## License

[Add license information]
"""
        with open(project_path / "README.md", 'w') as f:
            f.write(readme_content)

        # Create .gitignore
        gitignore_content = """# Dependencies
node_modules/
venv/
__pycache__/

# Build outputs
dist/
build/
*.pyc

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Project metadata (keep config, ignore logs)
.project/logs/
"""
        with open(project_path / ".gitignore", 'w') as f:
            f.write(gitignore_content)

    def _init_git(self, project_path: Path) -> bool:
        """Initialize git repository"""
        try:
            subprocess.run(
                ["git", "init"],
                cwd=project_path,
                check=True,
                capture_output=True
            )

            # Create initial commit
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

            return True
        except subprocess.CalledProcessError:
            return False

    def list_projects(self, detailed: bool = False) -> List[Dict]:
        """List all projects"""

        if not self.projects_dir.exists():
            print("📂 No projects directory found")
            return []

        projects = []
        for project_dir in sorted(self.projects_dir.iterdir()):
            if not project_dir.is_dir():
                continue

            config_path = project_dir / ".project" / "config.json"
            if config_path.exists():
                with open(config_path) as f:
                    config = json.load(f)
                projects.append(config)
            else:
                # Project without config
                projects.append({
                    "name": project_dir.name,
                    "type": "unknown",
                    "status": "no-config"
                })

        if not projects:
            print("\n📂 No projects found")
            print(f"\n💡 Create a new project:")
            print(f"   python system/project-cli.py create my-project")
            return []

        print(f"\n📂 Projects ({len(projects)}):\n")

        for i, proj in enumerate(projects, 1):
            status_emoji = {
                "initialized": "🆕",
                "in-progress": "🔨",
                "completed": "✅",
                "archived": "📦",
                "no-config": "⚠️"
            }.get(proj.get("status", "unknown"), "❓")

            print(f"{i}. {status_emoji} {proj['name']}")
            print(f"   Type: {proj.get('type', 'unknown')}")

            if detailed:
                print(f"   Created: {proj.get('created', 'unknown')}")
                if proj.get('description'):
                    print(f"   Description: {proj['description']}")
                if proj.get('git', {}).get('remote'):
                    print(f"   Remote: {proj['git']['remote']}")
                phases = proj.get('phases_completed', [])
                if phases:
                    print(f"   Phases: {', '.join(phases)}")

            print()

        return projects

    def get_project_info(self, name: str) -> Optional[Dict]:
        """Get detailed information about a project"""

        project_path = self.projects_dir / name
        if not project_path.exists():
            print(f"❌ Project '{name}' not found")
            return None

        config_path = project_path / ".project" / "config.json"
        if not config_path.exists():
            print(f"❌ Project config not found for '{name}'")
            return None

        with open(config_path) as f:
            config = json.load(f)

        print(f"\n📋 Project: {name}\n")
        print(f"{'─' * 50}")
        print(f"Type:          {config.get('type', 'unknown')}")
        print(f"Status:        {config.get('status', 'unknown')}")
        print(f"Version:       {config.get('version', '0.1.0')}")
        print(f"Created:       {config.get('created', 'unknown')}")

        if config.get('description'):
            print(f"Description:   {config['description']}")

        print(f"\n📁 Location:   {project_path}")

        # Git info
        git = config.get('git', {})
        print(f"\n🔀 Git:")
        print(f"   Initialized: {'✅' if git.get('initialized') else '❌'}")
        if git.get('remote'):
            print(f"   Remote:      {git['remote']}")
        print(f"   Branch:      {git.get('branch', 'main')}")

        # Tech stack
        tech_stack = config.get('tech_stack', {})
        if tech_stack:
            print(f"\n🛠️  Tech Stack:")
            for key, value in tech_stack.items():
                if isinstance(value, list):
                    print(f"   {key}: {', '.join(value)}")
                else:
                    print(f"   {key}: {value}")

        # Phases
        phases = config.get('phases_completed', [])
        if phases:
            print(f"\n✅ Completed Phases:")
            for phase in phases:
                print(f"   - {phase}")

        # Shared knowledge
        shared = config.get('shared_knowledge', [])
        if shared:
            print(f"\n🧠 Shared Knowledge:")
            for item in shared:
                print(f"   - {item}")

        print(f"\n{'─' * 50}\n")

        return config

    def init_git_remote(self, name: str, remote_url: str) -> bool:
        """Initialize GitHub remote for project"""

        project_path = self.projects_dir / name
        if not project_path.exists():
            print(f"❌ Project '{name}' not found")
            return False

        print(f"\n🔀 Initializing GitHub remote for: {name}")
        print(f"├── Remote URL: {remote_url}")

        try:
            # Add remote
            subprocess.run(
                ["git", "remote", "add", "origin", remote_url],
                cwd=project_path,
                check=True,
                capture_output=True
            )
            print(f"├── Remote 'origin' added")

            # Push to remote
            subprocess.run(
                ["git", "push", "-u", "origin", "main"],
                cwd=project_path,
                check=True,
                capture_output=True
            )
            print(f"├── Pushed to remote")

            # Update config
            config_path = project_path / ".project" / "config.json"
            with open(config_path) as f:
                config = json.load(f)

            config["git"]["remote"] = remote_url

            with open(config_path, 'w') as f:
                json.dump(config, indent=2, fp=f)

            print(f"└── ✅ GitHub remote initialized!\n")
            return True

        except subprocess.CalledProcessError as e:
            print(f"└── ❌ Error: {e}")
            return False

    def delete_project(self, name: str, confirm: bool = False) -> bool:
        """Delete a project"""

        project_path = self.projects_dir / name
        if not project_path.exists():
            print(f"❌ Project '{name}' not found")
            return False

        if not confirm:
            response = input(f"⚠️  Delete project '{name}'? This cannot be undone. (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("❌ Cancelled")
                return False

        print(f"\n🗑️  Deleting project: {name}")
        shutil.rmtree(project_path)
        print(f"✅ Project deleted\n")

        return True

def main():
    parser = argparse.ArgumentParser(
        description="Multi-Agent Project Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a new project
  python system/project-cli.py create my-app --template web-app

  # List all projects
  python system/project-cli.py list

  # Get project info
  python system/project-cli.py info my-app

  # Add GitHub remote
  python system/project-cli.py init-git my-app --remote https://github.com/user/my-app.git

  # Delete a project
  python system/project-cli.py delete my-app
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new project')
    create_parser.add_argument('name', help='Project name')
    create_parser.add_argument('--template', '-t', default='web-app',
                              help='Project template (default: web-app)')
    create_parser.add_argument('--description', '-d', default='',
                              help='Project description')
    create_parser.add_argument('--no-git', action='store_true',
                              help='Skip git initialization')

    # List command
    list_parser = subparsers.add_parser('list', help='List all projects')
    list_parser.add_argument('--detailed', '-d', action='store_true',
                            help='Show detailed information')

    # Info command
    info_parser = subparsers.add_parser('info', help='Show project information')
    info_parser.add_argument('name', help='Project name')

    # Init-git command
    git_parser = subparsers.add_parser('init-git', help='Initialize GitHub remote')
    git_parser.add_argument('name', help='Project name')
    git_parser.add_argument('--remote', '-r', required=True,
                           help='GitHub remote URL')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a project')
    delete_parser.add_argument('name', help='Project name')
    delete_parser.add_argument('--yes', '-y', action='store_true',
                              help='Skip confirmation')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    manager = ProjectManager()

    if args.command == 'create':
        manager.create_project(
            args.name,
            template=args.template,
            description=args.description,
            init_git=not args.no_git
        )

    elif args.command == 'list':
        manager.list_projects(detailed=args.detailed)

    elif args.command == 'info':
        manager.get_project_info(args.name)

    elif args.command == 'init-git':
        manager.init_git_remote(args.name, args.remote)

    elif args.command == 'delete':
        manager.delete_project(args.name, confirm=args.yes)

if __name__ == "__main__":
    main()
