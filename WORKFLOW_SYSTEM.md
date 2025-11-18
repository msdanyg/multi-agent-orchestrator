# Workflow Template System 🔄

## Overview

The Workflow Template System enables the multi-agent orchestrator to follow predefined, repeatable processes for common task types. Workflows define sequences of agent actions, validation steps, and best practices that ensure consistent, high-quality output across projects.

## Core Concepts

### Workflow Template
A structured definition of steps to accomplish a specific type of task. Each workflow includes:
- **Name & Description**: What the workflow does
- **Task Types**: Keywords that trigger this workflow
- **Steps**: Ordered sequence of agent actions
- **Validation Rules**: Quality checks between steps
- **Hooks**: Pre/post actions (e.g., git operations)

### Workflow Step
Individual action within a workflow:
- **Agent**: Which agent performs this step
- **Action**: What the agent should do
- **Required**: Whether step is mandatory or optional
- **Inputs**: Data needed from previous steps
- **Outputs**: Data produced for next steps
- **Validation**: Success criteria

### Workflow Context
Runtime state during workflow execution:
- Current step
- Completed steps
- Agent outputs
- Validation results
- User interventions

## Architecture

```
workflows/
├── templates/              # Workflow definitions
│   ├── web-app-development.yaml
│   ├── security-audit.yaml
│   ├── testing-suite.yaml
│   ├── documentation.yaml
│   ├── api-design.yaml
│   └── custom/            # User-defined workflows
├── learned/               # Auto-generated from usage patterns
└── history/              # Execution logs for learning
```

## Workflow Schema (YAML)

```yaml
name: web-app-development
version: 1.0.0
description: Complete workflow for building web applications from design to deployment
author: system
created: 2025-01-17
updated: 2025-01-17

# Task classification
task_types:
  - design web app
  - build web app
  - create website
  - develop ui
  - new web project

# Required agents for this workflow
agents_required:
  - designer
  - code_writer
  - qa_tester

# Workflow steps
steps:
  - id: design
    name: Create Design Specifications
    agent: designer
    action: |
      Create comprehensive UI/UX design specifications including:
      - User interface layout and components
      - Color scheme and typography
      - Responsive design breakpoints
      - Interaction patterns
      - Accessibility considerations
    required: true
    timeout: 300
    outputs:
      - DESIGN.md
    validation:
      - output_exists: DESIGN.md
      - min_lines: 100

  - id: implement
    name: Implement Application
    agent: code_writer
    action: |
      Implement the application based on design specifications:
      - Create HTML structure
      - Write CSS styling
      - Implement JavaScript functionality
      - Ensure responsive design
      - Follow best practices
    required: true
    depends_on: [design]
    inputs:
      - DESIGN.md
    outputs:
      - index.html
    timeout: 600
    validation:
      - output_exists: index.html
      - syntax_valid: true

  - id: code_review
    name: Code Quality Review
    agent: code_analyst
    action: |
      Review code for:
      - Code quality and best practices
      - Performance optimization opportunities
      - Potential bugs or issues
      - Maintainability
    required: false
    depends_on: [implement]
    inputs:
      - index.html
    outputs:
      - CODE_REVIEW.md

  - id: security_check
    name: Security Audit
    agent: security
    action: |
      Perform security review:
      - Check for XSS vulnerabilities
      - Validate input handling
      - Review authentication/authorization
      - Check dependency security
    required: false
    depends_on: [implement]
    inputs:
      - index.html
    outputs:
      - SECURITY_AUDIT.md

  - id: testing
    name: Quality Assurance Testing
    agent: qa_tester
    action: |
      Test the application:
      - Functional testing
      - UI/UX testing
      - Cross-browser compatibility
      - Responsive design testing
      - Accessibility testing
    required: true
    depends_on: [implement]
    inputs:
      - index.html
      - DESIGN.md
    outputs:
      - QA_REPORT.md
    validation:
      - all_tests_pass: true

  - id: documentation
    name: Create Documentation
    agent: docs_writer
    action: |
      Create comprehensive documentation:
      - README with usage instructions
      - Feature list
      - Installation guide
      - Troubleshooting section
    required: true
    depends_on: [implement, testing]
    outputs:
      - README.md
    validation:
      - output_exists: README.md
      - min_lines: 50

# Hooks (pre/post actions)
hooks:
  pre_workflow:
    - action: check_git_status
      description: Ensure clean git state
    - action: create_branch
      description: Create feature branch if needed

  post_workflow:
    - action: run_linter
      description: Run code linter
    - action: proof_read
      agent: docs_writer
      description: Proof-read all documentation
    - action: git_commit
      description: Commit all changes
      message: "Complete {workflow.name} workflow\n\nGenerated files:\n{outputs}"

  on_error:
    - action: rollback
      description: Revert changes on failure
    - action: notify_user
      description: Alert user of failure

# Quality gates
quality_gates:
  - name: design_approval
    after_step: design
    type: manual
    description: User reviews and approves design

  - name: all_tests_pass
    after_step: testing
    type: automatic
    condition: qa_tester.tests_passed == true

# Learning configuration
learning:
  enabled: true
  track_metrics:
    - step_duration
    - step_success_rate
    - user_modifications
  improve_on:
    - step_order_optimization
    - timeout_adjustment
    - validation_refinement

# Metadata
tags:
  - web-development
  - frontend
  - ui-ux
priority: high
usage_count: 0
success_rate: 0.0
```

## Workflow Manager CLI

### Commands

```bash
# List all workflows
python system/workflow-cli.py list

# Show workflow details
python system/workflow-cli.py show web-app-development

# Create new workflow
python system/workflow-cli.py create my-workflow --template base

# Edit workflow
python system/workflow-cli.py edit web-app-development

# Validate workflow
python system/workflow-cli.py validate web-app-development

# Execute workflow
python system/workflow-cli.py run web-app-development --project my-project

# Export workflow
python system/workflow-cli.py export web-app-development --format json

# Import workflow
python system/workflow-cli.py import custom-workflow.yaml

# Show workflow statistics
python system/workflow-cli.py stats

# Learn from history
python system/workflow-cli.py learn --analyze-history
```

## Orchestrator Integration

### Workflow Selection

When a task is received, the orchestrator:

1. **Analyzes Task**: Extracts keywords and intent
2. **Matches Workflows**: Finds workflows matching task_types
3. **Ranks Candidates**: Scores workflows by relevance
4. **Selects Best**: Chooses highest-scoring workflow
5. **Confirms with User**: (optional) Shows selected workflow
6. **Executes**: Runs workflow steps in order

### Workflow Execution

```python
class WorkflowExecutor:
    def execute_workflow(self, workflow, context):
        # Run pre-workflow hooks
        self.run_hooks(workflow.hooks.pre_workflow)

        # Execute steps in order
        for step in workflow.steps:
            if not self.should_execute_step(step, context):
                continue

            # Run the step
            result = self.execute_step(step, context)

            # Validate output
            if not self.validate_step(step, result):
                self.handle_validation_failure(step, result)

            # Update context
            context.add_result(step.id, result)

            # Check quality gates
            if self.has_quality_gate(step):
                if not self.check_quality_gate(step, context):
                    break

        # Run post-workflow hooks
        self.run_hooks(workflow.hooks.post_workflow, context)

        return context
```

## Default Workflows

### 1. Web App Development
- Design → Implement → Review → Test → Document

### 2. Security Audit
- Code Analysis → Vulnerability Scan → Penetration Test → Report

### 3. Testing Suite
- Unit Tests → Integration Tests → E2E Tests → Report

### 4. API Development
- Design API → Implement → Test → Document → Deploy

### 5. Documentation
- Analyze Code → Write Docs → Review → Proof-read

### 6. Code Review
- Static Analysis → Manual Review → Security Check → Recommendations

### 7. Deployment
- Pre-deploy Checks → Build → Test → Deploy → Verify

## Learning System

### Pattern Recognition

The system learns from workflow executions:

```python
class WorkflowLearner:
    def analyze_execution(self, execution_log):
        # Track which steps succeeded/failed
        # Measure step durations
        # Record user modifications
        # Note common patterns

    def suggest_improvements(self, workflow):
        # Optimize step order
        # Adjust timeouts
        # Add/remove optional steps
        # Update validation rules

    def create_new_workflow(self, task_history):
        # Identify repeated task patterns
        # Extract common agent sequences
        # Generate workflow template
        # Suggest to user for approval
```

### Auto-generated Workflows

When the system detects repeated patterns (e.g., user always runs security audit after code implementation), it:

1. Recognizes the pattern
2. Generates a workflow template
3. Suggests it to the user
4. Adds to custom workflows if approved

## User Interface

### Workflow Panel (in agent-ui)

```
┌─ WORKFLOWS ─────────────────┐
│ 📋 Available Workflows      │
│                             │
│ ⭐ Web App Development      │
│    5 steps • High priority  │
│                             │
│ 🔒 Security Audit           │
│    4 steps • Medium         │
│                             │
│ ✓ Testing Suite             │
│    3 steps • High           │
│                             │
│ 📝 Documentation            │
│    2 steps • Low            │
│                             │
│ [+ New Workflow]            │
└─────────────────────────────┘

┌─ WORKFLOW EXECUTION ────────┐
│ Web App Development         │
│                             │
│ ✅ Design                   │
│ ⏳ Implement (in progress)  │
│ ⏸️  Code Review (queued)    │
│ ⏸️  Testing (queued)        │
│ ⏸️  Documentation (queued)  │
│                             │
│ Progress: 20% (1/5 steps)   │
│ Estimated: 15 min remaining │
└─────────────────────────────┘
```

### Workflow Editor

Visual editor for creating/editing workflows:
- Drag-and-drop step ordering
- Agent selection dropdowns
- Validation rule builder
- Hook configuration
- Quality gate setup

## Benefits

### For Users
- **Consistency**: Same quality across all projects
- **Speed**: No need to manually specify agent sequences
- **Best Practices**: Built-in quality checks
- **Learning**: System improves over time
- **Customization**: Define custom workflows

### For Orchestrator
- **Structure**: Clear execution path
- **Validation**: Quality gates prevent errors
- **Recovery**: Error handling built-in
- **Metrics**: Track success rates
- **Optimization**: Learn from execution data

## Example Usage

### Scenario: User wants to build a weather app

**Without Workflows:**
```
User: "Build a weather app"
Orchestrator: [Guesses which agents to use, may miss steps]
```

**With Workflows:**
```
User: "Build a weather app"
Orchestrator:
  - Detects "build" + "app" → Matches "web-app-development" workflow
  - Shows: "I'll use the Web App Development workflow (5 steps)"
  - Executes:
    ✅ Designer creates DESIGN.md
    ✅ Code_writer implements index.html
    ✅ Code_analyst reviews code
    ✅ QA_tester tests functionality
    ✅ Docs_writer creates README.md
  - Runs hooks:
    ✅ Proof-reading before commit
    ✅ Git commit with generated message
Result: Complete, tested, documented app with proof-read docs
```

## Implementation Phases

### Phase 1: Core System (Current)
- [x] Workflow schema design
- [ ] Workflow storage structure
- [ ] Basic workflow manager CLI
- [ ] 4-5 default workflow templates
- [ ] Simple orchestrator integration

### Phase 2: Advanced Features
- [ ] Workflow learning system
- [ ] Auto-generation from patterns
- [ ] Quality gates implementation
- [ ] Advanced validation rules
- [ ] Workflow versioning

### Phase 3: UI Integration
- [ ] Workflow panel in agent-ui
- [ ] Visual workflow editor
- [ ] Execution monitoring
- [ ] Statistics dashboard
- [ ] Custom workflow creation UI

### Phase 4: Intelligence
- [ ] ML-based workflow optimization
- [ ] Anomaly detection
- [ ] Predictive step duration
- [ ] Smart agent selection
- [ ] Context-aware execution

## Future Enhancements

- **Conditional Branching**: Steps execute based on conditions
- **Parallel Execution**: Multiple agents work simultaneously
- **Sub-workflows**: Workflows can call other workflows
- **A/B Testing**: Compare workflow variants
- **Rollback**: Undo workflow execution
- **Scheduling**: Recurring workflow execution
- **Collaboration**: Multi-user workflow approval
- **Integration**: Connect to external tools (CI/CD, etc.)

---

**This workflow system transforms the orchestrator from a simple agent dispatcher into an intelligent process automation platform.**
