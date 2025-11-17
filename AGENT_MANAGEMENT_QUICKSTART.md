# Agent Management - Quick Start Guide

Easy tools for viewing and editing agent configurations.

---

## 🚀 Quick Commands

```bash
# Interactive mode (recommended for beginners)
python manage_agents.py

# Or direct commands
python manage_agents.py list
python manage_agents.py view designer
python manage_agents.py edit security
```

---

## 📋 Management Tool Features

### 1. List All Agents
```bash
# Brief list
python manage_agents.py list

# Detailed list with metrics
python manage_agents.py list --detailed
```

**Output:**
```
1. CODE_ANALYST
   Description: Expert in code analysis, architecture review
   Role: Analyzes code structure, identifies issues
   Model: claude-sonnet-4-5
   Skill Level: novice
```

---

### 2. View Agent Details
```bash
python manage_agents.py view designer
```

**Shows:**
- Basic information
- Available tools
- Capabilities
- Full system prompt
- Performance metrics
- Success rate
- Last used date

---

### 3. Edit Agent
```bash
python manage_agents.py edit security
```

**What happens:**
1. Opens agent config in your editor (nano/vim/$EDITOR)
2. Make changes
3. Save and exit
4. Confirm changes
5. Updates registry.json

**Edit fields:**
- Description
- Role
- Tools
- Capabilities
- System prompt
- Model
- Skill level

---

### 4. Create New Agent
```bash
python manage_agents.py create
```

**Guided wizard:**
1. Enter agent name
2. Enter description
3. Enter role
4. Select model
5. Choose tools
6. Define capabilities
7. Write system prompt
8. Preview and confirm
9. Optional: Create .claude/agents instruction file

---

### 5. Delete Agent
```bash
python manage_agents.py delete agent_name
```

**Safely removes:**
- Agent from registry.json
- Optional: .claude/agents instruction file

---

### 6. Compare Agents
```bash
python manage_agents.py compare code_writer designer
```

**Shows:**
- Shared tools and capabilities
- Unique tools per agent
- Performance comparison
- Success rates

---

## 🔍 Validation Tool

Check for configuration issues:

```bash
python validate_agents.py
```

**Checks:**
- Required fields present
- Valid model names
- Valid skill levels
- Valid tools
- Proper JSON structure
- Metrics completeness
- Empty fields

**Output:**
```
=== Agent Configuration Validator ===

Agent: designer
  ✓ All fields valid

Agent: security
  ⚠ WARNING: System prompt is very short (45 chars)

Summary:
  Total Agents: 12
  Agents with Issues: 1
  Errors: 0
  Warnings: 1

⚠ Validation completed with warnings
```

---

## 📁 Templates

Pre-made templates for creating agents:

### JSON Template
```bash
cp templates/agent_template.json my_new_agent.json
# Edit the file
# Add to registry manually or use create command
```

### Markdown Instructions Template
```bash
cp templates/agent_instructions.md .claude/agents/my_agent.md
# Edit with your agent's instructions
```

---

## 🎨 Interactive Mode

Start interactive mode:
```bash
python manage_agents.py
```

**Available commands:**
- `list` - List all agents
- `list --detailed` - Detailed list
- `view <name>` - View agent details
- `edit <name>` - Edit agent
- `create` - Create new agent
- `delete <name>` - Delete agent
- `compare <agent1> <agent2>` - Compare agents
- `help` - Show help
- `exit` - Exit

**Example session:**
```
> list
[Shows all agents]

> view designer
[Shows designer details]

> edit designer
[Opens in editor]

> exit
```

---

## 🛠️ Common Tasks

### Task 1: View All Agents with Performance
```bash
python manage_agents.py list --detailed
```

### Task 2: Check Specific Agent Before Editing
```bash
python manage_agents.py view security
```

### Task 3: Edit Agent Tools
```bash
# Opens editor
python manage_agents.py edit security

# Add "WebFetch" to tools array:
"tools": ["Read", "Grep", "Glob", "Bash", "Write", "WebFetch"]

# Save and confirm
```

### Task 4: Add New Capability
```bash
python manage_agents.py edit data_analyst

# Add to capabilities:
"capabilities": [
  "data_analysis",
  "data_visualization",
  "statistics",
  "pandas",
  "numpy",
  "sql",
  "reporting",
  "new_capability_here"  # Add this
]
```

### Task 5: Change Agent Model
```bash
python manage_agents.py edit researcher

# Change model:
"model": "claude-opus-4"  # For more complex research tasks
```

### Task 6: Create Specialized Agent
```bash
python manage_agents.py create

# Follow wizard:
Name: prompt_engineer
Description: Expert in crafting effective AI prompts
Role: Designs and optimizes prompts for AI systems
Model: claude-sonnet-4-5
Tools: Read, Write, Edit
Capabilities: prompt_engineering, ai_systems, optimization
System prompt: [Write detailed instructions]
```

### Task 7: Validate After Changes
```bash
# Make changes
python manage_agents.py edit security

# Validate
python validate_agents.py
```

---

## 📊 Understanding Agent Metrics

When viewing agents, you'll see metrics:

```
Performance:
  Tasks: 5
  Success: 4
  Failed: 1
  Success Rate: 80.0%
  Avg Time: 2.34s
  Total Cost: $0.0150
  Last Used: 2025-11-16T22:58:24
```

**Metrics explained:**
- **Tasks**: Total tasks assigned to agent
- **Success**: Successfully completed tasks
- **Failed**: Failed or errored tasks
- **Success Rate**: Percentage of successful tasks
- **Avg Time**: Average execution time in seconds
- **Total Cost**: Total API cost (if applicable)
- **Last Used**: Timestamp of last use

---

## 🎯 Best Practices

### 1. Always Validate After Editing
```bash
python manage_agents.py edit my_agent
python validate_agents.py
```

### 2. View Before Editing
```bash
python manage_agents.py view my_agent  # Check current state
python manage_agents.py edit my_agent   # Then edit
```

### 3. Backup Registry Before Major Changes
```bash
cp agents/registry.json agents/registry.json.backup
```

### 4. Keep System Prompts Focused
- 100-500 words ideal
- Clear structure
- Specific instructions
- Examples when helpful

### 5. Choose Right Tools for Agent
- **Analysis**: Read, Grep, Glob
- **Implementation**: Read, Write, Edit
- **Research**: WebSearch, WebFetch, Read
- **Testing**: Bash, Read, Grep
- **DevOps**: Bash, Read, Write, Edit

### 6. Define Clear Capabilities
Use specific, searchable terms:
- Good: `api_design`, `rest`, `graphql`
- Avoid: `good_at_apis`, `knows_web_stuff`

---

## 🐛 Troubleshooting

### "Agent not found"
```bash
# Check agent name
python manage_agents.py list

# Use exact name (lowercase, underscores)
python manage_agents.py view code_writer  # ✓ Correct
python manage_agents.py view "Code Writer"  # ✗ Wrong
```

### "Invalid JSON"
```bash
# Validate
python validate_agents.py

# If corrupted, restore backup
cp agents/registry.json.backup agents/registry.json
```

### "Editor not opening"
```bash
# Set your preferred editor
export EDITOR=nano
python manage_agents.py edit my_agent

# Or
export EDITOR=vim
export EDITOR=code  # VS Code
```

### Changes not saving
- Make sure to confirm with 'y' when prompted
- Check file permissions on agents/registry.json
- Ensure JSON is valid (use validator)

---

## 📝 File Locations

```
Multi-agent-v2/
├── manage_agents.py              # Main management tool
├── validate_agents.py            # Validation tool
├── agents/
│   └── registry.json            # Agent configurations (MAIN)
├── .claude/
│   └── agents/
│       ├── code_analyst.md      # Agent instructions
│       └── code_writer.md       # Agent instructions
└── templates/
    ├── agent_template.json      # JSON template
    └── agent_instructions.md    # Markdown template
```

---

## 🎓 Learning Path

### Beginner
1. `python manage_agents.py list` - See all agents
2. `python manage_agents.py view designer` - View one agent
3. `python manage_agents.py list --detailed` - See metrics

### Intermediate
1. `python manage_agents.py edit security` - Edit existing agent
2. `python validate_agents.py` - Validate changes
3. `python manage_agents.py compare code_writer designer` - Compare agents

### Advanced
1. `python manage_agents.py create` - Create new agent
2. Edit `agents/task_router.py` - Customize routing
3. Create custom `.claude/agents/*.md` files

---

## 💡 Pro Tips

1. **Use interactive mode for exploration**
   ```bash
   python manage_agents.py
   > view designer
   > view security
   > compare designer security
   ```

2. **Chain commands for workflow**
   ```bash
   python manage_agents.py view security && \
   python manage_agents.py edit security && \
   python validate_agents.py
   ```

3. **Quick check before running tasks**
   ```bash
   python manage_agents.py list --detailed | grep -A 10 "designer"
   ```

4. **Export agent config for sharing**
   ```bash
   cat agents/registry.json | jq '.designer' > designer_agent.json
   ```

5. **Search for agents by capability**
   ```bash
   cat agents/registry.json | jq 'to_entries[] | select(.value.capabilities[] | contains("security")) | .key'
   ```

---

## 🚀 Quick Reference Card

```
COMMAND                              ACTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
python manage_agents.py              Interactive mode
python manage_agents.py list         List all agents
python manage_agents.py view NAME    View agent details
python manage_agents.py edit NAME    Edit agent config
python manage_agents.py create       Create new agent
python manage_agents.py delete NAME  Delete agent
python manage_agents.py compare A B  Compare agents
python validate_agents.py            Validate configs

FILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
agents/registry.json                 Agent configs
.claude/agents/*.md                  Agent instructions
templates/                           Templates
```

---

**Ready to manage agents!** Start with `python manage_agents.py` 🎉
