# Execution Modes Guide

The multi-agent orchestrator supports two execution modes to suit different workflows and use cases.

---

## Quick Start

### Independent Mode (Default)
Runs autonomously without user intervention:

```bash
python main.py task "Build a calculator app" --project my-calc
```

### Interactive Mode
Asks for approval and feedback at key checkpoints:

```bash
python main.py task "Build a calculator app" --project my-calc --mode interactive
```

---

## Mode Details

### Independent Mode 🤖

**Best for:**
- Production workflows
- Batch processing
- CI/CD pipelines
- Automated tasks
- When you trust the workflow completely

**Characteristics:**
- No user prompts or interruptions
- Autonomous decision-making
- Fast execution
- Automatic error recovery
- Logs all decisions

**Example:**
```bash
python main.py task "Create documentation for the API" \
  --project api-docs \
  --workflow documentation
```

---

### Interactive Mode 👤

**Best for:**
- Development and experimentation
- Learning new workflows
- High-stakes tasks requiring oversight
- When you want control over each step
- Debugging workflow issues

**Characteristics:**
- Plan presentation before execution
- Step-by-step approval
- Optional output review
- Error handling choices (retry/skip/abort)
- Clarification questions when needed

**Example:**
```bash
python main.py task "Build secure payment gateway" \
  --project payment-system \
  --workflow api-development \
  --mode interactive
```

---

## Interactive Mode Workflow

When you run in interactive mode, you'll encounter these checkpoints:

### 1. Plan Presentation

```
================================================================================
📋 EXECUTION PLAN
================================================================================

🔄 Workflow: web-app-development
📝 Complete workflow for building web applications

📋 Steps (6):
  1. ✓ Create Design Specifications (designer) [Required]
  2. ✓ Implement Application (code_writer) [Required]
  3. ○ Code Quality Review (code_analyst) [Optional]
  4. ○ Security Audit (security) [Optional]
  5. ✓ Quality Assurance Testing (qa_tester) [Required]
  6. ✓ Create Documentation (docs_writer) [Required]

👤 Approve this plan? (yes/no/modify):
```

**Options:**
- `yes` - Proceed with execution
- `no` - Cancel workflow
- `modify` - (Future feature) Adjust workflow parameters

---

### 2. Step Approval

Before each step executes:

```
📍 Step 1/6: Create Design Specifications
Agent: designer
Action: Create comprehensive UI/UX design specifications including:
- User interface layout and components
- Color scheme and typography
- Responsive design breakpoints
[...]

👤 Proceed with this step? (yes/no/skip):
```

**Options:**
- `yes` - Execute this step
- `no` - Abort workflow
- `skip` - Skip this step (only available for optional steps marked with ○)

---

### 3. Result Review

After step completion:

```
✅ Step completed successfully
📄 Generated files:
   - DESIGN.md (385 lines)

👤 Review output before continuing? (yes/no):
```

**Options:**
- `yes` - View output summary
- `no` - Continue to next step

---

### 4. Error Handling

If a step fails:

```
❌ Step failed: [error message]

👤 How to proceed? (retry/skip/abort):
```

**Options:**
- `retry` - Try the step again
- `skip` - Skip and continue (if step is optional)
- `abort` - Stop the entire workflow

---

## Mode Comparison

| Feature | Independent | Interactive |
|---------|-------------|-------------|
| **User Input** | None | Required at checkpoints |
| **Speed** | Fast | Slower (waiting for user) |
| **Control** | Low | High |
| **Best For** | Production | Development |
| **Error Recovery** | Automatic | User-guided |
| **Plan Visibility** | Logged only | Presented for approval |
| **Can Skip Steps** | No | Yes (optional steps only) |
| **Learning Curve** | None | See workflow in action |

---

## Usage Examples

### Example 1: Build a Web Application

**Independent (Fast):**
```bash
python main.py task "Build a todo list app with drag-and-drop" \
  --project todo-app \
  --workflow web-app-development
```
Completes in ~15-30 minutes autonomously.

**Interactive (Controlled):**
```bash
python main.py task "Build a todo list app with drag-and-drop" \
  --project todo-app \
  --workflow web-app-development \
  --mode interactive
```
Takes longer but you approve each phase (design, implementation, testing, docs).

---

### Example 2: Security Audit

**Independent:**
```bash
python main.py task "Security audit of authentication system" \
  --project auth-audit \
  --workflow security-audit
```

**Interactive (Recommended for Security):**
```bash
python main.py task "Security audit of authentication system" \
  --project auth-audit \
  --workflow security-audit \
  --mode interactive
```
Review findings immediately and decide which issues to investigate deeper.

---

### Example 3: API Development

**Independent:**
```bash
python main.py task "Create REST API for user management" \
  --project user-api \
  --workflow api-development
```

**Interactive:**
```bash
python main.py task "Create REST API for user management" \
  --project user-api \
  --workflow api-development \
  --mode interactive
```
Approve API design before implementation, review endpoints before testing.

---

## Tips & Best Practices

### When to Use Independent Mode
- ✅ Repeated tasks you understand well
- ✅ Overnight batch jobs
- ✅ CI/CD automated workflows
- ✅ Simple, well-defined tasks
- ✅ When you trust the agent capabilities

### When to Use Interactive Mode
- ✅ First time using a workflow
- ✅ Complex multi-step projects
- ✅ High-risk or critical tasks
- ✅ Learning how workflows function
- ✅ When requirements may need adjustment
- ✅ Debugging workflow issues

### Switching Modes
You can run the same task in both modes:

```bash
# First run: interactive to understand workflow
python main.py task "Build feature X" --project app --mode interactive

# After understanding: independent for speed
python main.py task "Build feature Y" --project app
```

---

## Advanced Usage

### With Specific Agents
```bash
python main.py task "Complex task" \
  --project my-project \
  --mode interactive \
  --max-agents 5
```

### With Workflow Override
```bash
python main.py task "Build app" \
  --project my-app \
  --workflow web-app-development \
  --mode interactive
```

### Without Workflows (Direct Agent Selection)
```bash
python main.py task "Simple task" \
  --project quick-test \
  --no-workflows \
  --mode independent
```

---

## Troubleshooting

### "Workflow stuck waiting for input"
- You're in interactive mode - check terminal for prompts
- Response required: yes/no/skip/retry/abort
- Press Ctrl+C to abort if needed

### "Want to run without interruptions"
- Use independent mode (default)
- Or omit `--mode` parameter entirely

### "Want to see what the orchestrator is doing"
- Use interactive mode: `--mode interactive`
- Review execution plan before it starts
- Approve each step to see progress

### "Made a mistake approving a step"
- Press Ctrl+C to abort current step
- Or let it complete and fix in next run
- Future: undo/rollback feature planned

---

## Future Enhancements

Planned features for interactive mode:

- [ ] Rich UI with colored prompts (using `rich` library)
- [ ] Step modification (change parameters mid-workflow)
- [ ] Partial automation (pre-approve specific steps)
- [ ] Save approval patterns for future runs
- [ ] Dry-run mode (preview without execution)
- [ ] Undo/rollback failed steps
- [ ] Interactive timeout (auto-approve after delay)
- [ ] Multi-user approval (team workflows)

---

## Summary

**Independent Mode**: Fast, autonomous, production-ready
**Interactive Mode**: Controlled, educational, development-friendly

Start with **interactive** to learn, switch to **independent** for speed.

---

For detailed test results and technical implementation, see [EXECUTION_MODES_TEST_REPORT.md](EXECUTION_MODES_TEST_REPORT.md)

**Generated**: 2025-01-17
**Version**: 1.0.0
