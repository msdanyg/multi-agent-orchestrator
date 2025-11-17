# Multi-Agent Orchestrator - Deployment Guide

**Complete setup instructions for deploying the multi-agent system to any project or device**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Installation](#quick-installation)
3. [Detailed Setup Steps](#detailed-setup-steps)
4. [Project-Specific Configuration](#project-specific-configuration)
5. [Custom Agent Creation](#custom-agent-creation)
6. [Integration with Claude Agent SDK](#integration-with-claude-agent-sdk)
7. [Testing Your Setup](#testing-your-setup)
8. [Troubleshooting](#troubleshooting)
9. [Production Deployment](#production-deployment)

---

## Prerequisites

### Required Software

- **Python 3.10+** - Check version: `python3 --version`
- **TMUX** - Terminal multiplexer for agent isolation
- **Git** (optional) - For version control
- **Claude API Key** - From Anthropic (for full integration)

### System Requirements

- **OS**: macOS, Linux, or WSL2 on Windows
- **RAM**: Minimum 4GB (8GB+ recommended)
- **Disk Space**: 500MB for framework + workspace

### Check Your Environment

```bash
# Check Python version
python3 --version  # Should be 3.10+

# Check TMUX
tmux -V  # Should display version

# Check pip
pip3 --version
```

---

## Quick Installation

### 1. Copy Framework to Target Location

```bash
# Option A: Copy from source location
cp -r /path/to/Multi-agent /path/to/target/project-name

# Option B: Clone if in git
git clone <repository-url> /path/to/target/project-name

# Navigate to project
cd /path/to/target/project-name
```

### 2. Run Automated Setup

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup (installs dependencies, creates directories)
./setup.sh
```

### 3. Configure Environment

```bash
# Edit .env file
nano .env

# Add your API key
ANTHROPIC_API_KEY=your_api_key_here
```

### 4. Verify Installation

```bash
# Check system status
python3 main.py status

# List available agents
python3 main.py agents

# Run tests
python3 test_framework.py
```

---

## Detailed Setup Steps

### Step 1: Install TMUX (if needed)

**macOS:**
```bash
brew install tmux
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tmux
```

**Fedora/RHEL:**
```bash
sudo dnf install tmux
```

**Verify:**
```bash
tmux -V
# Should output: tmux 3.x
```

### Step 2: Create Project Directory Structure

```bash
# Navigate to where you want the orchestrator
cd /path/to/your/project

# Create directory (choose a meaningful name)
mkdir my-project-agents
cd my-project-agents

# Copy framework files
cp -r /path/to/Multi-agent/* .

# Or create from scratch with structure:
mkdir -p {agents,specialists,workspace/shared,logs,config}
```

### Step 3: Set Up Python Environment

**Option A: Virtual Environment (Recommended)**

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Upgrade pip
pip install --upgrade pip
```

**Option B: System-Wide (Not Recommended)**

```bash
# Install globally (requires sudo on some systems)
pip3 install --user -r requirements.txt
```

### Step 4: Install Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Or install individually
pip install python-dotenv rich

# For production (optional)
pip install anthropic  # Claude SDK (when ready for integration)
```

### Step 5: Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit with your settings
nano .env  # or vim, code, etc.
```

**Required Variables:**
```bash
# Anthropic API Configuration
ANTHROPIC_API_KEY=sk-ant-api03-...

# Model Configuration (optional, has defaults)
ORCHESTRATOR_MODEL=claude-opus-4
WORKER_MODEL=claude-sonnet-4-5
SIMPLE_MODEL=claude-haiku-4

# System Configuration
PROJECT_ROOT=/absolute/path/to/your/project
MAX_PARALLEL_AGENTS=5
AGENT_TIMEOUT=600

# Logging
LOG_LEVEL=INFO
```

### Step 6: Initialize Agent Registry

```bash
# Initialize default agents
python3 -c "
from agents import AgentRegistry
registry = AgentRegistry('agents/registry.json')
print(f'Initialized with {len(registry.agents)} agents')
"
```

### Step 7: Test Installation

```bash
# Run test suite
python3 test_framework.py

# Should show:
# ✅ 5/5 tests passing
```

---

## Project-Specific Configuration

### Customize for Your Project

#### 1. Update Project Root

Edit `.env`:
```bash
PROJECT_ROOT=/Users/yourname/your-specific-project
```

#### 2. Configure Working Directory

```bash
# Edit main.py or create config file
# Point workspace to your project location
WORKSPACE_DIR=/path/to/your/project/agent-workspace
```

#### 3. Set Project-Specific Tools

Create `config/project_config.json`:
```json
{
  "project_name": "My Awesome Project",
  "project_type": "web_application",
  "primary_language": "python",
  "framework": "django",
  "default_agents": ["code_writer", "tester", "devops"],
  "file_patterns": {
    "source": "src/**/*.py",
    "tests": "tests/**/*.py",
    "docs": "docs/**/*.md"
  }
}
```

#### 4. Customize Agent Registry for Your Stack

Edit `agents/registry.py` or add to your project:

```python
# Add project-specific agent
from agents import AgentRegistry, AgentDefinition

registry = AgentRegistry()

# Example: Django specialist
django_agent = AgentDefinition(
    name="django_expert",
    description="Django web framework specialist",
    role="Develops Django applications with best practices",
    tools=["Read", "Write", "Edit", "Bash"],
    capabilities=[
        "django", "python", "web_development",
        "orm", "views", "templates", "rest_api"
    ],
    system_prompt="""You are a Django expert specializing in:
- Django models and ORM
- Views and URL routing
- Django REST Framework
- Template rendering
- Authentication and permissions
- Database migrations
- Best practices and security

Always follow Django conventions and write clean, maintainable code.""",
    model="claude-sonnet-4-5"
)

registry.register_agent(django_agent)
registry.save_registry()
```

---

## Custom Agent Creation

### Creating Agents for Your Domain

#### Template for Custom Agent

Create `specialists/my_custom_agent.py`:

```python
from agents import AgentRegistry, AgentDefinition

def create_custom_agent():
    """Create a custom agent for your specific needs"""

    agent = AgentDefinition(
        name="my_specialist",
        description="Brief description of what this agent does",
        role="Specific role in your project",
        tools=[
            "Read",      # Read files
            "Write",     # Create new files
            "Edit",      # Modify existing files
            "Bash",      # Execute commands
            "Grep",      # Search code
            "Glob",      # Find files
            "WebSearch", # Research online
        ],
        capabilities=[
            "domain_1",
            "domain_2",
            "skill_1",
            "technology_1"
        ],
        system_prompt="""You are a specialist in [DOMAIN].

Your expertise includes:
- Specific skill 1
- Specific skill 2
- Specific skill 3

Best practices:
- Practice 1
- Practice 2

Always focus on [SPECIFIC GOAL].""",
        model="claude-sonnet-4-5"  # or opus/haiku
    )

    return agent

if __name__ == "__main__":
    registry = AgentRegistry()
    agent = create_custom_agent()
    registry.register_agent(agent)
    print(f"✅ Registered {agent.name}")
```

#### Register Your Custom Agent

```bash
# Run your custom agent script
python3 specialists/my_custom_agent.py

# Verify registration
python3 main.py agents | grep my_specialist
```

### Domain-Specific Examples

**Example 1: React/TypeScript Specialist**

```python
react_agent = AgentDefinition(
    name="react_typescript_dev",
    description="React and TypeScript specialist for frontend development",
    role="Develops React components with TypeScript",
    tools=["Read", "Write", "Edit", "Bash"],
    capabilities=[
        "react", "typescript", "javascript", "jsx", "tsx",
        "hooks", "components", "state_management", "frontend"
    ],
    system_prompt="""You are a React + TypeScript specialist.

Expertise:
- Functional components with hooks
- TypeScript type safety
- Component composition
- State management (Context, Redux)
- React best practices
- Performance optimization

Always use:
- Proper TypeScript interfaces
- React.FC or explicit typing
- Meaningful prop names
- Component composition over inheritance""",
    model="claude-sonnet-4-5"
)
```

**Example 2: Database Specialist**

```python
database_agent = AgentDefinition(
    name="database_architect",
    description="Database design and optimization specialist",
    role="Designs schemas, writes queries, optimizes performance",
    tools=["Read", "Write", "Bash"],
    capabilities=[
        "postgresql", "mysql", "mongodb", "sql",
        "schema_design", "query_optimization", "indexing",
        "migrations", "database_performance"
    ],
    system_prompt="""You are a database architecture specialist.

Expertise:
- Schema design and normalization
- Query optimization
- Index strategy
- Performance tuning
- Migration planning
- Data integrity

Best practices:
- Always use transactions for critical operations
- Index frequently queried columns
- Avoid N+1 queries
- Use appropriate data types
- Document schema decisions""",
    model="claude-sonnet-4-5"
)
```

**Example 3: API Specialist**

```python
api_agent = AgentDefinition(
    name="api_developer",
    description="RESTful API design and implementation specialist",
    role="Develops clean, well-documented APIs",
    tools=["Read", "Write", "Edit", "Bash"],
    capabilities=[
        "rest_api", "api_design", "openapi", "swagger",
        "http", "json", "authentication", "rate_limiting"
    ],
    system_prompt="""You are a REST API specialist.

Expertise:
- RESTful design principles
- OpenAPI/Swagger documentation
- Authentication (JWT, OAuth)
- Error handling and status codes
- Rate limiting and pagination
- API versioning
- Security best practices

Guidelines:
- Use proper HTTP methods (GET, POST, PUT, DELETE)
- Return appropriate status codes
- Include comprehensive error messages
- Document all endpoints
- Implement proper authentication""",
    model="claude-sonnet-4-5"
)
```

---

## Integration with Claude Agent SDK

### Full Production Integration

#### Step 1: Install Claude Agent SDK

```bash
# Activate virtual environment
source venv/bin/activate

# Install SDK
pip install claude-agent-sdk

# Verify installation
python3 -c "import claude_agent_sdk; print('SDK installed')"
```

#### Step 2: Modify Orchestrator for Real Execution

Edit `agents/orchestrator.py` in the `_execute_single_agent` method:

**Find this section (around line 250):**

```python
# In real implementation, this would integrate with Claude Agent SDK
# For now, we'll simulate the execution
print(f"    📦 TMUX Session: {session_id}")
# ... simulation code ...
```

**Replace with:**

```python
from claude_agent_sdk import query, ClaudeAgentOptions

# Configure agent options
options = ClaudeAgentOptions(
    allowed_tools=agent.tools,
    system_prompt=agent.system_prompt,
    model=agent.model,
    cwd=str(agent_workspace),
    permission_mode='default'  # or 'acceptEdits' for auto-approval
)

# Execute with Claude Agent SDK
print(f"    📦 TMUX Session: {session_id}")
print(f"    🤖 Executing with Claude Agent SDK...")

token_usage = 0
cost = 0.0

try:
    async for message in query(prompt=prompt, options=options):
        # Handle different message types
        if hasattr(message, 'type'):
            if message.type == 'text':
                print(f"    📝 {message.content[:100]}...")
            elif message.type == 'tool_use':
                print(f"    🔧 Using tool: {message.tool_name}")

        # Track final result
        if hasattr(message, 'usage'):
            token_usage = message.usage.get('total_tokens', 0)

        if hasattr(message, 'cost'):
            cost = message.cost

    result['success'] = True
    result['output'] = "Task completed successfully"
    result['tokens'] = token_usage
    result['cost'] = cost

except Exception as e:
    result['success'] = False
    result['error'] = str(e)
    print(f"    ❌ SDK Error: {e}")
```

#### Step 3: Update Result Recording

In `_record_outcomes` method, use actual token/cost data:

```python
outcome = TaskOutcome(
    task_id=task_id,
    agent_name=agent_name,
    task_description=task_description,
    task_type=analysis.task_type,
    success=agent_result.get('success', False),
    execution_time=agent_result.get('execution_time', 0),
    tokens_used=agent_result.get('tokens', 0),  # Real data
    cost=agent_result.get('cost', 0.0),         # Real data
    error_message=agent_result.get('error'),
    prompt_used=prompt,                         # Store actual prompt
    timestamp=datetime.now().isoformat()
)
```

#### Step 4: Test SDK Integration

```bash
# Test with real API call
python3 main.py task "Analyze the README.md file structure" --max-agents 1

# Monitor token usage
python3 main.py report
cat logs/system_report.md
```

---

## Testing Your Setup

### Verification Checklist

```bash
# 1. Test framework components
python3 test_framework.py
# Expected: ✅ 5/5 tests passing

# 2. Check system status
python3 main.py status
# Expected: Shows agent registry, tmux stats

# 3. List agents
python3 main.py agents
# Expected: Shows 6 default agents + any custom ones

# 4. Test TMUX functionality
tmux new-session -d -s test-123
tmux has-session -t test-123 && echo "✅ TMUX working"
tmux kill-session -t test-123

# 5. Test simple task execution
python3 main.py task "List files in current directory" --no-tmux

# 6. Run examples
python3 examples.py
# Select example 5 for system status

# 7. Generate report
python3 main.py report
cat logs/system_report.md
```

### Test Custom Agent

```python
# test_custom_agent.py
import asyncio
from agents import Orchestrator

async def test():
    orchestrator = Orchestrator()

    # Test task that should trigger your custom agent
    result = await orchestrator.execute_task(
        "Test task for custom agent functionality",
        max_agents=1
    )

    print(f"Success: {result['success']}")
    print(f"Agents: {result['agents_used']}")

asyncio.run(test())
```

---

## Troubleshooting

### Common Issues & Solutions

#### Issue: "No module named 'dotenv'"

```bash
# Solution: Install python-dotenv
pip install python-dotenv

# Or make it optional (already done in main.py)
```

#### Issue: "TMUX not found"

```bash
# macOS
brew install tmux

# Ubuntu/Debian
sudo apt-get install tmux

# Verify
tmux -V
```

#### Issue: "Permission denied" on setup.sh

```bash
# Solution: Make executable
chmod +x setup.sh
./setup.sh
```

#### Issue: "ModuleNotFoundError: agents"

```bash
# Ensure you're in the correct directory
cd /path/to/Multi-agent

# Check agents/__init__.py exists
ls agents/__init__.py

# Verify Python path
python3 -c "import sys; print(sys.path)"
```

#### Issue: "API Key not working"

```bash
# Check .env file
cat .env | grep ANTHROPIC_API_KEY

# Verify key format (should start with sk-ant-)
echo $ANTHROPIC_API_KEY

# Test API key
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
print(f'Key loaded: {bool(os.getenv(\"ANTHROPIC_API_KEY\"))}')
"
```

#### Issue: TMUX sessions accumulating

```bash
# List all sessions
tmux ls

# Kill specific session
tmux kill-session -t session-name

# Kill all sessions
tmux kill-server

# Or use cleanup
python3 -c "
from agents import TmuxManager
tm = TmuxManager()
cleaned = tm.cleanup_old_sessions(max_age_hours=1)
print(f'Cleaned {cleaned} sessions')
"
```

#### Issue: Tests failing

```bash
# Run tests with verbose output
python3 test_framework.py -v

# Test individual components
python3 -c "
from agents import AgentRegistry
registry = AgentRegistry('agents/test_registry.json')
print(f'Agents: {len(registry.agents)}')
"
```

---

## Production Deployment

### Production Checklist

#### 1. Security Configuration

```bash
# .env for production
ANTHROPIC_API_KEY=your_production_key
LOG_LEVEL=WARNING  # Less verbose
MAX_PARALLEL_AGENTS=10  # Scale up
AGENT_TIMEOUT=1800  # 30 minutes
```

**Set proper permissions:**
```bash
chmod 600 .env  # Only owner can read
chmod 755 *.py  # Executable scripts
chmod 700 workspace/  # Private workspace
```

#### 2. Service Configuration

Create systemd service (`/etc/systemd/system/multi-agent.service`):

```ini
[Unit]
Description=Multi-Agent Orchestrator
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/opt/multi-agent
Environment="PATH=/opt/multi-agent/venv/bin"
ExecStart=/opt/multi-agent/venv/bin/python3 main.py task "${TASK_DESCRIPTION}"
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable multi-agent
sudo systemctl start multi-agent
sudo systemctl status multi-agent
```

#### 3. Logging Configuration

Create `config/logging.conf`:

```ini
[loggers]
keys=root,agents

[handlers]
keys=fileHandler,consoleHandler

[formatters]
keys=detailed

[logger_root]
level=INFO
handlers=fileHandler,consoleHandler

[logger_agents]
level=INFO
handlers=fileHandler
qualname=agents
propagate=0

[handler_fileHandler]
class=FileHandler
level=INFO
formatter=detailed
args=('logs/orchestrator.log', 'a')

[handler_consoleHandler]
class=StreamHandler
level=WARNING
formatter=detailed
args=(sys.stdout,)

[formatter_detailed]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```

#### 4. Monitoring Setup

Create monitoring script (`scripts/monitor.sh`):

```bash
#!/bin/bash

# Monitor multi-agent system
LOGFILE="logs/monitor.log"

while true; do
    echo "=== $(date) ===" >> $LOGFILE

    # Check active sessions
    python3 -c "
from agents import TmuxManager
tm = TmuxManager()
active = len(tm.get_active_sessions())
print(f'Active sessions: {active}')
" >> $LOGFILE

    # Check disk space
    df -h workspace/ >> $LOGFILE

    # Check memory
    free -h >> $LOGFILE

    # Sleep 5 minutes
    sleep 300
done
```

#### 5. Backup Strategy

```bash
# Create backup script
cat > scripts/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/multi-agent"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup registry and skills
tar -czf $BACKUP_DIR/agents_$DATE.tar.gz \
    agents/registry.json \
    agents/skills_history.json \
    config/

# Backup recent logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz \
    logs/

# Keep only last 7 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
EOF

chmod +x scripts/backup.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /path/to/multi-agent/scripts/backup.sh") | crontab -
```

#### 6. Performance Optimization

**Enable caching:**
```bash
# Add to .env
ENABLE_PROMPT_CACHING=true
CACHE_DIRECTORY=/var/cache/multi-agent
```

**Optimize TMUX:**
```bash
# Create ~/.tmux.conf
set -g history-limit 10000
set -g status-interval 60
set -g automatic-rename off
```

#### 7. Health Checks

Create `scripts/healthcheck.py`:

```python
#!/usr/bin/env python3
import sys
from agents import Orchestrator, TmuxManager

def health_check():
    """Check system health"""
    issues = []

    # Check orchestrator
    try:
        orch = Orchestrator()
        status = orch.get_system_status()
        if status['registry']['total_agents'] < 5:
            issues.append("Low agent count")
    except Exception as e:
        issues.append(f"Orchestrator error: {e}")

    # Check TMUX
    try:
        tm = TmuxManager()
        if not tm.check_tmux_installed():
            issues.append("TMUX not available")
    except Exception as e:
        issues.append(f"TMUX error: {e}")

    # Report
    if issues:
        print(f"❌ Health check FAILED:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ Health check PASSED")
        return True

if __name__ == "__main__":
    success = health_check()
    sys.exit(0 if success else 1)
```

Run periodically:
```bash
*/15 * * * * /path/to/multi-agent/venv/bin/python3 /path/to/multi-agent/scripts/healthcheck.py
```

---

## Quick Reference Commands

### Daily Operations

```bash
# Start work
cd /path/to/multi-agent
source venv/bin/activate  # If using venv

# Execute task
python3 main.py task "Your task description"

# Check status
python3 main.py status

# Generate report
python3 main.py report

# View sessions
tmux ls

# Attach to session
tmux attach -t session-name
```

### Maintenance

```bash
# Cleanup old sessions
python3 -c "from agents import TmuxManager; TmuxManager().cleanup_old_sessions()"

# View logs
tail -f logs/orchestrator.log

# Check disk usage
du -sh workspace/

# Backup data
./scripts/backup.sh
```

### Agent Management

```bash
# List agents
python3 main.py agents

# Add custom agent
python3 specialists/my_agent.py

# Test agent
python3 test_framework.py
```

---

## Summary

### Installation Steps:
1. ✅ Install TMUX
2. ✅ Copy framework files
3. ✅ Set up Python environment
4. ✅ Install dependencies
5. ✅ Configure .env
6. ✅ Initialize agents
7. ✅ Test installation

### Customization Steps:
1. ✅ Configure for your project
2. ✅ Create custom agents
3. ✅ Set up task patterns
4. ✅ Test custom configuration

### Production Steps:
1. ✅ Integrate Claude SDK
2. ✅ Set up monitoring
3. ✅ Configure backups
4. ✅ Enable health checks
5. ✅ Deploy as service

**Your multi-agent orchestrator is now ready to use!** 🎉

For support, see:
- `README.md` - Main documentation
- `QUICKSTART.md` - Quick start guide
- `ARCHITECTURE.md` - System design
- `examples.py` - Usage examples
