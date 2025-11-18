# CLAUDE.md - AI Assistant Development Guide

**Repository:** Multi-Agent Orchestrator
**Purpose:** Intelligent multi-agent system for automated task delegation using Claude AI
**Last Updated:** 2025-11-18

---

## 🎯 Repository Overview

This is the **Multi-Agent Orchestrator Framework** - a sophisticated system that automatically delegates tasks to specialized Claude AI agents using TMUX session management and the Claude Agent SDK. The framework provides:

- **Automatic Task Delegation**: Analyzes tasks and routes to optimal agents
- **Intelligent Agent Selection**: Matches tasks based on capabilities and performance history
- **Parallel Execution**: Executes independent tasks concurrently
- **TMUX Integration**: Isolated, persistent agent sessions with recovery
- **Continuous Learning**: Tracks performance and improves agent selection over time
- **Skill Progression**: Agents level up from Novice → Intermediate → Expert → Master

---

## 📁 Codebase Structure

```
multi-agent-orchestrator/
├── .claude/                          # Agent definitions and skills
│   ├── agents/                       # 12 specialized agent profiles (*.md)
│   │   ├── code_writer.md           # Implementation & bug fixing
│   │   ├── code_analyst.md          # Code review & architecture
│   │   ├── tester.md                # Testing & QA
│   │   ├── researcher.md            # Research & documentation
│   │   ├── designer.md              # UI/UX design
│   │   ├── devops.md                # DevOps & deployment
│   │   ├── security.md              # Security auditing
│   │   ├── api_expert.md            # API development
│   │   ├── database_manager.md      # Database operations
│   │   ├── data_analyst.md          # Data analysis
│   │   ├── docs_writer.md           # Technical writing
│   │   └── qa_tester.md             # Quality assurance
│   └── skills/
│       └── parallel-development.md  # Multi-task patterns
│
├── agents/                           # Core orchestration framework
│   ├── __init__.py                  # Package exports
│   ├── orchestrator.py              # Main coordinator (Claude Opus 4)
│   ├── orchestrator_v2.py           # Enhanced version
│   ├── task_router.py               # Task analysis & agent selection
│   ├── registry.py                  # Agent registry & metrics
│   ├── tmux_manager.py              # TMUX session management
│   ├── skills_system.py             # Learning & performance tracking
│   └── registry.json                # Persisted agent metrics
│
├── workspace/                        # Runtime agent workspaces
│   ├── shared/                      # Shared files between agents
│   └── <agent_name>/                # Per-agent isolated workspace
│
├── logs/                            # System logs and reports
│   ├── system.log                   # Main system logs
│   ├── skills_report.md             # Agent learning insights
│   └── system_report.md             # Performance reports
│
├── system/
│   └── project-cli.py               # Project management CLI
│
├── templates/
│   ├── agent_template.json          # Template for custom agents
│   ├── agent_instructions.md        # Agent creation guide
│   └── web-app/                     # Web app templates
│
├── Root-Level Python Scripts
│   ├── main.py                      # CLI entry point (5.9KB)
│   ├── manage_agents.py             # Agent management tool (17KB)
│   ├── examples.py                  # Usage examples (5.1KB)
│   ├── test_framework.py            # Framework tests (6.3KB)
│   ├── validate_agents.py           # Agent validation (5.6KB)
│   └── test_calculator.py           # Calculator tests (7.7KB)
│
├── Configuration & Setup
│   ├── .env.example                 # Environment template
│   ├── requirements.txt             # Python dependencies
│   ├── install.sh                   # Full installation (506 lines)
│   ├── setup.sh                     # Basic setup
│   ├── publish_to_github.sh         # GitHub publishing
│   └── .gitignore
│
└── Documentation (16,267 lines)
    ├── README.md                    # Main documentation
    ├── ARCHITECTURE.md              # System architecture
    ├── QUICKSTART.md                # Quick start guide
    ├── DEPLOYMENT_GUIDE.md          # Deployment instructions
    ├── AGENT_SYSTEM_GUIDE.md        # Agent system docs
    ├── MULTI_AGENT_WORKFLOW.md      # Workflow patterns
    ├── MULTI_PROJECT_SYSTEM.md      # Multi-project support
    ├── CONTRIBUTING.md              # Contribution guidelines
    └── [20+ more documentation files]
```

---

## 🏗️ Core Components

### 1. **Orchestrator** (`agents/orchestrator.py`)

**Role:** Central coordinator and task planner

- Receives user tasks and decomposes them into subtasks
- Analyzes requirements using the Task Router
- Selects optimal agents from the registry
- Manages workflow and dependencies
- Aggregates results and presents output
- **Model:** Claude Opus 4 (complex reasoning)
- **Key Class:** `Orchestrator`

**Key Methods:**
```python
async def execute_task(task_description: str, max_agents: int = 3, use_tmux: bool = True)
def get_system_status() -> dict
```

### 2. **Task Router** (`agents/task_router.py`)

**Role:** Intelligent task analysis and agent matching

- **40+ task pattern recognition** using regex
- Language detection (Python, JavaScript, TypeScript, Java, Go, Rust)
- Complexity estimation (simple, medium, complex)
- Parallelization potential analysis
- Confidence scoring for agent selection
- **Key Classes:** `TaskRouter`, `TaskAnalysis`, `AgentAssignment`

**Recognized Task Types:**
- `code_analysis` - Code review and architecture
- `implementation` - Feature development
- `bug_fixing` - Debugging and fixes
- `testing` - Test execution and validation
- `research` - Information gathering
- `documentation` - Technical writing
- `deployment` - DevOps operations
- `security_audit` - Security analysis
- `database_operations` - Database work
- `api_development` - API design/implementation

### 3. **Agent Registry** (`agents/registry.py`)

**Role:** Central database of agent capabilities and performance

- Loads agents from `.claude/agents/*.md` files
- Tracks performance metrics (success rate, execution time, token usage, cost)
- Calculates skill levels based on performance
- Persists metrics to `agents/registry.json`
- Supports dynamic agent registration
- **Key Classes:** `AgentRegistry`, `AgentDefinition`, `AgentMetrics`, `SkillLevel`

**Agent Metrics Tracked:**
- Total tasks executed
- Successful/failed task counts
- Token usage and cost
- Average completion time
- Success rate percentage
- Last used timestamp
- Skill level progression

**Skill Progression System:**

| Level | Requirements | Benefits |
|-------|-------------|----------|
| **Novice** | Default starting level | Base capabilities |
| **Intermediate** | 5+ tasks, 75%+ success | 1.2x priority multiplier |
| **Expert** | 20+ tasks, 85%+ success | 1.5x priority multiplier |
| **Master** | 50+ tasks, 90%+ success | 2.0x priority multiplier |

### 4. **TMUX Manager** (`agents/tmux_manager.py`)

**Role:** Session lifecycle management

- Creates isolated TMUX sessions per agent
- Monitors agent status and health
- Handles session recovery on failure
- Enables session persistence across disconnections
- Provides session observation/debugging
- Automatic session cleanup
- **Key Class:** `TmuxManager`

### 5. **Skills System** (`agents/skills_system.py`)

**Role:** Continuous learning and improvement

- Tracks task outcomes (success/failure, execution time, quality)
- Stores successful prompt patterns
- Updates agent skill levels based on performance
- Suggests new agents for recurring task patterns
- Generates performance reports and insights
- Identifies knowledge gaps
- **Key Classes:** `SkillsSystem`, `TaskOutcome`

### 6. **Orchestrator V2** (`agents/orchestrator_v2.py`)

Enhanced version with improved multi-agent coordination and workflow management.

---

## 🔧 Development Workflows

### Standard Task Execution Flow

```
User Task
    ↓
Orchestrator (receives task)
    ↓
Task Router (analyzes requirements)
    ├─ Detects task type (40+ regex patterns)
    ├─ Estimates complexity
    ├─ Identifies parallelization potential
    └─ Extracts required capabilities
    ↓
Agent Registry (selects best agents)
    ├─ Scores agents by capability match
    ├─ Considers performance history
    ├─ Evaluates skill levels
    └─ Returns ranked assignments
    ↓
TMUX Manager (creates isolated sessions)
    ├─ Creates per-agent TMUX session
    ├─ Sets up workspace directory
    └─ Enables session persistence
    ↓
Specialist Agents (execute in parallel/sequential)
    ├─ Primary agents: core task work
    ├─ Supporting agents: validation/testing
    └─ Based on task dependencies
    ↓
Skills System (tracks outcomes)
    ├─ Records success/failure
    ├─ Updates performance metrics
    ├─ Suggests prompt improvements
    └─ Updates skill levels
    ↓
Results Aggregated → User
```

### Multi-Agent Collaboration Pattern

The framework supports iterative improvement workflows:

1. **Code Writer** creates initial implementation
2. **Tester** validates and identifies bugs
3. **Code Writer** returns to fix identified issues
4. **QA Tester** performs final validation
5. **Documentation Writer** creates docs

This pattern is demonstrated in `MULTI_AGENT_WORKFLOW.md` with the Snake Game example.

---

## 💻 Development Conventions

### Code Style (PEP 8)

- Follow PEP 8 for Python code
- Use type hints for function signatures
- Write docstrings for all public functions/classes
- Keep functions focused and small (< 50 lines preferred)
- Use meaningful variable names

**Example:**
```python
async def execute_task(
    self,
    task_description: str,
    max_agents: int = 3,
    use_tmux: bool = True,
    context: Optional[dict] = None
) -> dict:
    """
    Execute a task using the multi-agent system.

    Args:
        task_description: Natural language description of the task
        max_agents: Maximum number of agents to use (default: 3)
        use_tmux: Whether to use TMUX sessions (default: True)
        context: Optional context dictionary

    Returns:
        dict: Execution result with success status, outputs, and metrics
    """
    pass
```

### Commit Message Convention

Use conventional commit format:
- `Add:` for new features
- `Fix:` for bug fixes
- `Update:` for changes to existing features
- `Docs:` for documentation only changes
- `Test:` for test-only changes

**Examples:**
```bash
git commit -m "Add: Multi-project system with workspace isolation"
git commit -m "Fix: Snake game reverse direction bug"
git commit -m "Update: Improve agent selection confidence scoring"
git commit -m "Docs: Add comprehensive CLAUDE.md guide"
git commit -m "Test: Add integration tests for task router"
```

### Testing Requirements

- Add tests for new features using `test_framework.py`
- Ensure all tests pass before submitting changes
- Aim for >80% test coverage
- Test agent definitions with `validate_agents.py`

### Documentation Standards

- Update `README.md` when adding features
- Add docstrings to all new code
- Update relevant guides (DEPLOYMENT_GUIDE.md, ARCHITECTURE.md)
- Document new agents in `.claude/agents/`

---

## 🤖 Agent System Architecture

### Agent Definition Format

Agents are defined in `.claude/agents/*.md` files with YAML frontmatter:

```markdown
---
name: code_writer
description: Implementation and bug fixing specialist
allowed_tools: ["Read", "Write", "Edit", "Glob", "Bash"]
model: claude-sonnet-4-5
---

You are a specialist code writer agent...

[Agent's system prompt and guidelines]
```

### Available Tools for Agents

- `Read` - Read files from filesystem
- `Write` - Write new files
- `Edit` - Edit existing files
- `Glob` - Find files by pattern
- `Grep` - Search file contents
- `Bash` - Execute shell commands
- `WebSearch` - Search the web
- `WebFetch` - Fetch web content
- `Task` - Delegate to subagents

### Creating New Agents

1. **Create definition file**: `.claude/agents/your_agent.md`
2. **Use proper YAML frontmatter**:
   ```yaml
   ---
   name: your_agent_name
   description: Brief description
   allowed_tools: ["Read", "Write", "Grep"]
   model: claude-sonnet-4-5
   ---
   ```
3. **Write clear system prompt** with role, capabilities, and guidelines
4. **Test agent** with `validate_agents.py`
5. **Add to documentation**

### Model Tiering Strategy

The framework uses three model tiers for cost optimization:

- **Claude Opus 4** - Complex reasoning, orchestration (expensive, powerful)
- **Claude Sonnet 4.5** - Standard tasks, most agent work (balanced)
- **Claude Haiku 4** - Simple tasks, data retrieval (fast, cheap)

Configure in `.env`:
```bash
ORCHESTRATOR_MODEL=claude-opus-4
WORKER_MODEL=claude-sonnet-4-5
SIMPLE_MODEL=claude-haiku-4
```

---

## 🧪 Testing & Validation

### Running Tests

```bash
# Run all framework tests
python test_framework.py

# Test calculator functionality
python test_calculator.py

# Validate agent definitions
python validate_agents.py

# Run usage examples
python examples.py
```

### Test Files

- `test_framework.py` - Tests orchestrator, router, registry, TMUX manager, skills system
- `test_calculator.py` - Tests calculator operations and interface
- `validate_agents.py` - Validates agent definition files

### Manual Testing with TMUX

```bash
# List all TMUX sessions
tmux ls

# Attach to agent session
tmux attach -t agent-code_writer-<session-id>

# Detach from session
Ctrl+B, then D

# Kill session
tmux kill-session -t <session-id>
```

---

## ⚙️ Environment & Configuration

### Environment Setup

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Configure `.env` file:**
   ```bash
   # Required: API Key
   ANTHROPIC_API_KEY=your_key_here

   # Model Selection
   ORCHESTRATOR_MODEL=claude-opus-4
   WORKER_MODEL=claude-sonnet-4-5
   SIMPLE_MODEL=claude-haiku-4

   # System Configuration
   PROJECT_ROOT=/path/to/project
   MAX_PARALLEL_AGENTS=5
   AGENT_TIMEOUT=600

   # Logging
   LOG_LEVEL=INFO
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Python Dependencies

From `requirements.txt`:
- `claude-agent-sdk>=0.1.0` - Claude Agent SDK
- `anthropic>=0.40.0` - Anthropic API client
- `python-dotenv>=1.0.0` - Environment configuration
- `pydantic>=2.0.0` - Data validation
- `rich>=13.0.0` - Rich console output
- `PyYAML>=6.0.0` - YAML configuration
- `asyncio` - Async programming

### Prerequisites

- **Python 3.10+**
- **TMUX** - Session manager
- **Claude API Key** - From Anthropic

**Install TMUX:**
```bash
# macOS
brew install tmux

# Ubuntu/Debian
sudo apt-get install tmux

# Fedora
sudo dnf install tmux
```

---

## 📝 Common Commands & Workflows

### CLI Commands (via `main.py`)

```bash
# Execute a task
python main.py task "Refactor authentication module to use JWT"

# Limit number of agents
python main.py task "Fix bugs in payment system" --max-agents 2

# Execute without TMUX (direct execution)
python main.py task "Update documentation" --no-tmux

# Show system status
python main.py status

# List all agents with metrics
python main.py agents

# Generate comprehensive reports
python main.py report

# Custom report location
python main.py report --output custom_report.md
```

### Agent Management (via `manage_agents.py`)

```bash
# Interactive agent management
python manage_agents.py
```

This provides:
- View agent definitions
- Edit agent configurations
- Color-coded console output
- Agent registry browsing

### Programmatic Usage

**Basic Task Execution:**
```python
import asyncio
from agents import Orchestrator

async def main():
    orchestrator = Orchestrator()

    result = await orchestrator.execute_task(
        task_description="Fix memory leak in data processing",
        max_agents=3
    )

    print(f"Success: {result['success']}")
    print(f"Time: {result['execution_time']:.2f}s")

asyncio.run(main())
```

**Parallel Task Execution:**
```python
async def parallel_tasks():
    orchestrator = Orchestrator()

    tasks = [
        orchestrator.execute_task("Review database models"),
        orchestrator.execute_task("Update API documentation"),
        orchestrator.execute_task("Run test suite")
    ]

    results = await asyncio.gather(*tasks)
```

**With Custom Context:**
```python
result = await orchestrator.execute_task(
    task_description="Optimize search algorithm",
    context={
        'files': ['search.py', 'indexer.py'],
        'constraints': 'Maintain O(log n) complexity',
        'previous_results': 'Profiling shows bottleneck in indexing'
    }
)
```

---

## 🎨 File Organization Patterns

### Workspace Directory Structure

Each agent gets an isolated workspace:

```
workspace/
├── shared/                    # Shared files between agents
│   ├── task_context.json     # Task information
│   ├── results.json          # Aggregated results
│   └── artifacts/            # Shared artifacts
│
├── code_writer/              # Code Writer's workspace
│   ├── workspace/            # Working directory
│   ├── output.txt           # Agent output
│   └── session.log          # Session logs
│
├── tester/                   # Tester's workspace
│   ├── workspace/
│   ├── test_results.json
│   └── session.log
│
└── sessions.json             # Active session tracking
```

### Log Directory Structure

```
logs/
├── system.log               # Main system logs
├── skills_report.md         # Agent learning insights
├── system_report.md         # Performance reports
└── agent_<name>.log         # Per-agent logs
```

### Configuration Files

```
.env                         # Environment configuration (gitignored)
.env.example                 # Environment template (committed)
agents/registry.json         # Agent metrics (auto-generated)
agents/skills_history.json   # Skills learning data
```

---

## 🔍 Important Patterns & Best Practices

### 1. Agent Selection Strategy

The system uses multi-factor scoring:

```python
score = (
    capability_match * 0.4 +      # 40% weight: Does agent have required skills?
    success_rate * 0.3 +           # 30% weight: Historical success
    skill_level * 0.2 +            # 20% weight: Experience level
    availability * 0.1             # 10% weight: Current load
)
```

### 2. Task Decomposition

Complex tasks are automatically decomposed:

- **Sequential tasks**: Dependencies between steps
- **Parallel tasks**: Independent operations
- **Iterative tasks**: Repeated refinement (code → test → fix → test)

### 3. Error Handling & Recovery

- **TMUX sessions persist** through disconnections
- **Automatic retry** on transient failures
- **Session recovery** from checkpoints
- **Graceful degradation** when agents unavailable

### 4. Performance Optimization

- **Prompt caching**: Reduces token usage on repeated operations
- **Context compaction**: Automatic summarization for long sessions
- **Model tiering**: Use appropriate model for task complexity
- **Parallel execution**: Independent tasks run simultaneously

### 5. Cost Management

Track costs with built-in metrics:

```python
status = orchestrator.get_system_status()
print(f"Total cost: ${status['registry']['total_cost']:.2f}")
```

**Typical costs:**
- Simple task: $0.01 - $0.05
- Medium task: $0.05 - $0.20
- Complex task: $0.20 - $1.00

---

## 🚀 Installation & Setup

### Quick Installation

```bash
# Clone repository
git clone https://github.com/yourusername/multi-agent-orchestrator.git
cd multi-agent-orchestrator

# Run full installation
bash install.sh

# Configure environment
cp .env.example .env
# Edit .env and add ANTHROPIC_API_KEY

# Verify installation
python main.py status
```

### Installation Types

The `install.sh` script supports three modes:

1. **Full** - Complete installation with all features
   ```bash
   bash install.sh /path/to/target full
   ```

2. **Minimal** - Essential files only
   ```bash
   bash install.sh /path/to/target minimal
   ```

3. **Custom** - Interactive selection
   ```bash
   bash install.sh /path/to/target custom
   ```

---

## 📊 Monitoring & Debugging

### View System Status

```bash
python main.py status
```

Shows:
- Active agents
- Recent tasks
- Performance metrics
- Token usage and costs
- Agent skill levels

### Generate Reports

```bash
python main.py report
```

Generates:
- `logs/system_report.md` - System performance
- `logs/skills_report.md` - Agent learning insights

### View Agent Workspace

```bash
# List agent workspaces
ls -la workspace/

# View specific agent's workspace
ls -la workspace/code_writer/

# View agent output
cat workspace/code_writer/output.txt
```

### Check Logs

```bash
# System logs
tail -f logs/system.log

# Agent-specific logs
tail -f logs/agent_code_writer.log
```

### TMUX Session Management

```bash
# List all sessions
tmux ls

# Attach to session
tmux attach -t agent-code_writer-abc123

# Kill old sessions
tmux kill-session -t <session-id>

# Kill all sessions
tmux kill-server
```

---

## 🐛 Troubleshooting

### Common Issues

**1. TMUX Not Found**
```bash
# Install tmux
brew install tmux  # macOS
sudo apt install tmux  # Ubuntu/Debian
```

**2. API Key Issues**
```bash
# Verify API key is set
echo $ANTHROPIC_API_KEY

# Or check .env file
cat .env
```

**3. Agent Not Found**
```bash
# List available agents
python main.py agents

# Validate agent definitions
python validate_agents.py

# Check registry
cat agents/registry.json
```

**4. Session Cleanup**
```bash
# Kill old sessions
tmux kill-session -t <session-id>

# Kill all sessions
tmux kill-server

# Clean workspace
rm -rf workspace/*/
```

**5. Permission Issues**
```bash
# Make scripts executable
chmod +x install.sh setup.sh publish_to_github.sh
chmod +x main.py examples.py manage_agents.py
```

---

## 🎓 Learning Resources

### Documentation Files to Read

1. **Start here:**
   - `README.md` - Overview and quick start
   - `QUICKSTART.md` - Getting started guide

2. **Architecture:**
   - `ARCHITECTURE.md` - System design details
   - `PROJECT_ARCHITECTURE.md` - Project-level architecture

3. **Workflows:**
   - `MULTI_AGENT_WORKFLOW.md` - Multi-agent patterns
   - `AGENT_SYSTEM_GUIDE.md` - Agent system deep dive

4. **Operations:**
   - `DEPLOYMENT_GUIDE.md` - Setup and deployment
   - `AGENT_MANAGEMENT_QUICKSTART.md` - Managing agents

5. **Examples:**
   - `examples.py` - Code examples
   - `GAME_TEST_RESULTS.md` - Snake game workflow example

### Key Concepts

- **Orchestrator Pattern**: Central coordinator delegates to specialists
- **Task Routing**: Intelligent analysis and agent matching
- **Skill Progression**: Agents improve through experience
- **TMUX Isolation**: Each agent in separate persistent session
- **Continuous Learning**: Performance tracking and optimization

---

## 🔐 Security Considerations

From `SECURITY_REVIEW.md` and `PHASE3_SECURITY_AUDIT.md`:

1. **API Key Protection**: Never commit `.env` file
2. **Input Validation**: All user inputs validated
3. **Command Injection**: Shell commands properly escaped
4. **File Access**: Agents restricted to workspace directories
5. **Resource Limits**: Timeouts and rate limiting enforced

---

## 📈 Performance Tips

1. **Use appropriate model tier** for task complexity
2. **Enable parallel execution** for independent tasks
3. **Leverage prompt caching** for repeated operations
4. **Monitor token usage** with built-in metrics
5. **Clean up TMUX sessions** periodically
6. **Use `--no-tmux`** for quick simple tasks

---

## 🤝 Contributing

See `CONTRIBUTING.md` for detailed guidelines.

**Quick checklist:**
- [ ] Follow PEP 8 code style
- [ ] Add type hints
- [ ] Write docstrings
- [ ] Add tests
- [ ] Update documentation
- [ ] Use conventional commit messages
- [ ] Test with `test_framework.py`

---

## 📞 Support & Resources

- **Issues**: Report bugs or request features
- **Documentation**: Check `README.md` and guides
- **Examples**: See `examples.py` for usage patterns
- **Testing**: Run `test_framework.py` to validate
- **Agent Management**: Use `manage_agents.py` for interactive config

---

## 🎉 Quick Reference

### Most Common Commands

```bash
# Execute task
python main.py task "your task description"

# Check status
python main.py status

# View agents
python main.py agents

# Generate report
python main.py report

# Validate setup
python validate_agents.py

# Run tests
python test_framework.py

# Manage agents
python manage_agents.py
```

### Directory Quick Access

```bash
# Agent definitions
cd .claude/agents/

# Core framework
cd agents/

# View logs
cd logs/

# Agent workspaces
cd workspace/

# Documentation
ls *.md
```

---

**End of CLAUDE.md** | Last updated: 2025-11-18 | Framework Version: 2.0
