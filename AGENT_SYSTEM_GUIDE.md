# Agent System Architecture Guide
## Where to Find Agent Instructions, Memory, Skills & Configuration

---

## 📁 Directory Structure

```
Multi-agent-v2/
│
├── .claude/                          # Claude Code agent definitions
│   └── agents/                       # Agent-specific instructions
│       ├── code_analyst.md          # Code analyst prompt
│       └── code_writer.md           # Code writer prompt
│
├── agents/                           # Core agent system
│   ├── registry.json                # ⭐ MAIN: All agent definitions & metrics
│   ├── skills_history.json          # 🧠 MEMORY: Learning & performance history
│   ├── orchestrator.py              # Agent coordinator
│   ├── registry.py                  # Registry management
│   ├── task_router.py               # Task routing logic
│   ├── skills_system.py             # Skills & learning system
│   └── tmux_manager.py              # TMUX session management
│
└── workspace/                        # Agent workspaces
    └── [agent_name]/                # Per-agent work directories
        └── [task_id]/               # Task-specific files
```

---

## 1. 📋 Agent Registry (Main Configuration)

**Location:** `agents/registry.json`

This is the **primary source** for all agent definitions. Each agent has:

### Agent Definition Structure:
```json
{
  "agent_name": {
    "name": "agent_name",
    "description": "What the agent does",
    "role": "Agent's primary role",
    "tools": ["Tool1", "Tool2"],           // Available tools
    "capabilities": ["skill1", "skill2"],   // What it can do
    "system_prompt": "Detailed instructions",
    "model": "claude-sonnet-4-5",          // Which Claude model
    "skill_level": "novice",                // Progress level
    "metrics": {                            // Performance tracking
      "total_tasks": 0,
      "successful_tasks": 0,
      "failed_tasks": 0,
      "total_tokens": 0,
      "total_cost": 0.0,
      "avg_completion_time": 0.0,
      "last_used": null
    }
  }
}
```

### Currently Registered Agents (12 total):

1. **code_analyst** - Code review & architecture
2. **code_writer** - Implementation
3. **tester** - Testing & validation
4. **researcher** - Information gathering
5. **devops** - Deployment & infrastructure
6. **docs_writer** - Documentation
7. **designer** - UI/UX design
8. **qa_tester** - Comprehensive QA
9. **api_expert** - API design & integration
10. **security** - Security auditing
11. **data_analyst** - Data analysis
12. **database_manager** - Database design

### To View Agent Details:
```bash
# View all agents
cat agents/registry.json | python -m json.tool

# View specific agent
cat agents/registry.json | jq '.code_writer'

# Or use the CLI
python main.py agents
```

---

## 2. 🧠 Skills & Memory System

**Location:** `agents/skills_history.json`

This file tracks:
- Task execution outcomes
- Success/failure patterns
- Performance metrics over time
- Learning insights

### Structure:
```json
{
  "outcomes": [
    {
      "task_id": "unique_id",
      "agent_name": "code_analyst",
      "task_description": "...",
      "task_type": "general",
      "success": true,
      "execution_time": 1.02,
      "tokens_used": 0,
      "cost": 0.0,
      "timestamp": "2025-11-16T22:58:24"
    }
  ],
  "prompt_patterns": {
    // Learned prompt patterns that work well
  },
  "agent_insights": {
    "agent_name": {
      "task_types": {...},      // Which tasks work best
      "common_errors": {...},   // Known issues
      "best_tasks": [...],      // Top performances
      "worst_tasks": [...]      // Areas for improvement
    }
  }
}
```

### To View Memory:
```bash
# View skills history
cat agents/skills_history.json | python -m json.tool

# View specific agent insights
cat agents/skills_history.json | jq '.agent_insights.code_analyst'
```

---

## 3. 📝 Agent Instructions (.claude files)

**Location:** `.claude/agents/[agent_name].md`

These are **Claude Code-specific** agent definitions in Markdown format.

### Format:
```markdown
---
name: agent_name
description: Brief description
allowed_tools: ["Tool1", "Tool2"]
model: claude-sonnet-4-5
---

Detailed instructions...

## Core Expertise
- Skill 1
- Skill 2

## Working Style
- How the agent works

## Constraints
- Limitations and rules

## Output Format
- Expected output structure
```

### Currently Available:
- `.claude/agents/code_analyst.md`
- `.claude/agents/code_writer.md`

### To Create New Agent Instructions:
```bash
# Create new agent file
nano .claude/agents/designer.md
```

Example template:
```markdown
---
name: designer
description: UI/UX design specialist
allowed_tools: ["Read", "Write", "Edit"]
model: claude-sonnet-4-5
---

You are a UI/UX design expert specializing in...
```

---

## 4. 🎯 Task Router Configuration

**Location:** `agents/task_router.py`

Defines how tasks are analyzed and routed to agents.

### Key Components:

#### Task Patterns (lines 35-72):
```python
TASK_PATTERNS = {
    r'\b(review|analyze)\s+code': ('code_analysis', ['code_review']),
    r'\b(implement|build)\s+feature': ('implementation', ['implementation']),
    # ... more patterns
}
```

#### Language Detection (lines 75-83):
```python
LANGUAGE_PATTERNS = {
    r'\bpython\b': 'python',
    r'\bjavascript\b': 'javascript',
    # ... more languages
}
```

#### Complexity Indicators (lines 86-92):
```python
COMPLEXITY_HIGH = ['refactor', 'architecture', 'system']
COMPLEXITY_MEDIUM = ['implement', 'feature', 'api']
```

### To Modify Routing:
```bash
# Edit task router
nano agents/task_router.py
```

---

## 5. 🔧 Agent Management Python Files

### `orchestrator.py`
- **Purpose:** Coordinates multi-agent task execution
- **Key Functions:**
  - `execute_task()` - Main task execution
  - `_execute_with_agents()` - Agent coordination
  - `_record_outcomes()` - Learning tracking

### `registry.py`
- **Purpose:** Manages agent registry
- **Key Functions:**
  - `load_registry()` - Load agent definitions
  - `get_agent()` - Retrieve specific agent
  - `find_best_agent()` - Agent selection
  - `update_metrics()` - Performance tracking

### `skills_system.py`
- **Purpose:** Learning and adaptation system
- **Key Functions:**
  - `record_outcome()` - Save task results
  - `get_agent_insights()` - Performance analysis
  - `suggest_improvements()` - Optimization tips

### To View System Code:
```bash
# View orchestrator
cat agents/orchestrator.py

# View registry manager
cat agents/registry.py

# View skills system
cat agents/skills_system.py
```

---

## 6. 💾 Workspace & Sessions

**Location:** `workspace/`

Each agent gets its own workspace:

```
workspace/
├── code_analyst/
│   └── 81952879/          # Task ID
│       └── prompt.txt     # Task prompt given to agent
├── code_writer/
│   └── [task_id]/
└── sessions.json          # TMUX session tracking
```

### To View Workspace:
```bash
# List all workspaces
ls -la workspace/

# View specific agent workspace
ls -la workspace/code_analyst/

# View task prompt
cat workspace/code_analyst/81952879/prompt.txt
```

---

## 🔍 How to View Agent Information

### Option 1: Using CLI Commands

```bash
# Activate virtual environment first
source venv/bin/activate

# List all agents with details
python main.py agents

# Check system status
python main.py status

# Generate full report
python main.py report
```

### Option 2: Direct File Access

```bash
# View agent registry
cat agents/registry.json | python -m json.tool

# View specific agent (with jq)
cat agents/registry.json | jq '.designer'

# View skills history
cat agents/skills_history.json | python -m json.tool

# View agent instructions
cat .claude/agents/code_analyst.md
```

### Option 3: Using Python

```python
import json

# Load registry
with open('agents/registry.json', 'r') as f:
    registry = json.load(f)

# View specific agent
print(json.dumps(registry['code_writer'], indent=2))

# View all agent names
print(list(registry.keys()))
```

---

## ✏️ How to Modify Agent Configuration

### 1. Edit Agent Definition (registry.json)

```bash
# Open in editor
nano agents/registry.json

# Or use jq to edit specific field
jq '.code_writer.model = "claude-opus-4"' agents/registry.json > temp.json
mv temp.json agents/registry.json
```

### 2. Edit Agent Instructions (.claude files)

```bash
# Edit existing
nano .claude/agents/code_analyst.md

# Create new agent
cat > .claude/agents/designer.md << 'EOF'
---
name: designer
description: UI/UX design expert
allowed_tools: ["Read", "Write", "Edit"]
model: claude-sonnet-4-5
---

Your instructions here...
EOF
```

### 3. Modify Task Routing

```bash
# Edit task router
nano agents/task_router.py

# Add new pattern to TASK_PATTERNS dictionary
```

---

## 🎓 Agent Skill Levels

Agents progress through skill levels based on performance:

1. **novice** (default) - Just starting
2. **intermediate** - Some experience
3. **expert** - High proficiency
4. **master** - Peak performance

Skill level affects:
- Confidence scores in task selection
- Priority in agent selection
- Learning rate in skills system

---

## 📊 Monitoring Agent Performance

### View Metrics:
```bash
# CLI status
python main.py status

# View specific agent metrics
cat agents/registry.json | jq '.code_analyst.metrics'
```

### Metrics Tracked:
- Total tasks completed
- Success/failure rate
- Average execution time
- Token usage
- Cost (if applicable)
- Last used timestamp

---

## 🔄 Agent Lifecycle

1. **Registration** → Added to `agents/registry.json`
2. **Task Assignment** → Router selects agent via `task_router.py`
3. **Execution** → Orchestrator runs agent in TMUX session
4. **Recording** → Results saved to `skills_history.json`
5. **Learning** → Metrics updated in `registry.json`

---

## 🛠️ Quick Reference Commands

```bash
# View all agents
python main.py agents

# View agent files
ls -la agents/
ls -la .claude/agents/

# Edit agent definition
nano agents/registry.json

# Edit agent instructions
nano .claude/agents/code_analyst.md

# View workspace
ls -la workspace/

# Check skills/memory
cat agents/skills_history.json

# System status
python main.py status
```

---

## 📚 Key Files Summary

| File | Purpose | Contains |
|------|---------|----------|
| `agents/registry.json` | Main config | All agent definitions, capabilities, metrics |
| `agents/skills_history.json` | Memory | Task outcomes, learning patterns |
| `.claude/agents/*.md` | Instructions | Detailed agent prompts |
| `agents/task_router.py` | Routing logic | How tasks are matched to agents |
| `agents/orchestrator.py` | Coordinator | Multi-agent execution engine |
| `workspace/` | Work area | Task-specific files and outputs |

---

## 💡 Pro Tips

1. **Always edit registry.json carefully** - Invalid JSON breaks the system
2. **Use jq for JSON editing** - Safer than manual editing
3. **Back up before changes** - `cp agents/registry.json agents/registry.json.bak`
4. **Check syntax** - `python -m json.tool agents/registry.json`
5. **Test new agents** - Start with simple tasks
6. **Monitor performance** - Check metrics regularly
7. **Update skill levels** - Manually promote agents based on performance

---

## 🚀 Next Steps

1. **Explore agent definitions:** `cat agents/registry.json | python -m json.tool`
2. **Read agent instructions:** `cat .claude/agents/*.md`
3. **Check learning history:** `cat agents/skills_history.json`
4. **Try modifying an agent:** Edit capabilities or tools
5. **Test the changes:** `python main.py agents`

---

**Everything is transparent and editable!** All agent configurations are in plain JSON and Markdown files. 🎉
