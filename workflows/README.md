# Workflow Templates 🔄

Structured, repeatable processes for the multi-agent orchestrator system.

## Overview

Workflow templates define sequences of agent actions that accomplish specific types of tasks. They ensure consistency, quality, and best practices across all projects.

## Quick Start

### List Available Workflows

```bash
python system/workflow-cli.py list
```

### View Workflow Details

```bash
python system/workflow-cli.py show web-app-development
```

### Match Workflow to Task

```bash
python system/workflow-cli.py match "build a web app"
```

### Show Statistics

```bash
python system/workflow-cli.py stats
```

## Available Workflows

### 1. 🌐 Web App Development
**File:** `templates/web-app-development.yaml`

Complete workflow for building web applications from design to deployment.

**Steps:**
1. Design (designer) - Create UI/UX specifications
2. Implement (code_writer) - Build the application
3. Code Review (code_analyst) - Review code quality
4. Security Check (security) - Security audit
5. Testing (qa_tester) - Quality assurance
6. Documentation (docs_writer) - Create README

**Triggers:** build web app, create website, develop ui, new web project

**Duration:** ~30 minutes

### 2. 🔒 Security Audit
**File:** `templates/security-audit.yaml`

Comprehensive security audit workflow for applications and code.

**Steps:**
1. Code Analysis (code_analyst) - Static analysis
2. Vulnerability Scan (security) - OWASP Top 10 assessment
3. Penetration Test (security) - Simulated attacks
4. Security Report (security) - Comprehensive report
5. Documentation (docs_writer) - Security guide

**Triggers:** security audit, security review, vulnerability scan

**Duration:** ~20 minutes

### 3. ✓ Testing Suite
**File:** `templates/testing-suite.yaml`

Comprehensive testing workflow covering all testing types.

**Steps:**
1. Test Plan (qa_tester) - Create test strategy
2. Functional Testing (qa_tester) - Feature testing
3. UI Testing (qa_tester) - UI/UX validation
4. Integration Testing (qa_tester) - Component interactions
5. Edge Case Testing (qa_tester) - Error scenarios
6. Performance Testing (qa_tester) - Performance metrics
7. Final Report (qa_tester) - Comprehensive QA report
8. Documentation (docs_writer) - Testing guide

**Triggers:** test application, create tests, quality assurance

**Duration:** ~25 minutes

### 4. 📝 Documentation
**File:** `templates/documentation.yaml`

Comprehensive documentation creation workflow.

**Steps:**
1. Analyze Project (code_analyst) - Understand project
2. README (docs_writer) - Create README.md
3. API Docs (docs_writer) - API documentation
4. User Guide (docs_writer) - User manual
5. Developer Guide (docs_writer) - Developer docs
6. CHANGELOG (docs_writer) - Version history
7. Proof-read (docs_writer) - Review all docs

**Triggers:** create documentation, write docs, document project

**Duration:** ~15 minutes

### 5. 🔌 API Development
**File:** `templates/api-development.yaml`

Complete workflow for designing, implementing, and documenting APIs.

**Steps:**
1. API Design (api_expert) - Design specification
2. Implement API (code_writer) - Build endpoints
3. Security Review (security) - API security audit
4. API Testing (qa_tester) - Comprehensive testing
5. API Documentation (docs_writer) - API docs
6. Integration Examples (code_writer) - Example code

**Triggers:** design api, create api, build api, develop api

**Duration:** ~40 minutes

## Creating Custom Workflows

### Method 1: Use CLI

```bash
python system/workflow-cli.py create my-workflow --description "My custom workflow"
```

This creates a template in `workflows/templates/custom/my-workflow.yaml` that you can edit.

### Method 2: Copy Existing Workflow

```bash
# Export existing workflow
python system/workflow-cli.py export web-app-development -o my-workflow.yaml

# Edit the file
# Import as custom workflow
python system/workflow-cli.py import my-workflow.yaml
```

### Method 3: Create from Scratch

Create a YAML file in `workflows/templates/custom/`:

```yaml
name: my-custom-workflow
version: 1.0.0
description: Description of what this workflow does
author: your-name
created: 2025-01-17
updated: 2025-01-17

task_types:
  - trigger keyword 1
  - trigger keyword 2

agents_required:
  - agent_name

steps:
  - id: step1
    name: Step Name
    agent: agent_name
    action: |
      What the agent should do...
    required: true
    outputs:
      - OUTPUT_FILE.md
    validation:
      - type: output_exists
        file: OUTPUT_FILE.md

hooks:
  post_workflow:
    - action: git_commit
      description: Commit changes

tags:
  - tag1
  - tag2
priority: high
usage_count: 0
success_rate: 0.0
estimated_duration: 600
```

## Workflow CLI Commands

### List Workflows

```bash
python system/workflow-cli.py list                  # List all workflows
python system/workflow-cli.py list -d               # Detailed view
python system/workflow-cli.py list -c               # Custom only
```

### Show Workflow

```bash
python system/workflow-cli.py show WORKFLOW_NAME
```

### Create Workflow

```bash
python system/workflow-cli.py create WORKFLOW_NAME
python system/workflow-cli.py create WORKFLOW_NAME -d "Description"
python system/workflow-cli.py create WORKFLOW_NAME --no-interactive
```

### Edit Workflow

```bash
python system/workflow-cli.py edit WORKFLOW_NAME
```

Opens the workflow in your default editor (set via `$EDITOR`).

### Validate Workflow

```bash
python system/workflow-cli.py validate WORKFLOW_NAME
```

Checks for:
- Required fields
- Step structure
- Valid dependencies
- Proper validation rules

### Delete Workflow

```bash
python system/workflow-cli.py delete WORKFLOW_NAME
python system/workflow-cli.py delete WORKFLOW_NAME -f    # Force, skip confirmation
```

**Note:** Only custom workflows can be deleted.

### Export Workflow

```bash
python system/workflow-cli.py export WORKFLOW_NAME
python system/workflow-cli.py export WORKFLOW_NAME -f json
python system/workflow-cli.py export WORKFLOW_NAME -o output.yaml
```

### Import Workflow

```bash
python system/workflow-cli.py import workflow.yaml
python system/workflow-cli.py import workflow.json --system   # Import as system workflow
```

### Statistics

```bash
python system/workflow-cli.py stats
```

Shows:
- Total workflows
- System vs custom
- Usage statistics
- Success rates
- Popular tags
- Most used workflows

### Match Workflow

```bash
python system/workflow-cli.py match "TASK DESCRIPTION"
```

Finds workflows that match the task description.

## Workflow Structure

### Required Fields

```yaml
name: workflow-name         # Unique identifier
version: 1.0.0             # Semantic versioning
description: "..."         # What the workflow does
steps: []                  # List of workflow steps
```

### Recommended Fields

```yaml
author: system             # Who created it
created: 2025-01-17       # Creation date
updated: 2025-01-17       # Last update
task_types: []            # Keywords that trigger this workflow
agents_required: []       # Agents needed for this workflow
priority: high            # Priority level (high/medium/low)
tags: []                  # Categorization tags
estimated_duration: 600   # Seconds
```

### Step Structure

```yaml
steps:
  - id: unique_step_id               # Unique identifier
    name: Human-Readable Name        # Display name
    agent: agent_name                # Which agent performs this
    action: |                        # What the agent should do
      Multi-line description
      of the action
    required: true                   # Is this step mandatory?
    depends_on: [other_step_id]     # Dependencies
    inputs: [FILE.md]                # Input files
    outputs: [OUTPUT.md]             # Output files
    timeout: 300                     # Timeout in seconds
    validation:                      # Validation rules
      - type: output_exists
        file: OUTPUT.md
      - type: min_lines
        file: OUTPUT.md
        value: 50
```

### Hooks

```yaml
hooks:
  pre_workflow:              # Before workflow starts
    - action: check_git_status
      description: Ensure clean git state

  post_workflow:             # After workflow completes
    - action: git_commit
      description: Commit changes
      message: "Workflow complete"

  on_error:                  # On failure
    - action: rollback
      description: Revert changes
```

### Quality Gates

```yaml
quality_gates:
  - name: design_approval
    after_step: design
    type: manual              # manual or automatic
    description: User reviews design
    required: false

  - name: all_tests_pass
    after_step: testing
    type: automatic
    condition: tests_passed
    required: true
```

### Validation Types

- `output_exists`: Check if file was created
- `min_lines`: Minimum number of lines
- `max_lines`: Maximum number of lines
- `syntax_valid`: Check syntax (requires language)
- `custom`: Custom validation logic

## Integration with Orchestrator

The orchestrator automatically:

1. **Analyzes the task** - Extracts keywords and intent
2. **Finds matching workflows** - Based on task_types
3. **Ranks workflows** - Scores by relevance
4. **Selects best match** - Chooses highest-scoring workflow
5. **Executes workflow** - Runs steps in order
6. **Validates outputs** - Checks quality gates
7. **Runs hooks** - Pre/post workflow actions
8. **Logs execution** - Saves to history for learning

### Example

```python
# User task: "Build a weather app"
# Orchestrator matches: web-app-development workflow
# Executes:
#   1. Designer creates DESIGN.md
#   2. Code_writer implements index.html
#   3. QA_tester tests functionality
#   4. Docs_writer creates README.md
#   5. Hooks: Proof-read → Git commit
# Result: Complete, tested, documented app
```

## Learning System

The workflow system learns from execution:

### What It Tracks

- Step success/failure rates
- Step execution durations
- User modifications to workflows
- Common task patterns
- Validation failures

### How It Improves

- **Optimizes step order** - Reorders steps for efficiency
- **Adjusts timeouts** - Updates based on actual durations
- **Refines validation** - Improves quality checks
- **Suggests new workflows** - Creates workflows from repeated patterns

### Auto-Generated Workflows

When the system detects repeated task patterns (e.g., user always runs security audit after implementation), it:

1. Recognizes the pattern
2. Generates a workflow template
3. Saves to `workflows/learned/`
4. Suggests to user for approval
5. Moves to custom workflows if approved

## Directory Structure

```
workflows/
├── README.md                          # This file
├── templates/                         # Workflow definitions
│   ├── web-app-development.yaml      # Web app workflow
│   ├── security-audit.yaml           # Security workflow
│   ├── testing-suite.yaml            # Testing workflow
│   ├── documentation.yaml            # Documentation workflow
│   ├── api-development.yaml          # API workflow
│   └── custom/                       # User-defined workflows
│       └── my-workflow.yaml
├── learned/                          # Auto-generated workflows
│   └── pattern-based-workflow.yaml
└── history/                          # Execution logs
    └── 2025-01-17_workflow-run.json
```

## Best Practices

### Workflow Design

1. **Keep steps focused** - Each step should do one thing well
2. **Define clear dependencies** - Use `depends_on` for ordering
3. **Add validation** - Ensure outputs meet quality standards
4. **Use hooks** - Automate common pre/post actions
5. **Set realistic timeouts** - Allow enough time for agents
6. **Document actions** - Write clear action descriptions

### Step Actions

- Be specific about what the agent should do
- Include success criteria
- List required outputs
- Mention any constraints
- Reference input files

### Validation Rules

- Always validate critical outputs
- Check for both existence and quality
- Use multiple validation types
- Set appropriate thresholds

### Quality Gates

- Add gates for critical checkpoints
- Use manual gates for user approvals
- Use automatic gates for quality checks
- Make gates appropriate to priority

## Troubleshooting

### Workflow Not Matching Task

Check `task_types` in the workflow. Add keywords that describe when this workflow should be used.

```bash
python system/workflow-cli.py show WORKFLOW_NAME
python system/workflow-cli.py match "your task description"
```

### Step Failing

1. Check step timeout - may need to increase
2. Verify agent is available
3. Check dependencies are satisfied
4. Review validation rules

### Validation Errors

```bash
python system/workflow-cli.py validate WORKFLOW_NAME
```

Fix any errors reported.

### Editing Workflows

```bash
# Edit with default editor
python system/workflow-cli.py edit WORKFLOW_NAME

# Or manually
$EDITOR workflows/templates/WORKFLOW_NAME.yaml
```

## Examples

### Simple 2-Step Workflow

```yaml
name: quick-prototype
version: 1.0.0
description: Quick prototype without testing
task_types: [quick prototype, fast prototype]
agents_required: [designer, code_writer]

steps:
  - id: design
    name: Quick Design
    agent: designer
    action: Create simple design mockup
    required: true
    outputs: [DESIGN.md]

  - id: implement
    name: Build Prototype
    agent: code_writer
    action: Implement basic prototype
    required: true
    depends_on: [design]
    outputs: [prototype.html]

tags: [prototype, fast]
priority: low
estimated_duration: 300
```

### Complex Multi-Agent Workflow

See `templates/web-app-development.yaml` for a full example with:
- 6 steps
- Multiple agents
- Dependencies
- Validation rules
- Quality gates
- Pre/post hooks

## Contributing

To contribute a workflow:

1. Create your workflow in `templates/custom/`
2. Test thoroughly
3. Validate: `python system/workflow-cli.py validate WORKFLOW_NAME`
4. Export: `python system/workflow-cli.py export WORKFLOW_NAME`
5. Submit for inclusion in system templates

## Resources

- [WORKFLOW_SYSTEM.md](../WORKFLOW_SYSTEM.md) - Complete system architecture
- [Workflow Schema](../WORKFLOW_SYSTEM.md#workflow-schema-yaml) - Full YAML spec
- [Agent Registry](../.claude/agents/registry.json) - Available agents

---

**Transform your multi-agent orchestrator into an intelligent process automation platform!** 🚀
