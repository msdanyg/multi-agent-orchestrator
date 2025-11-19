# Multi-Agent Management Framework

**Version:** 2.1 | **Status:** ✅ Production Verified | **Last Updated:** 2025-11-18

An intelligent orchestration system that automatically delegates tasks to specialized Claude AI agents using TMUX for session management and the Claude Agent SDK for agent execution.

> **NEW in v2.1:** Real multi-agent workflows verified with actual Claude API calls. See [RELEASE_NOTES_v2.1.md](RELEASE_NOTES_v2.1.md) for details.

## Features

- **Automatic Task Delegation**: Analyzes tasks and selects optimal agents automatically
- **Intelligent Agent Selection**: Matches tasks to agents based on capabilities and performance history
- **Parallel Execution**: Executes independent tasks concurrently for efficiency
- **TMUX Integration**: Isolated agent sessions with persistence and recovery
- **Continuous Learning**: Tracks performance and improves over time
- **Skill Progression**: Agents level up from Novice to Master based on success
- **Comprehensive Monitoring**: Detailed metrics, reports, and insights

## Architecture

```
User Task
    ↓
Orchestrator (Manager)
    ↓
Task Router (Analyzes & Plans)
    ↓
Agent Registry (Selects Best Agents)
    ↓
TMUX Manager (Creates Sessions)
    ↓
Specialist Agents (Execute in Parallel/Sequential)
    ↓
Skills System (Tracks & Learns)
    ↓
Results Aggregated → User
```

## Default Specialist Agents

1. **Code Analyst**: Code review, architecture analysis, refactoring recommendations
2. **Code Writer**: Feature implementation, bug fixes, clean code development
3. **Tester**: Test execution, validation, quality assurance
4. **Researcher**: Information gathering, documentation search, best practices
5. **DevOps**: Builds, deployments, environment setup, infrastructure
6. **Documentation Writer**: Technical writing, tutorials, API docs

## Installation

### Prerequisites

- Python 3.10+
- TMUX (session manager)
- Claude API Key

### Setup

1. **Install TMUX** (if not already installed):
```bash
# macOS
brew install tmux

# Ubuntu/Debian
sudo apt-get install tmux

# Fedora
sudo dnf install tmux
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

4. **Verify installation**:
```bash
python main.py status
```

## Quick Start

### Execute a Task

```bash
python main.py task "Refactor the authentication module to use JWT tokens"
```

### List All Agents

```bash
python main.py agents
```

### Check System Status

```bash
python main.py status
```

### Generate Reports

```bash
python main.py report
```

## Usage Examples

### Basic Task Execution

```python
import asyncio
from agents import Orchestrator

async def main():
    orchestrator = Orchestrator()

    result = await orchestrator.execute_task(
        task_description="Fix the memory leak in the data processing pipeline",
        max_agents=3
    )

    print(f"Success: {result['success']}")
    print(f"Time: {result['execution_time']:.2f}s")

asyncio.run(main())
```

### Complex Multi-Step Workflow

```python
async def complex_workflow():
    orchestrator = Orchestrator()

    # Step 1: Research
    research = await orchestrator.execute_task(
        "Research JWT authentication best practices"
    )

    # Step 2: Implement
    if research['success']:
        implementation = await orchestrator.execute_task(
            "Implement JWT authentication",
            context={'previous_results': research}
        )

        # Step 3: Test
        if implementation['success']:
            testing = await orchestrator.execute_task(
                "Test JWT authentication implementation"
            )
```

### Parallel Task Execution

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

### Custom Context

```python
result = await orchestrator.execute_task(
    task_description="Optimize the search algorithm",
    context={
        'files': ['search.py', 'indexer.py'],
        'constraints': 'Maintain O(log n) complexity',
        'previous_results': 'Profiling shows bottleneck in indexing'
    }
)
```

## CLI Commands

### Task Execution

```bash
# Basic task
python main.py task "Implement user authentication"

# Limit number of agents
python main.py task "Fix bugs in payment system" --max-agents 2

# Execute without TMUX (direct execution)
python main.py task "Update documentation" --no-tmux
```

### System Management

```bash
# Show system status
python main.py status

# List all registered agents with performance metrics
python main.py agents

# Generate comprehensive reports
python main.py report

# Custom report location
python main.py report --output custom_report.md
```

## How It Works

### 1. Task Analysis

The Task Router analyzes your request to determine:
- Task type (implementation, bug fixing, research, etc.)
- Required capabilities (programming languages, tools)
- Complexity level (simple, medium, complex)
- Parallelization potential

### 2. Agent Selection

The system selects agents based on:
- Capability matching (agent skills vs task requirements)
- Historical performance (success rate, completion time)
- Skill level (novice → intermediate → expert → master)
- Confidence scoring

### 3. Execution

Agents execute tasks:
- **Primary agents**: Handle core task requirements
- **Supporting agents**: Validation, testing, review
- **Parallel or sequential**: Based on task dependencies

### 4. Learning

The Skills System tracks:
- Task outcomes (success/failure)
- Execution metrics (time, tokens, cost)
- Error patterns
- Successful prompt templates

Agents automatically level up based on performance.

## Agent Skill Progression

| Level | Requirements | Benefits |
|-------|-------------|----------|
| **Novice** | Default starting level | Base capabilities |
| **Intermediate** | 5+ tasks, 75%+ success rate | 1.2x priority multiplier |
| **Expert** | 20+ tasks, 85%+ success rate | 1.5x priority multiplier |
| **Master** | 50+ tasks, 90%+ success rate | 2.0x priority multiplier |

## Configuration

### Environment Variables

```bash
# API Configuration
ANTHROPIC_API_KEY=your_key_here

# Model Selection
ORCHESTRATOR_MODEL=claude-opus-4        # Planning and coordination
WORKER_MODEL=claude-sonnet-4-5          # Task execution
SIMPLE_MODEL=claude-haiku-4             # Simple tasks

# System Configuration
PROJECT_ROOT=/path/to/project
MAX_PARALLEL_AGENTS=5
AGENT_TIMEOUT=600

# Logging
LOG_LEVEL=INFO
```

### Custom Agents

Add custom agents to the registry:

```python
from agents import AgentRegistry, AgentDefinition

registry = AgentRegistry()

custom_agent = AgentDefinition(
    name="security_auditor",
    description="Security vulnerability detection and analysis",
    role="Analyzes code for security issues",
    tools=["Read", "Grep", "Glob"],
    capabilities=["security", "vulnerability_scan", "owasp"],
    system_prompt="You are a security expert specializing in...",
    model="claude-sonnet-4-5"
)

registry.register_agent(custom_agent)
```

## Directory Structure

```
Multi-agent/
├── agents/                 # Core framework
│   ├── orchestrator.py    # Main coordinator
│   ├── registry.py        # Agent definitions & metrics
│   ├── task_router.py     # Task analysis & agent selection
│   ├── tmux_manager.py    # TMUX session management
│   ├── skills_system.py   # Learning & improvement
│   └── __init__.py
├── workspace/             # Agent workspaces
│   ├── shared/           # Shared files between agents
│   └── <agent_name>/     # Per-agent workspace
├── logs/                  # System logs and reports
├── config/                # Configuration files
├── specialists/           # Custom specialist agents
├── main.py               # CLI entry point
├── examples.py           # Usage examples
├── ARCHITECTURE.md       # Detailed architecture
└── README.md            # This file
```

## Monitoring & Debugging

### View TMUX Sessions

```bash
# List all sessions
tmux ls

# Attach to specific agent session
tmux attach -t agent-code_writer-abc123

# Detach from session
Ctrl+B, then D
```

### Check Logs

```bash
# View system logs
tail -f logs/system.log

# View agent workspace
ls -la workspace/code_writer/
```

### Performance Reports

```bash
# Generate comprehensive report
python main.py report

# View skills report
cat logs/skills_report.md

# View system report
cat logs/system_report.md
```

## Advanced Features

### Session Recovery

TMUX sessions persist even if disconnected. Reattach anytime:

```bash
tmux attach -t <session-id>
```

### Checkpoint System

For long-running tasks, the framework automatically creates checkpoints to enable recovery.

### Context Compaction

Automatic context window management prevents overflow during long conversations.

### Hooks & Events

Customize agent behavior with lifecycle hooks:
- PreToolUse
- PostToolUse
- SubagentStop
- PreCompact

## Performance Optimization

### Model Tiering

- **Opus 4**: Complex reasoning, orchestration (expensive but powerful)
- **Sonnet 4**: Standard tasks, most agent work (balanced)
- **Haiku 4**: Simple tasks, data retrieval (fast and cheap)

### Parallel Execution

Independent tasks execute simultaneously when possible.

### Prompt Caching

Automatic caching reduces token usage on repeated operations.

### Context Management

Aggressive compaction and summarization for long sessions.

## Cost Management

Track costs with built-in metrics:

```python
status = orchestrator.get_system_status()
print(f"Total cost: ${status['registry']['total_cost']:.2f}")
```

Typical costs:
- Simple task: $0.01 - $0.05
- Medium task: $0.05 - $0.20
- Complex task: $0.20 - $1.00

## Troubleshooting

### TMUX Not Found

```bash
# Install tmux first
brew install tmux  # macOS
sudo apt install tmux  # Linux
```

### API Key Issues

```bash
# Verify API key is set
echo $ANTHROPIC_API_KEY

# Or check .env file
cat .env
```

### Agent Not Found

```bash
# List available agents
python main.py agents

# Check registry
cat agents/registry.json
```

### Session Cleanup

```bash
# Kill old sessions
tmux kill-session -t <session-id>

# Kill all sessions
tmux kill-server
```

## Integration with Claude Agent SDK

This framework is designed to integrate with the Claude Agent SDK. The current implementation provides the orchestration layer and can be enhanced with full SDK integration for production use.

### Next Steps for Production

1. Integrate Claude Agent SDK for actual agent execution
2. Implement MCP servers for inter-agent communication
3. Add comprehensive error handling and retries
4. Set up observability (OpenTelemetry, logging)
5. Implement authentication and authorization
6. Add distributed execution support

## Contributing

To add new agents or capabilities:

1. Define agent in `agents/registry.py`
2. Add task patterns in `agents/task_router.py`
3. Test with examples
4. Update documentation

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- Check troubleshooting section
- Review examples in `examples.py`
- See architecture documentation in `ARCHITECTURE.md`

## Roadmap

- [ ] Full Claude Agent SDK integration
- [ ] Web dashboard for monitoring
- [ ] Agent collaboration (peer-to-peer)
- [ ] Cloud deployment support
- [ ] Multi-project agent pools
- [ ] Visual workflow designer
- [ ] Prompt template library
- [ ] Integration with CI/CD systems

---

Built with Claude Agent SDK and TMUX | Version 1.0.0
