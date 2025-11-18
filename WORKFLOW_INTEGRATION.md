# Workflow Integration Guide 🔄

Complete guide for using the integrated workflow system with the multi-agent orchestrator.

## Overview

The multi-agent orchestrator now includes intelligent workflow template matching. When you execute a task, the system automatically:

1. **Matches** the task to available workflow templates
2. **Selects** the best workflow (if match score ≥ threshold)
3. **Executes** the workflow with full tracking
4. **Records** execution history for learning
5. **Optimizes** workflows based on real usage data

## Quick Start

### Basic Usage (Workflow Enabled by Default)

```bash
# Execute a task - automatically uses workflows when matched
python main.py task "Build a weather app"

# The system will:
# - Find "web-app-development" workflow
# - Execute: Design → Implement → Test → Document
# - Track execution and learn from it
```

### Force Specific Workflow

```bash
# Force use of a specific workflow by name
python main.py task "Build calculator" --workflow web-app-development
```

### Disable Workflows (Use Direct Agent Selection)

```bash
# Skip workflow matching, use traditional agent selection
python main.py task "Debug authentication bug" --no-workflows
```

## How It Works

### 1. Task Submission

```bash
python main.py task "Create a todo list application"
```

### 2. Workflow Matching

The system searches for matching workflows:

```
🔍 Analyzing task...
💡 Matching Workflows (1):
   🟢 web-app-development (Score: 12, Relevance: high)
```

**Matching Algorithm**:
- Checks `task_types` keywords (weight: 10)
- Checks workflow name (weight: 5)
- Checks description words (weight: 2)
- Checks tags (weight: 3)
- Threshold: Score ≥ 5 (configurable)

### 3. Workflow Execution

```
🔄 WORKFLOW EXECUTION MODE
📋 Task: Create a todo list application
🔄 Workflow: web-app-development
👥 Required Agents: designer, code_writer, qa_tester
📋 Steps: 6
⏱️  Est. Duration: 30m

────────────────────────────────────────────────────────────────
📍 Step 1/6: Create Design Specifications
   Agent: designer | Required: Yes
   ✅ Step completed successfully

────────────────────────────────────────────────────────────────
📍 Step 2/6: Implement Application
   Agent: code_writer | Required: Yes
   ✅ Step completed successfully

... (more steps)

────────────────────────────────────────────────────────────────
📊 WORKFLOW EXECUTION SUMMARY
────────────────────────────────────────────────────────────────
Status: ✅ Success
Steps Completed: 6/6
Steps Failed: 0
Outputs Generated: 3
```

### 4. History Tracking

Execution saved to: `workflows/history/2025-01-17_web-app-development_20250117_143022.json`

### 5. Learning & Optimization

The system continuously learns:
- Step success rates
- Actual execution times
- Frequently skipped steps
- Common failure patterns

## Command-Line Options

### Task Execution

```bash
python main.py task "DESCRIPTION" [OPTIONS]
```

**Options:**

| Flag | Description | Default |
|------|-------------|---------|
| `--workflow NAME` | Force use of specific workflow | Auto-match |
| `--no-workflows` | Disable workflow matching | Enabled |
| `--max-agents N` | Max agents for non-workflow mode | 3 |
| `--no-tmux` | Execute without TMUX sessions | TMUX enabled |

### Examples

```bash
# Auto-match workflow
python main.py task "Build API documentation"

# Force specific workflow
python main.py task "Build web app" --workflow web-app-development

# Use direct agent selection (no workflows)
python main.py task "Fix bug in auth" --no-workflows

# Force workflow without TMUX
python main.py task "Create docs" --workflow documentation --no-tmux
```

## Available Workflows

### 1. web-app-development
**Triggers:** build web app, create website, develop ui, new web project

**Steps:**
1. Designer: Create design specifications
2. Code_writer: Implement application
3. Code_analyst: Code quality review (optional)
4. Security: Security audit (optional)
5. QA_tester: Quality assurance testing
6. Docs_writer: Create documentation

**Duration:** ~30 minutes

### 2. security-audit
**Triggers:** security audit, security review, vulnerability scan

**Steps:**
1. Code_analyst: Static code analysis
2. Security: Vulnerability assessment
3. Security: Penetration testing (optional)
4. Security: Generate security report
5. Docs_writer: Document findings (optional)

**Duration:** ~20 minutes

### 3. testing-suite
**Triggers:** test application, create tests, quality assurance

**Steps:**
1. QA_tester: Create test plan
2. QA_tester: Functional testing
3. QA_tester: UI testing
4. QA_tester: Integration testing
5. QA_tester: Edge case testing
6. QA_tester: Performance testing (optional)
7. QA_tester: Generate QA report
8. Docs_writer: Document testing procedures (optional)

**Duration:** ~25 minutes

### 4. documentation
**Triggers:** create documentation, write docs, document project

**Steps:**
1. Code_analyst: Analyze project
2. Docs_writer: Create README
3. Docs_writer: Create API docs (optional)
4. Docs_writer: Create user guide (optional)
5. Docs_writer: Create developer guide (optional)
6. Docs_writer: Create CHANGELOG (optional)
7. Docs_writer: Proof-read documentation

**Duration:** ~15 minutes

### 5. api-development
**Triggers:** design api, create api, build api, develop api

**Steps:**
1. API_expert: Design API specification
2. Code_writer: Implement API
3. Security: API security review
4. QA_tester: API testing
5. Docs_writer: Create API documentation
6. Code_writer: Create integration examples (optional)

**Duration:** ~40 minutes

## Workflow Management

### List All Workflows

```bash
python system/workflow-cli.py list
```

### Show Workflow Details

```bash
python system/workflow-cli.py show web-app-development
```

### Match Task to Workflow

```bash
python system/workflow-cli.py match "build a calculator"
```

### Preview Workflow

```bash
python system/workflow_executor.py preview web-app-development
```

## History & Analytics

### View Execution History

```python
from system.workflow_history import WorkflowHistory

history = WorkflowHistory()
stats = history.get_workflow_statistics("web-app-development")

print(f"Success Rate: {stats['success_rate']:.1%}")
print(f"Avg Duration: {stats['avg_duration']}s")
```

### Analyze Performance

```python
from system.workflow_learning import WorkflowLearner

learner = WorkflowLearner()
analysis = learner.analyze_workflow("web-app-development")

for improvement in analysis['improvements']:
    print(f"- {improvement['recommendation']}")
```

### Export Learning Report

```python
from system.workflow_learning import WorkflowLearner

learner = WorkflowLearner()
report_path = learner.export_learning_report()
print(f"Report saved to: {report_path}")
```

## Creating Custom Workflows

### Method 1: CLI

```bash
python system/workflow-cli.py create my-workflow \
  --description "Custom workflow for my use case"
```

This creates `workflows/templates/custom/my-workflow.yaml`

### Method 2: Copy and Edit

```bash
# Export existing workflow
python system/workflow-cli.py export web-app-development -o my-workflow.yaml

# Edit the file
# ... make changes ...

# Import back
python system/workflow-cli.py import my-workflow.yaml
```

### Method 3: Auto-Generate

The system can detect repeated patterns and suggest new workflows:

```python
from system.workflow_learning import WorkflowLearner

learner = WorkflowLearner()
patterns = learner.detect_task_patterns(min_occurrences=3)

# Review detected patterns
for pattern in patterns:
    print(f"Pattern: {pattern['keywords']}")
    print(f"Occurrences: {pattern['occurrences']}")
    print(f"Agent Sequence: {' → '.join(pattern['agent_sequence'])}")

    # Generate workflow
    workflow = learner.generate_workflow_template(pattern, "my-new-workflow")
    learner.save_learned_workflow(workflow)
```

## Integration with Orchestrator

### Programmatic Usage

```python
from agents import WorkflowOrchestrator

# Create workflow-enabled orchestrator
orchestrator = WorkflowOrchestrator(
    workspace_dir="workspace",
    enable_workflows=True,
    workflow_match_threshold=5
)

# Execute task (auto-matches workflows)
result = await orchestrator.execute_task(
    task_description="Build a calculator app",
    use_tmux=True
)

# Force specific workflow
result = await orchestrator.execute_task(
    task_description="Build docs",
    force_workflow="documentation"
)

# Skip workflows
result = await orchestrator.execute_task(
    task_description="Debug issue",
    skip_workflow=True
)
```

### Get Statistics

```python
# Workflow statistics
stats = orchestrator.get_workflow_statistics()
print(f"Total Executions: {stats['total_executions']}")
print(f"Success Rate: {stats['success_rate']:.1%}")

# Analyze specific workflow
analysis = orchestrator.analyze_workflow_performance("web-app-development")
print(f"Recommendations: {analysis['recommendation_count']}")

# Detect patterns
patterns = orchestrator.detect_workflow_patterns(min_occurrences=2)
print(f"Detected Patterns: {len(patterns)}")
```

## Configuration

### Adjust Match Threshold

```python
orchestrator = WorkflowOrchestrator(
    enable_workflows=True,
    workflow_match_threshold=10  # Higher = more strict matching
)
```

**Recommended Values:**
- `5`: Default (matches most relevant workflows)
- `10`: Strict (only high-relevance matches)
- `3`: Lenient (matches more workflows)

### Disable Workflows Globally

```python
orchestrator = WorkflowOrchestrator(
    enable_workflows=False  # Disable all workflow matching
)
```

## Troubleshooting

### Workflow Not Matching

**Problem:** Task doesn't match any workflow

**Solutions:**
1. Check available workflows: `python system/workflow-cli.py list`
2. Test matching: `python system/workflow-cli.py match "your task"`
3. Lower threshold: `workflow_match_threshold=3`
4. Add keywords to workflow `task_types`
5. Create custom workflow for your use case

### Workflow Fails Mid-Execution

**Problem:** Workflow stops at a step

**Solutions:**
1. Check execution history: `workflows/history/`
2. Review step requirements in workflow YAML
3. Verify agent is in registry: `python main.py agents`
4. Check step timeout (may need increase)
5. Make problematic step optional if not critical

### Wrong Workflow Selected

**Problem:** System chooses unexpected workflow

**Solutions:**
1. Use `--workflow NAME` to force correct one
2. Adjust workflow `task_types` keywords
3. Increase `workflow_match_threshold`
4. Use `--no-workflows` for direct agent selection

## Best Practices

### 1. Use Descriptive Task Descriptions

**Good:**
```bash
python main.py task "Build a responsive web application with user authentication"
```

**Less Good:**
```bash
python main.py task "Make app"  # Too vague for matching
```

### 2. Review Execution History

Regularly check `workflows/history/` to see:
- Which workflows are used most
- Where failures occur
- Performance trends

### 3. Optimize Based on Learning

```bash
# Generate learning report
python -c "from system.workflow_learning import WorkflowLearner; WorkflowLearner().export_learning_report()"

# Review recommendations in workflows/LEARNING_REPORT.md
# Adjust workflows based on insights
```

### 4. Create Custom Workflows for Repeated Tasks

If you do the same task 3+ times, create a workflow:
```bash
python system/workflow-cli.py create my-repeated-task
```

### 5. Use Quality Gates for Critical Steps

In workflow YAML:
```yaml
quality_gates:
  - name: all_tests_pass
    after_step: testing
    type: automatic
    condition: tests_passed
    required: true
```

## Advanced Features

### Conditional Execution

Skip optional steps based on context:

```python
result = await orchestrator.execute_task(
    task_description="Build app",
    context={'skip_optional_steps': True}
)
```

### Parallel Execution (Planned)

Future: Execute independent steps in parallel for speed.

### Workflow Versioning (Planned)

Future: Track workflow template versions and migrations.

### A/B Testing (Planned)

Future: Compare different workflow configurations.

## Support

- **Workflow CLI**: `python system/workflow-cli.py --help`
- **Executor**: `python system/workflow_executor.py --help`
- **Main CLI**: `python main.py --help`

---

**Now you have intelligent, self-improving workflow automation!** 🚀
