# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies (Optional)

The framework is ready to use, but for full functionality install:

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install python-dotenv rich
```

### 2. Verify Installation

```bash
python3 main.py status
```

You should see:
```
🤖 Agent Registry: 6 agents ready
📦 TMUX Sessions: Available
```

### 3. List Available Agents

```bash
python3 main.py agents
```

Shows all 6 default specialist agents:
- **code_analyst** - Code review and architecture
- **code_writer** - Implementation and bug fixes
- **tester** - Testing and validation
- **researcher** - Information gathering
- **devops** - Builds and deployment
- **docs_writer** - Documentation

### 4. Run Your First Task

```bash
python3 main.py task "Analyze the codebase structure and identify key components"
```

The orchestrator will:
1. ✅ Analyze your task
2. ✅ Select the best agent(s)
3. ✅ Execute in TMUX sessions
4. ✅ Return results

### 5. Try Examples

```bash
python3 examples.py
```

Choose from 7 interactive examples demonstrating:
- Code refactoring
- Bug fixing
- Feature implementation
- Research tasks
- Complex workflows
- Parallel execution

## 📖 Common Commands

### Execute Tasks

```bash
# Simple task
python3 main.py task "Fix authentication bugs"

# Limit agents
python3 main.py task "Implement API" --max-agents 2

# Without TMUX (direct execution)
python3 main.py task "Update docs" --no-tmux
```

### System Management

```bash
# Show status
python3 main.py status

# List agents
python3 main.py agents

# Generate reports
python3 main.py report
```

### Monitor TMUX Sessions

```bash
# List all sessions
tmux ls

# Attach to session
tmux attach -t agent-code_writer-abc123

# Detach (from inside session)
Ctrl+B, then D
```

## 🔧 Integration with Claude Agent SDK

The current implementation provides the orchestration framework. To integrate with Claude Agent SDK for production use:

### Option 1: Add SDK Integration to Orchestrator

Edit `agents/orchestrator.py` in the `_execute_single_agent` method:

```python
# Replace simulation with actual SDK call
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    allowed_tools=agent.tools,
    system_prompt=agent.system_prompt,
    model=agent.model,
    cwd=str(agent_workspace)
)

async for message in query(prompt=prompt, options=options):
    # Process message
    if isinstance(message, ResultMessage):
        result['success'] = True
        result['output'] = message.content
```

### Option 2: Use as Orchestration Layer

Keep the framework as a meta-orchestrator that manages multiple Claude Agent SDK instances, delegating work and aggregating results.

## 💡 Next Steps

1. **Review Architecture**: Read `ARCHITECTURE.md` for design details
2. **Full Documentation**: See `README.md` for comprehensive guide
3. **Run Tests**: Execute `python3 test_framework.py`
4. **Customize Agents**: Add your own specialists in `agents/registry.py`
5. **Configure**: Create `.env` file for API keys when ready

## 🎯 Example Workflows

### Code Refactoring

```bash
python3 main.py task "Refactor authentication to use JWT tokens"
```

The system will:
- Assign **code_analyst** to review current implementation
- Assign **code_writer** to implement changes
- Assign **tester** to validate the refactoring

### Bug Investigation

```bash
python3 main.py task "Investigate and fix memory leak in data pipeline"
```

Automatically delegates to:
- **code_analyst** for analysis
- **code_writer** for the fix
- **tester** for validation

### Feature Development

```bash
python3 main.py task "Implement user dashboard with React and TypeScript"
```

Coordinates:
- **researcher** for best practices
- **code_writer** for implementation
- **tester** for testing
- **docs_writer** for documentation

## 🔍 Troubleshooting

### TMUX Issues

```bash
# Check if installed
tmux -V

# Kill stuck sessions
tmux kill-session -t <session-id>

# Kill all sessions
tmux kill-server
```

### Agent Not Found

```bash
# Verify agents loaded
python3 main.py agents

# Check registry
cat agents/registry.json
```

### No Python Module

```bash
# Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📚 Learn More

- **Architecture**: `ARCHITECTURE.md` - System design
- **Full Docs**: `README.md` - Complete reference
- **Examples**: `examples.py` - Interactive examples
- **Tests**: `test_framework.py` - Framework validation

## 🆘 Need Help?

1. Check the troubleshooting section in README.md
2. Review examples in examples.py
3. Run tests to verify setup: `python3 test_framework.py`

---

**Ready to orchestrate! 🎭**

Your multi-agent system is set up and ready to automatically delegate tasks to specialized AI agents.
