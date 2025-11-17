# 🎯 Agent Management Tools - User Guide

**Easy-to-use tools for viewing and editing your multi-agent system**

---

## 🚀 Quick Start (3 Simple Steps)

### 1. List All Agents
```bash
python manage_agents.py list
```
See all 12 agents at a glance!

### 2. View Agent Details
```bash
python manage_agents.py view designer
```
See everything about a specific agent!

### 3. Edit Agent
```bash
python manage_agents.py edit designer
```
Opens in your text editor - make changes and save!

---

## 📦 What You Get

### 1. **manage_agents.py** - Main Management Tool
**Your one-stop shop for agent management**

**Features:**
- ✅ List all agents (brief or detailed)
- ✅ View complete agent information
- ✅ Edit agent configurations in your editor
- ✅ Create new agents with guided wizard
- ✅ Delete agents safely
- ✅ Compare two agents side-by-side
- ✅ Interactive mode or command-line mode

**Usage:**
```bash
# Interactive mode (easiest)
python manage_agents.py

# Or specific commands
python manage_agents.py list
python manage_agents.py view security
python manage_agents.py edit api_expert
```

---

### 2. **validate_agents.py** - Configuration Validator
**Checks your agents for issues**

**Checks:**
- Required fields present
- Valid model names
- Valid tool names
- Proper JSON structure
- Empty fields
- Metrics completeness

**Usage:**
```bash
python validate_agents.py
```

**Output:**
```
✓ All agents validated successfully!
Total Agents: 12
Errors: 0
Warnings: 0
```

---

### 3. **templates/** - Agent Templates
**Pre-made templates for creating new agents**

Files:
- `agent_template.json` - JSON structure template
- `agent_instructions.md` - Markdown instructions template

**Usage:**
```bash
# Copy template
cp templates/agent_template.json my_agent.json

# Edit in your favorite editor
nano my_agent.json

# Or use the create wizard
python manage_agents.py create
```

---

## 🎓 Tutorial: Common Tasks

### Task 1: "I want to see what agents I have"
```bash
python manage_agents.py list
```
Shows brief list of all 12 agents with descriptions.

**Want more detail?**
```bash
python manage_agents.py list --detailed
```
Shows tools, capabilities, and performance metrics.

---

### Task 2: "I want to see everything about the security agent"
```bash
python manage_agents.py view security
```

**Shows:**
- Description and role
- Available tools (Read, Grep, Glob, Bash, Write)
- Capabilities (security_audit, owasp, cryptography, etc.)
- Full system prompt
- Performance metrics
- Success rate
- Last used

---

### Task 3: "I want to add a new tool to the designer agent"
```bash
python manage_agents.py edit designer
```

**What happens:**
1. Opens `designer` config in your editor (nano/vim/vscode)
2. Find the `"tools"` array
3. Add `"WebFetch"` to the list:
   ```json
   "tools": ["Read", "Write", "Edit", "Glob", "WebFetch"]
   ```
4. Save and exit
5. Confirm changes with `y`
6. Done!

**Verify:**
```bash
python manage_agents.py view designer
# Check Tools section
```

---

### Task 4: "I want to add a new capability"
```bash
python manage_agents.py edit data_analyst
```

1. Find `"capabilities"` array
2. Add new capability:
   ```json
   "capabilities": [
     "data_analysis",
     "data_visualization",
     "statistics",
     "machine_learning",  // Add this
     "deep_learning"      // And this
   ]
   ```
3. Save and confirm

---

### Task 5: "I want to change which AI model an agent uses"
```bash
python manage_agents.py edit researcher
```

Change the model:
```json
"model": "claude-opus-4"  // More powerful for complex research
```

**Available models:**
- `claude-haiku-4` - Fast, simple tasks
- `claude-sonnet-4-5` - Balanced (default)
- `claude-opus-4` - Most powerful, complex tasks

---

### Task 6: "I want to create a completely new agent"
```bash
python manage_agents.py create
```

**Guided wizard asks:**
1. Agent name (e.g., `prompt_engineer`)
2. Description (one line)
3. Role (what it does)
4. Model (haiku/sonnet/opus)
5. Tools (comma-separated)
6. Capabilities (comma-separated)
7. System prompt (detailed instructions)
8. Preview and confirm
9. Create .claude/agents file? (y/n)

**Result:**
- Agent added to registry.json
- Optional: .claude/agents/prompt_engineer.md created
- Ready to use immediately!

---

### Task 7: "I want to make sure my changes are valid"
```bash
# After editing
python validate_agents.py
```

**Checks:**
- JSON is valid
- All required fields present
- No typos in model names
- Tools are recognized
- Metrics structure correct

---

### Task 8: "I want to compare two similar agents"
```bash
python manage_agents.py compare code_writer designer
```

**Shows:**
- Shared tools
- Unique tools per agent
- Shared capabilities
- Unique capabilities
- Performance comparison

**Useful for:**
- Understanding agent differences
- Deciding which agent to use
- Avoiding duplicate agents

---

## 🎨 Interactive Mode Demo

The easiest way to explore:

```bash
python manage_agents.py
```

**Interactive session:**
```
===============================================================================
                        AGENT MANAGEMENT TOOL
===============================================================================

Available Commands:
  list              - List all agents (brief)
  list --detailed   - List all agents (detailed)
  view <name>       - View specific agent details
  edit <name>       - Edit agent configuration
  create            - Create new agent from template
  delete <name>     - Delete an agent
  compare <n1> <n2> - Compare two agents
  help              - Show this menu
  exit              - Exit

Examples:
  view designer
  edit security
  compare code_writer designer

> list
[Shows all agents]

> view designer
[Shows designer details]

> compare designer code_writer
[Shows comparison]

> exit
Goodbye!
```

---

## 📋 Agent Configuration Fields

When editing agents, here's what each field means:

```json
{
  "name": "agent_name",              // Internal identifier
  "description": "What it does",     // Brief description
  "role": "Primary responsibility",  // Main role
  "tools": ["Read", "Write"],        // Available tools
  "capabilities": ["python", "api"], // What it can do
  "system_prompt": "Instructions",   // Detailed prompt
  "model": "claude-sonnet-4-5",     // AI model to use
  "skill_level": "novice",          // Progress level
  "metrics": {                       // Performance tracking
    "total_tasks": 0,
    "successful_tasks": 0,
    "failed_tasks": 0,
    // ... more metrics
  }
}
```

---

## 🛠️ Available Tools for Agents

When editing `"tools"`, choose from:

| Tool | What It Does |
|------|--------------|
| **Read** | Read files |
| **Write** | Create new files |
| **Edit** | Modify existing files |
| **Glob** | Find files by pattern |
| **Grep** | Search file contents |
| **Bash** | Run terminal commands |
| **WebSearch** | Search the web |
| **WebFetch** | Fetch web pages |
| **TodoWrite** | Manage task lists |

**Examples:**
- **Analyst agents:** Read, Grep, Glob
- **Implementation agents:** Read, Write, Edit
- **Research agents:** WebSearch, WebFetch, Read
- **DevOps agents:** Bash, Read, Write, Edit

---

## 🎯 Choosing Capabilities

Capabilities help the system route tasks to the right agent.

**Use specific, searchable terms:**

✅ **Good capabilities:**
- `python`, `javascript`, `typescript`
- `api_design`, `rest`, `graphql`
- `security_audit`, `owasp`, `penetration_testing`
- `ui_design`, `responsive_design`, `accessibility`

❌ **Avoid vague terms:**
- `programming`
- `good_at_coding`
- `web_stuff`

---

## 🚨 Common Issues & Solutions

### Issue: "Agent not found"
**Problem:** Typo in agent name

**Solution:**
```bash
# Check exact names
python manage_agents.py list

# Use exact name (lowercase, underscores)
python manage_agents.py view code_writer  # ✓
python manage_agents.py view "Code Writer"  # ✗
```

---

### Issue: "Invalid JSON"
**Problem:** Syntax error in JSON

**Solution:**
```bash
# Validate
python validate_agents.py

# If broken, restore backup
cp agents/registry.json.backup agents/registry.json
```

---

### Issue: "Editor not opening"
**Problem:** No default editor set

**Solution:**
```bash
# Set editor
export EDITOR=nano
# Or
export EDITOR=vim
export EDITOR=code  # VS Code

# Then try again
python manage_agents.py edit my_agent
```

---

### Issue: "Changes not saving"
**Problem:** Didn't confirm changes

**Solution:**
- Always type `y` when prompted "Save changes?"
- Check for error messages
- Validate after editing: `python validate_agents.py`

---

## 💡 Pro Tips

### Tip 1: Always Backup Before Major Changes
```bash
cp agents/registry.json agents/registry.json.backup
```

### Tip 2: Validate After Every Edit
```bash
python manage_agents.py edit security
python validate_agents.py  # Always run this
```

### Tip 3: Use Interactive Mode for Exploration
```bash
python manage_agents.py
> list
> view designer
> view security
> compare designer security
```

### Tip 4: View Before Editing
```bash
python manage_agents.py view designer  # See current state
python manage_agents.py edit designer  # Then make changes
```

### Tip 5: Start Simple When Creating Agents
```bash
# Start with basic config
python manage_agents.py create

# Test it
python main.py agents

# Refine later
python manage_agents.py edit new_agent
```

---

## 📚 File Reference

| File | Purpose | When to Use |
|------|---------|-------------|
| `manage_agents.py` | Main tool | View/edit agents |
| `validate_agents.py` | Validator | After editing |
| `agents/registry.json` | Agent storage | Direct editing (advanced) |
| `templates/agent_template.json` | Template | Creating agents manually |
| `.claude/agents/*.md` | Instructions | Detailed agent prompts |

---

## 🎬 Example Session

Complete workflow:

```bash
# 1. See all agents
python manage_agents.py list

# 2. Check designer agent
python manage_agents.py view designer

# 3. Add WebFetch tool to designer
python manage_agents.py edit designer
# [Add "WebFetch" to tools array, save]

# 4. Validate changes
python validate_agents.py

# 5. Confirm it worked
python manage_agents.py view designer
# [Check Tools section includes WebFetch]

# 6. Test with the system
python main.py agents
# [Verify designer shows updated tools]
```

---

## 🎓 Next Steps

1. **Explore:** `python manage_agents.py list --detailed`
2. **Learn:** `python manage_agents.py view designer`
3. **Practice:** `python manage_agents.py edit designer`
4. **Validate:** `python validate_agents.py`
5. **Create:** `python manage_agents.py create`

---

## 📞 Quick Command Reference

```bash
# View agents
python manage_agents.py list
python manage_agents.py list --detailed
python manage_agents.py view <name>

# Edit agents
python manage_agents.py edit <name>
python manage_agents.py create
python manage_agents.py delete <name>

# Compare
python manage_agents.py compare <name1> <name2>

# Validate
python validate_agents.py

# Interactive
python manage_agents.py
```

---

**You now have complete control over your agent system!** 🎉

Start with `python manage_agents.py` and explore! 🚀
