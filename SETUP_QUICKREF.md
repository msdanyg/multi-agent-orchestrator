# Multi-Agent Setup - Quick Reference Card

**One-page guide for deploying to new projects/devices**

---

## 🚀 Super Quick Install (1 Command)

```bash
# Copy framework and auto-install everything
./install.sh /path/to/new/project full
```

---

## 📦 Installation Options

### Option 1: Automated Install Script

```bash
# Full installation
./install.sh /path/to/target full

# Minimal installation (core only)
./install.sh /path/to/target minimal

# Custom installation (choose components)
./install.sh /path/to/target custom
```

### Option 2: Manual Setup Script

```bash
# Copy files
cp -r /path/to/Multi-agent /path/to/target
cd /path/to/target

# Run setup
./setup.sh
```

### Option 3: Manual Step-by-Step

```bash
# 1. Create directory
mkdir my-project-agents && cd my-project-agents

# 2. Copy files
cp -r /path/to/Multi-agent/* .

# 3. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Configure
cp .env.example .env
nano .env  # Add ANTHROPIC_API_KEY

# 5. Initialize
python3 -c "from agents import AgentRegistry; AgentRegistry()"

# 6. Test
python3 main.py status
```

---

## ⚙️ Configuration Checklist

- [ ] Install TMUX: `brew install tmux` (macOS) or `apt install tmux` (Linux)
- [ ] Python 3.10+: `python3 --version`
- [ ] Copy framework files
- [ ] Create `.env` file
- [ ] Add `ANTHROPIC_API_KEY=your_key`
- [ ] Set `PROJECT_ROOT=/your/project/path`
- [ ] Run `python3 main.py status` to verify

---

## 🎯 Quick Commands

```bash
# Check status
python3 main.py status

# List agents
python3 main.py agents

# Run task
python3 main.py task "description"

# Run examples
python3 examples.py

# Run tests
python3 test_framework.py

# Generate report
python3 main.py report
```

---

## 🤖 Add Custom Agent (3 Steps)

### Step 1: Create Agent File

```python
# specialists/my_agent.py
from agents import AgentRegistry, AgentDefinition

agent = AgentDefinition(
    name="my_specialist",
    description="What this agent does",
    role="Agent's specific role",
    tools=["Read", "Write", "Bash"],
    capabilities=["skill1", "skill2"],
    system_prompt="You are an expert in...",
    model="claude-sonnet-4-5"
)

registry = AgentRegistry()
registry.register_agent(agent)
```

### Step 2: Register

```bash
python3 specialists/my_agent.py
```

### Step 3: Verify

```bash
python3 main.py agents | grep my_specialist
```

---

## 🔧 Common Configurations

### Web Development Project

```bash
# .env
PROJECT_ROOT=/Users/me/my-web-app
MAX_PARALLEL_AGENTS=5

# Add agents for: react, node, api, database
```

### Data Science Project

```bash
# .env
PROJECT_ROOT=/Users/me/ml-project
MAX_PARALLEL_AGENTS=3

# Add agents for: python, jupyter, data_analysis
```

### DevOps Project

```bash
# .env
PROJECT_ROOT=/Users/me/infrastructure
MAX_PARALLEL_AGENTS=5

# Add agents for: docker, kubernetes, terraform, ci_cd
```

---

## 📂 Essential File Structure

```
my-project/
├── agents/               # Core framework
│   ├── orchestrator.py
│   ├── registry.py
│   ├── task_router.py
│   └── registry.json
├── specialists/          # Custom agents (add yours here)
├── workspace/           # Agent working directories
├── logs/                # System logs
├── config/              # Configuration files
├── main.py             # CLI entry point
├── .env                # Environment config (add API key here)
└── README.md           # Documentation
```

---

## 🐛 Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| "TMUX not found" | `brew install tmux` or `apt install tmux` |
| "No module agents" | Run from project root: `cd /path/to/project` |
| "API key error" | Check `.env`: `cat .env \| grep ANTHROPIC` |
| Sessions stuck | `tmux kill-server` |
| Tests failing | `python3 test_framework.py -v` |
| Import errors | Activate venv: `source venv/bin/activate` |

---

## 📞 Help Resources

| Resource | Location |
|----------|----------|
| **Quick Start** | `QUICKSTART.md` |
| **Full Setup Guide** | `DEPLOYMENT_GUIDE.md` |
| **Main Documentation** | `README.md` |
| **Architecture** | `ARCHITECTURE.md` |
| **Examples** | `examples.py` |
| **Tests** | `test_framework.py` |

---

## ✅ Verification Steps

```bash
# 1. Framework installed
ls agents/orchestrator.py  # Should exist

# 2. TMUX available
tmux -V  # Should show version

# 3. Python works
python3 main.py status  # Should show stats

# 4. Agents loaded
python3 main.py agents  # Should show 6+ agents

# 5. Tests pass
python3 test_framework.py  # Should show 5/5 passing
```

---

## 🎓 Example: Deploy to New Project

```bash
# 1. Navigate to new project
cd ~/projects/my-new-app

# 2. Install orchestrator
/path/to/Multi-agent/install.sh . full

# 3. Configure for this project
echo "PROJECT_ROOT=$(pwd)" >> .env
echo "ANTHROPIC_API_KEY=sk-ant-xxx" >> .env

# 4. Create project-specific agent
cat > specialists/my_app_agent.py << 'EOF'
from agents import AgentRegistry, AgentDefinition

agent = AgentDefinition(
    name="myapp_specialist",
    description="Specialist for my app's tech stack",
    role="Develops features using our stack",
    tools=["Read", "Write", "Edit", "Bash"],
    capabilities=["python", "flask", "postgresql"],
    system_prompt="You are an expert in Flask and PostgreSQL...",
    model="claude-sonnet-4-5"
)

registry = AgentRegistry()
registry.register_agent(agent)
print("✅ Registered myapp_specialist")
EOF

# 5. Register custom agent
python3 specialists/my_app_agent.py

# 6. Test with project-specific task
python3 main.py task "Review the Flask app structure"

# 7. Verify
python3 main.py status
python3 main.py agents
```

---

## 💡 Pro Tips

1. **Use virtual environments** - Isolates dependencies
2. **Create project-specific agents** - Better task routing
3. **Monitor workspace disk usage** - Clean up regularly
4. **Use meaningful task descriptions** - Better agent selection
5. **Check logs when debugging** - `tail -f logs/*.log`
6. **Backup registry and skills** - `cp agents/*.json backup/`

---

## 🚦 Success Indicators

✅ `python3 main.py status` shows agent counts
✅ `python3 main.py agents` lists 6+ agents
✅ `test_framework.py` shows 5/5 passing
✅ `python3 main.py task "test"` executes without errors
✅ `.env` contains valid `ANTHROPIC_API_KEY`
✅ `tmux ls` works without error

---

## 📋 Pre-Deployment Checklist

Before deploying to a new device/project:

- [ ] TMUX installed and working
- [ ] Python 3.10+ available
- [ ] API key obtained from Anthropic
- [ ] Project directory created
- [ ] Framework files copied
- [ ] Dependencies installed (requirements.txt)
- [ ] .env configured with API key
- [ ] Agents initialized (registry.json created)
- [ ] Tests passing (test_framework.py)
- [ ] System status shows ready (main.py status)

---

## 🎯 Three Deployment Methods Compared

| Method | Speed | Customization | Best For |
|--------|-------|---------------|----------|
| **install.sh full** | ⚡ Fast | ⭐ Medium | Quick setup, testing |
| **install.sh custom** | ⚡⚡ Medium | ⭐⭐⭐ High | Production, specific needs |
| **Manual setup** | ⚡⚡⚡ Slow | ⭐⭐⭐⭐ Very High | Learning, complex setups |

**Recommendation**: Start with `install.sh full`, customize later.

---

**Questions? See detailed guide: `DEPLOYMENT_GUIDE.md`**

**Ready to deploy? Run: `./install.sh /path/to/target full`**
