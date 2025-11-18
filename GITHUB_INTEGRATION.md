# GitHub Integration Guide

The Multi-Agent Orchestrator now includes built-in GitHub repository management for all projects, ensuring each project has its own dedicated GitHub repository.

---

## 🎯 Overview

Every project created by the orchestrator can automatically:
- Create a dedicated GitHub repository
- Initialize git with proper ignore files
- Push initial commits
- Manage ongoing updates and commits

---

## 📋 Prerequisites

### 1. Install GitHub CLI

```bash
# macOS
brew install gh

# Linux
sudo apt install gh

# Windows
winget install GitHub.cli
```

### 2. Authenticate with GitHub

```bash
gh auth login
```

Follow the prompts to authenticate with your GitHub account.

### 3. Verify Authentication

```bash
gh auth status
```

You should see: ✓ Logged in to github.com

---

## 🚀 Quick Start

### Option 1: Create New Project with GitHub Repo

When creating a new project, the orchestrator can automatically create a GitHub repository:

```bash
python main.py task "Build a calculator" \\
  --project my-calculator \\
  --create-github
```

This will:
1. Create the project locally
2. Initialize git repository
3. Create GitHub repository
4. Push initial commit
5. Set up remote tracking

### Option 2: Add GitHub to Existing Project

For projects that already exist:

```bash
python system/github_manager.py setup my-calculator \\
  --description "A calculator built with Multi-Agent Orchestrator"
```

---

## 💻 Usage Examples

### Create Public Repository

```bash
python main.py task "Build a web app" \\
  --project my-app \\
  --create-github
```

### Create Private Repository

```bash
python main.py task "Build internal tool" \\
  --project internal-tool \\
  --create-github \\
  --github-private
```

### Manual GitHub Operations

#### Create Repository for Existing Project

```bash
python system/github_manager.py create my-project \\
  --description "Project description" \\
  --private
```

#### Push Changes

```bash
python system/github_manager.py push my-project \\
  --message "Added new features"
```

#### Check Repository Status

```bash
python system/github_manager.py status my-project
```

---

## 🔧 CLI Reference

### Project Creation Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--create-github` | Create GitHub repository | `false` |
| `--github-private` | Make repository private | `false` (public) |
| `--description` | Repository description | Project name |

### GitHub Manager Commands

```bash
# Create repository
python system/github_manager.py create PROJECT_NAME [--description DESC] [--private]

# Push changes
python system/github_manager.py push PROJECT_NAME [--message MSG]

# Check status
python system/github_manager.py status PROJECT_NAME

# Setup existing project
python system/github_manager.py setup PROJECT_NAME [--description DESC] [--private]
```

---

## 📝 Configuration

### GitHub Settings

Copy the example configuration:

```bash
cp config/github.example.json config/github.json
```

Edit `config/github.json`:

```json
{
  "enabled": true,
  "auto_create": false,
  "auto_push": false,
  "default_visibility": "public",
  "commit_messages": {
    "initial": "Initial commit via Multi-Agent Orchestrator",
    "workflow_complete": "Complete {workflow_name} workflow\\n\\n{summary}",
    "agent_update": "Update by {agent_name}"
  }
}
```

### Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `enabled` | boolean | Enable/disable GitHub integration |
| `auto_create` | boolean | Automatically create repos for new projects |
| `auto_push` | boolean | Auto-push after workflow completion |
| `default_visibility` | string | "public" or "private" |
| `commit_messages` | object | Custom commit message templates |

---

## 🔄 Workflow Integration

### Automatic Repository Creation

When a workflow creates a new project, you can enable automatic GitHub repository creation:

1. Set `auto_create: true` in `config/github.json`
2. All new projects automatically get GitHub repos

### Manual Repository Creation

If auto-creation is disabled, create repositories manually:

```bash
python system/github_manager.py setup my-project
```

### Pushing Workflow Results

After a workflow completes, push the results:

```bash
cd projects/my-project
git add .
git commit -m "Complete workflow"
git push
```

Or use the manager:

```bash
python system/github_manager.py push my-project \\
  --message "Complete web-app-development workflow"
```

---

## 📊 Project Structure with GitHub

When a project is created with GitHub integration:

```
my-project/
├── .git/                    # Git repository
├── .gitignore              # Ignore patterns
├── .project/               # Project metadata
│   ├── config.json         # Includes GitHub remote URL
│   └── agent-memory/       # Agent memory (ignored by git)
├── README.md               # Project documentation
├── src/                    # Source code
├── docs/                   # Documentation
└── tests/                  # Test files
```

The `.project/config.json` includes GitHub information:

```json
{
  "name": "my-project",
  "git": {
    "remote": "https://github.com/username/my-project",
    "branch": "main",
    "initialized": true,
    "github_created": true
  }
}
```

---

## 🛠️ Advanced Usage

### Custom Commit Messages

```python
from system.github_manager import GitHubManager
from pathlib import Path

manager = GitHubManager()
project_path = Path("projects/my-project")

# Custom commit and push
manager.commit_and_push(
    project_path,
    message="Add calculator feature\\n\\nImplemented scientific calculator with history"
)
```

### Check Repository Info

```python
manager = GitHubManager()
project_path = Path("projects/my-project")

info = manager.get_repo_info(project_path)
print(f"Remote: {info['remote']}")
print(f"Branch: {info['branch']}")
```

---

## 🔍 Troubleshooting

### GitHub CLI Not Found

**Error**: `GitHub CLI not installed or not authenticated`

**Solution**:
```bash
brew install gh  # macOS
gh auth login
```

### Repository Already Exists

**Error**: `Failed to create repository: repository already exists`

**Solution**:
- Use a different project name, or
- Delete the existing repository on GitHub first

### Push Failed

**Error**: `Failed to push: fatal: could not read Username`

**Solution**:
```bash
gh auth login
gh auth refresh
```

### No Remote Configured

**Error**: `No git remote configured`

**Solution**:
```bash
python system/github_manager.py setup my-project
```

---

## 🎨 Best Practices

### 1. Repository Naming

- Use kebab-case: `my-awesome-project`
- Keep names descriptive: `todo-app` not `project1`
- Avoid special characters except hyphens

### 2. Visibility

- Use **public** for:
  - Open source projects
  - Portfolio projects
  - Learning demonstrations

- Use **private** for:
  - Client projects
  - Internal tools
  - Work in progress

### 3. Commit Messages

Follow conventional commits:
- `feat: Add calculator functionality`
- `fix: Correct button alignment`
- `docs: Update README`
- `refactor: Simplify calculation logic`

### 4. Repository Management

- Commit after each significant workflow step
- Push regularly to backup work
- Use meaningful branch names
- Add proper README documentation

---

## 🔐 Security Considerations

### API Token Security

- Never commit GitHub tokens to repositories
- Use `gh auth login` for authentication
- Tokens are stored securely by GitHub CLI

### Private Repositories

- Use `--github-private` for sensitive projects
- Review `.gitignore` to exclude secrets
- Never commit `.env` or credential files

### Repository Permissions

- Review collaborator access regularly
- Use branch protection for important branches
- Enable 2FA on your GitHub account

---

## 📈 Future Enhancements

Planned features:

- [ ] Automatic push after workflow completion (configurable)
- [ ] Branch management for different workflow stages
- [ ] Pull request creation for code review
- [ ] GitHub Actions integration
- [ ] Issue creation for failed steps
- [ ] Release management
- [ ] Repository templates customization
- [ ] Team/organization support

---

## 🤝 Integration with Existing Workflows

### Web App Development Workflow

```bash
# Create project with GitHub
python main.py task "Build a todo app" \\
  --project todo-app \\
  --workflow web-app-development \\
  --create-github

# Workflow will:
# 1. Create design specs
# 2. Implement application
# 3. Run QA testing
# 4. Generate documentation
# 5. All tracked in dedicated GitHub repo
```

### Adding GitHub to Completed Projects

```bash
# For projects created without GitHub
python system/github_manager.py setup my-old-project \\
  --description "Migrating to GitHub"

# Push all existing work
cd projects/my-old-project
git push -u origin main
```

---

## 📚 Examples

### Example 1: Calculator Project

```bash
# Create with GitHub
python main.py task "Build a scientific calculator" \\
  --project calc \\
  --create-github \\
  --description "Scientific calculator with history"

# Result:
# ✅ Project created
# ✅ GitHub repo created at: https://github.com/username/calc
# ✅ Initial commit pushed
```

### Example 2: Private Internal Tool

```bash
# Create private repo
python main.py task "Build admin dashboard" \\
  --project admin-dash \\
  --create-github \\
  --github-private \\
  --description "Internal admin dashboard"

# Result:
# ✅ Private repository created
# ✅ Ready for development
```

### Example 3: Adding GitHub Later

```bash
# Setup GitHub for existing project
python system/github_manager.py setup my-project \\
  --description "Adding version control" \\
  --private

# Result:
# ✅ Git initialized
# ✅ GitHub repo created
# ✅ Initial commit pushed
```

---

## 🆘 Support

### Getting Help

```bash
# Project creation help
python main.py --help

# GitHub manager help
python system/github_manager.py --help

# Check GitHub CLI status
gh auth status
```

### Common Commands

```bash
# List all projects
ls projects/

# Check project git status
cd projects/my-project && git status

# View remote URL
cd projects/my-project && git remote -v

# View commit history
cd projects/my-project && git log --oneline
```

---

## 📜 License

GitHub integration is part of the Multi-Agent Orchestrator system.

---

**Generated**: 2025-01-18
**Version**: 1.0.0
**Status**: Production Ready
