# Debugging Checklist - Claude CLI File Creation

## Quick Start for Next Session

**Goal**: Fix Claude CLI execution so files are actually created

**Current Status**: Process runs but no files appear (0 expected, 1+ actual)

## Pre-Debug Verification

```bash
# 1. Verify Claude CLI works independently
cd /tmp && echo "Create index.html with Hello World" | claude --print --allowed-tools Write
# Expected: ✅ Creates /tmp/index.html

# 2. Check current codebase
cd /Users/dglickman@bgrove.com/Multi-agent-v2
git status
# Should show: main branch, 8 commits ahead

# 3. Review implementation
cat agents/orchestrator.py | grep -A 30 "Execute claude with stdin"
```

## Debugging Steps (Priority Order)

### 1. Add Verbose Logging (15 min)

**File**: `agents/orchestrator.py:323-333`

Add logging after Claude CLI execution:

```python
if process.returncode == 0:
    # ADD THIS:
    print(f"    📤 stdout: {stdout.decode('utf-8', errors='ignore')[:500]}")
    print(f"    📤 stderr: {stderr.decode('utf-8', errors='ignore')[:500]}")
    print(f"    📁 cwd: {agent_workspace}")

    # Success - check for created files
    created_files = list(agent_workspace.glob('**/*'))
else:
    # ADD THIS:
    print(f"    ❌ Return code: {process.returncode}")
    print(f"    📤 stdout: {stdout.decode('utf-8', errors='ignore')}")
    print(f"    📤 stderr: {stderr.decode('utf-8', errors='ignore')}")
```

**Test**:
```bash
python main.py task "Create index.html" --project debug1 --no-workflows --max-agents 1
```

**Expected Output**: See what Claude is actually returning

---

### 2. Test Without Tool Restrictions (10 min)

**File**: `agents/orchestrator.py:301-307`

Temporarily remove tool restrictions:

```python
# Build command arguments
cmd_args = ['claude', '--print']

# COMMENT OUT:
# if agent.tools:
#     cmd_args.append('--allowed-tools')
#     cmd_args.append(' '.join(agent.tools))
```

**Test**:
```bash
python main.py task "Create index.html" --project debug2 --no-workflows --max-agents 1
```

**If this works**: Tool restriction format is the issue

---

### 3. Test with Simpler Prompt (10 min)

Replace full agent instructions with simple prompt:

**File**: `agents/orchestrator.py:272-291`

```python
# COMMENT OUT full_prompt generation
# full_prompt = f"""{agent_instructions}...

# USE SIMPLE PROMPT:
full_prompt = f"""Create a file called index.html with a simple HTML structure containing an h1 tag that says "Hello World"."""
```

**Test**:
```bash
python main.py task "test" --project debug3 --no-workflows --max-agents 1
```

**If this works**: Agent instructions format is the issue

---

### 4. Test Working Directory (10 min)

Verify files are being created in the right place:

```python
# After Claude execution:
print(f"    📁 Working dir: {agent_workspace}")
print(f"    📁 Absolute path: {agent_workspace.absolute()}")
print(f"    📁 Exists: {agent_workspace.exists()}")
print(f"    📁 Is dir: {agent_workspace.is_dir()}")

# List ALL files in workspace:
all_files = list(agent_workspace.rglob('*'))
print(f"    📄 All files in workspace: {[str(f) for f in all_files]}")
```

**Test**:
```bash
python main.py task "Create index.html" --project debug4 --no-workflows --max-agents 1
ls -la projects/debug4/
```

---

### 5. Compare Working vs Non-Working (15 min)

**Working command** (verified):
```bash
cd projects/debug5 && echo "Create index.html with Hello World" | claude --print --allowed-tools Write
ls -la projects/debug5/
```

**Non-working command** (current implementation):
```python
process = await asyncio.create_subprocess_exec(
    'claude', '--print', '--allowed-tools', 'Read Write Edit Glob',
    stdin=PIPE, stdout=PIPE, stderr=PIPE,
    cwd=str(agent_workspace)
)
```

**Key differences to check:**
- Tool format: "Read Write Edit Glob" vs individual args?
- Working directory vs cd?
- Stdin encoding?
- Environment variables?

---

### 6. Test with strace/dtrace (Advanced, 20 min)

If still not working, trace the actual system calls:

```bash
# On macOS:
cd projects/debug6
dtruss -f claude --print --allowed-tools Write < full_prompt.txt 2>&1 | grep -E "write|open|create"

# Check what files it's trying to create
```

---

## Quick Fixes to Try

### Fix 1: Tool Format
```python
# Current:
cmd_args.append(' '.join(agent.tools))  # "Read Write Edit Glob"

# Try:
for tool in agent.tools:
    cmd_args.append(tool)  # ['Read', 'Write', 'Edit', 'Glob']
```

### Fix 2: Environment Variables
```python
# Add env parameter:
process = await asyncio.create_subprocess_exec(
    *cmd_args,
    stdin=PIPE, stdout=PIPE, stderr=PIPE,
    cwd=str(agent_workspace),
    env={**os.environ, 'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY')}
)
```

### Fix 3: Shell Execution
```python
# Try with shell=True:
cmd = f"cd {agent_workspace} && claude --print --allowed-tools Write"
process = await asyncio.create_subprocess_shell(
    cmd,
    stdin=PIPE, stdout=PIPE, stderr=PIPE
)
```

---

## Success Criteria

✅ Command: `python main.py task "Create index.html" --project test-success --no-workflows`

✅ Expected output:
```
✅ Agent completed successfully
📄 Files created: 1
```

✅ Verify: `cat projects/test-success/index.html` shows HTML content

---

## If Still Stuck

### Alternative Approach: Hybrid Execution

Instead of subprocess, use file-based communication:

```python
# Write prompt to file
prompt_file = agent_workspace / "task.txt"
prompt_file.write_text(full_prompt)

# Execute with file input
cmd = f"cd {agent_workspace} && claude --print --allowed-tools Write < task.txt > output.txt 2> error.txt"
subprocess.run(cmd, shell=True)

# Read results
output = (agent_workspace / "output.txt").read_text()
errors = (agent_workspace / "error.txt").read_text()
```

---

## Time Estimates

- Quick logging: 15 min
- Tool restrictions test: 10 min
- Simple prompt test: 10 min
- Working dir verification: 10 min
- Comparison debugging: 15 min

**Total estimated time: 1 hour**

---

## Resources

- Implementation: `agents/orchestrator.py:300-350`
- Test projects: `projects/debug*/`
- Documentation: `IMPLEMENTATION_STATUS.md`
- Claude CLI: `claude --help`

---

**Remember**: The infrastructure is 100% complete. This is just debugging the CLI invocation. Once files are created, everything else works!

**Last Known Working State**: `echo "..." | claude --print --allowed-tools Write` ✅
