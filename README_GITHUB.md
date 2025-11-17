# Multi-Agent Orchestrator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **Intelligent multi-agent orchestration framework using Claude AI for automatic task delegation, parallel execution, and continuous improvement**

Transform complex development tasks into coordinated workflows with specialized AI agents that automatically collaborate to deliver results.

---

## ✨ Features

- 🤖 **Automatic Task Delegation** - Analyzes tasks and routes to optimal specialist agents
- ⚡ **Parallel Execution** - Multiple agents work simultaneously for efficiency
- 🎯 **Intelligent Routing** - Task router selects best agents based on capabilities and performance
- 📊 **Continuous Learning** - Agents improve through performance tracking and skill progression
- 🔄 **TMUX Integration** - Isolated agent sessions with persistence and recovery
- 📈 **Performance Tracking** - Comprehensive metrics, logging, and reporting
- 🎭 **6 Default Specialists** - Pre-configured agents for common development tasks
- 📚 **Extensive Documentation** - Guides for setup, deployment, and customization

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- TMUX (`brew install tmux` on macOS or `apt install tmux` on Linux)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/multi-agent-orchestrator.git
cd multi-agent-orchestrator

# Run automated setup
./install.sh . full

# Configure API key
nano .env
# Add: ANTHROPIC_API_KEY=your_key_here
```

### First Task

```bash
# Execute a task
python3 main.py task "Analyze the project structure and identify key components"

# List available agents
python3 main.py agents

# Check system status
python3 main.py status
```

**[→ See Full Quick Start Guide](QUICKSTART.md)**

---

## 🎯 How It Works

```
User Task
    ↓
🧠 Orchestrator (Analyzes & Plans)
    ↓
📊 Task Router (Selects Optimal Agents)
    ↓
🤖 Specialist Agents (Execute in Parallel/Sequential)
    ├─ Code Analyst: Reviews architecture
    ├─ Code Writer: Implements features
    ├─ Tester: Validates functionality
    ├─ Researcher: Gathers information
    ├─ DevOps: Handles deployment
    └─ Docs Writer: Creates documentation
    ↓
✅ Results Aggregated & Returned
```

**[→ See Architecture Details](ARCHITECTURE.md)**

---

## 🤖 Default Specialist Agents

| Agent | Specialization | Tools | Use Cases |
|-------|---------------|-------|-----------|
| **code_analyst** | Code review, architecture | Read, Grep, Glob | Analyze code quality, identify patterns |
| **code_writer** | Implementation, bug fixes | Read, Write, Edit | Build features, fix bugs |
| **tester** | Testing, QA validation | Bash, Read, Grep | Run tests, validate functionality |
| **researcher** | Information gathering | WebSearch, WebFetch | Research best practices, find docs |
| **devops** | Deployment, infrastructure | Bash, Read, Write | Build, deploy, configure systems |
| **docs_writer** | Technical documentation | Read, Write, Glob | Create guides, API docs |

**[→ Learn About Agent Customization](DEPLOYMENT_GUIDE.md#custom-agent-creation)**

---

## 📚 Example: Multi-Agent Calculator

See the framework in action with our calculator demo that showcases true multi-agent collaboration:

```bash
# Run the calculator demo
python3 calculator_cli.py

# See the test suite (31 tests, 100% passing)
python3 test_calculator.py
```

**Built by 4 specialized agents:**
- `code_analyst` - Designed architecture
- `code_writer` - Implemented code (275 lines)
- `tester` - Created tests (31 tests)
- `docs_writer` - Wrote documentation

**[→ See Calculator Demo Details](MULTI_AGENT_PROOF.md)**

---

## 💻 Usage Examples

### Basic Task Execution

```bash
# Code review
python3 main.py task "Review the authentication module for security issues"

# Feature implementation
python3 main.py task "Implement JWT authentication with proper error handling"

# Research task
python3 main.py task "Research best practices for API rate limiting"
```

### Programmatic Usage

```python
import asyncio
from agents import Orchestrator

async def main():
    orchestrator = Orchestrator()

    result = await orchestrator.execute_task(
        task_description="Build a REST API with FastAPI",
        max_agents=3
    )

    print(f"Success: {result['success']}")
    print(f"Agents used: {result['agents_used']}")

asyncio.run(main())
```

### Complex Workflows

```python
# Sequential pipeline
await orchestrator.execute_task("Research OAuth 2.0 best practices")
await orchestrator.execute_task("Implement OAuth based on research")
await orchestrator.execute_task("Test OAuth implementation")

# Parallel execution
tasks = [
    orchestrator.execute_task("Review database models"),
    orchestrator.execute_task("Update API documentation"),
    orchestrator.execute_task("Run test suite")
]
results = await asyncio.gather(*tasks)
```

**[→ See More Examples](examples.py)**

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | Get started in 5 minutes |
| [README.md](README.md) | Complete feature documentation |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design and architecture |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Detailed setup and configuration |
| [SETUP_QUICKREF.md](SETUP_QUICKREF.md) | Quick reference card |
| [IMPROVEMENTS_ANALYSIS.md](IMPROVEMENTS_ANALYSIS.md) | Future enhancements roadmap |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |

---

## 🛠️ Key Commands

```bash
# System Management
python3 main.py status              # Show system status
python3 main.py agents              # List all agents
python3 main.py report              # Generate performance report

# Task Execution
python3 main.py task "description"  # Execute a task
python3 main.py task "..." --max-agents 2  # Limit agents
python3 main.py task "..." --no-tmux       # Direct execution

# Examples and Testing
python3 examples.py                 # Interactive examples
python3 test_framework.py           # Run test suite

# TMUX Session Management
tmux ls                             # List sessions
tmux attach -t <session-id>         # Attach to session
```

---

## 🎯 Use Cases

### Software Development
- Code review and refactoring
- Feature implementation
- Bug fixing and debugging
- Test generation and validation

### Research & Analysis
- Technology research
- Best practices investigation
- Competitive analysis
- Documentation search

### DevOps & Deployment
- CI/CD pipeline setup
- Infrastructure configuration
- Build automation
- Deployment management

### Documentation
- API documentation
- User guides
- Technical specifications
- README files

---

## 🔧 Configuration

### Environment Variables

```bash
# .env file
ANTHROPIC_API_KEY=your_key_here
ORCHESTRATOR_MODEL=claude-opus-4
WORKER_MODEL=claude-sonnet-4-5
MAX_PARALLEL_AGENTS=5
AGENT_TIMEOUT=600
LOG_LEVEL=INFO
```

### Custom Agents

Create custom agents for your tech stack:

```python
from agents import AgentRegistry, AgentDefinition

custom_agent = AgentDefinition(
    name="django_expert",
    description="Django web framework specialist",
    tools=["Read", "Write", "Bash"],
    capabilities=["django", "python", "web_development"],
    system_prompt="You are a Django expert...",
    model="claude-sonnet-4-5"
)

registry = AgentRegistry()
registry.register_agent(custom_agent)
```

**[→ See Full Configuration Guide](DEPLOYMENT_GUIDE.md)**

---

## 📊 System Requirements

- **OS**: macOS, Linux, or WSL2 on Windows
- **Python**: 3.10 or higher
- **TMUX**: 3.0 or higher
- **RAM**: 4GB minimum (8GB+ recommended)
- **Disk**: 500MB for framework + workspace

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Areas for contribution:**
- New specialist agents
- Workflow patterns
- Documentation improvements
- Bug fixes
- Performance optimizations

---

## 🐛 Troubleshooting

### Common Issues

**TMUX not found**
```bash
brew install tmux  # macOS
sudo apt install tmux  # Linux
```

**Import errors**
```bash
# Activate virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

**Agent not found**
```bash
# List available agents
python3 main.py agents

# Check registry
cat agents/registry.json
```

**[→ See Full Troubleshooting Guide](DEPLOYMENT_GUIDE.md#troubleshooting)**

---

## 📈 Performance

- **Test Coverage**: 100% (31/31 tests passing)
- **Agent Specialization**: 6 default agents
- **Setup Time**: < 5 minutes
- **Task Routing**: Automatic with confidence scoring
- **Parallel Execution**: Up to 5 concurrent agents

---

## 🗺️ Roadmap

### Current (v1.0)
- ✅ Complete orchestration framework
- ✅ 6 default specialist agents
- ✅ Automatic task routing
- ✅ TMUX session management
- ✅ Skills tracking and learning

### Planned (v2.0)
- [ ] Native Claude Agent SDK integration
- [ ] MCP (Model Context Protocol) support
- [ ] 150+ pre-built MCP tools
- [ ] Web dashboard for monitoring
- [ ] Agent collaboration patterns
- [ ] Cloud deployment support

**[→ See Detailed Roadmap](IMPROVEMENTS_ANALYSIS.md)**

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Claude Agent SDK](https://docs.claude.com/en/docs/agent-sdk/overview)
- Inspired by multi-agent orchestration patterns
- Thanks to all contributors

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/multi-agent-orchestrator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/multi-agent-orchestrator/discussions)
- **Documentation**: See [docs](./README.md)

---

## ⭐ Show Your Support

If you find this project useful, please consider:
- Starring the repository ⭐
- Sharing with others
- Contributing improvements
- Reporting issues

---

**Built with ❤️ by the open source community**

[Get Started →](QUICKSTART.md) | [Documentation →](README.md) | [Examples →](examples.py)
