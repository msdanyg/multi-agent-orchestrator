# Multi-Project Architecture Design
## Professional Project Management with Cross-Project Learning

**Date:** 2025-11-17
**Purpose:** Enable professional development of multiple isolated projects with shared, evolving agents

---

## Current vs. Proposed Architecture

### Current Issues
- ❌ Single project in root directory (no isolation)
- ❌ No per-project git repository management
- ❌ Skills history is global but not structured for reuse
- ❌ No project scaffolding or templates
- ❌ No clean separation between system and projects

### Proposed Solution
- ✅ Projects isolated in separate directories
- ✅ Each project has own git repository
- ✅ Agents shared across all projects
- ✅ Skills learned and transferred between projects
- ✅ Project templates for quick setup
- ✅ Professional folder structure per project

---

## Directory Structure

```
multi-agent-orchestrator/              (CORE SYSTEM - Never modify during projects)
├── agents/                            (Shared agent system)
│   ├── registry.json                  (Agent definitions)
│   ├── task_router.py                 (Task routing logic)
│   └── skills_database.json           (Global cross-project skills)
│
├── .claude/agents/                    (Agent instruction files)
│   ├── designer.md
│   ├── code_writer.md
│   ├── security.md
│   └── ... (all agents)
│
├── system/                            (NEW: System tools)
│   ├── project-cli.py                 (Project management CLI)
│   ├── agent-cli.py                   (Agent management - moved)
│   ├── orchestrator.py                (Enhanced orchestrator)
│   └── learning-engine.py             (Cross-project learning)
│
├── templates/                         (Project templates)
│   ├── web-app/                       (Web application template)
│   ├── api-service/                   (REST API template)
│   ├── library/                       (Library/package template)
│   ├── documentation/                 (Docs site template)
│   └── custom/                        (Custom templates)
│
├── projects/                          (NEW: All user projects)
│   │
│   ├── my-saas-app/                   (Example project 1)
│   │   ├── .git/                      (Own git repository)
│   │   ├── .github/                   (GitHub workflows)
│   │   ├── .project/                  (Project metadata)
│   │   │   ├── config.json            (Project configuration)
│   │   │   ├── agent-memory/          (Project-specific learnings)
│   │   │   │   ├── designer.json      (Designer's project context)
│   │   │   │   ├── code_writer.json   (Code patterns used)
│   │   │   │   └── security.json      (Security patterns)
│   │   │   └── skills-gained.json     (Skills learned in this project)
│   │   ├── README.md
│   │   ├── docs/                      (Project documentation)
│   │   ├── src/                       (Source code)
│   │   ├── tests/                     (Tests)
│   │   └── .gitignore
│   │
│   ├── marketing-website/             (Example project 2)
│   │   ├── .git/
│   │   ├── .project/
│   │   ├── ... (same structure)
│   │
│   └── internal-tool/                 (Example project 3)
│       └── ... (same structure)
│
├── shared-knowledge/                  (NEW: Cross-project knowledge base)
│   ├── brand-guidelines/              (Reusable brand assets)
│   ├── code-patterns/                 (Proven code patterns)
│   ├── design-systems/                (Reusable design systems)
│   └── security-rules/                (Security best practices)
│
├── main.py                            (Original orchestrator - backward compat)
├── manage_agents.py                   (Agent management)
└── README.md                          (System documentation)
```

---

## Key Components

### 1. Project CLI (`system/project-cli.py`)

**Commands:**
```bash
# Create new project
python project-cli.py create <project-name> --template web-app

# List all projects
python project-cli.py list

# Switch to project (sets working context)
python project-cli.py use <project-name>

# Get project info
python project-cli.py info <project-name>

# Initialize git and GitHub
python project-cli.py init-git <project-name> --remote <github-url>

# Archive project
python project-cli.py archive <project-name>

# Clone existing project
python project-cli.py clone <github-url> <project-name>

# Export project structure
python project-cli.py export <project-name>
```

---

### 2. Project Configuration (`.project/config.json`)

```json
{
  "name": "my-saas-app",
  "type": "web-app",
  "created": "2025-11-17T10:00:00Z",
  "description": "SaaS application for task management",
  "version": "1.0.0",

  "git": {
    "remote": "https://github.com/user/my-saas-app.git",
    "branch": "main",
    "initialized": true
  },

  "tech_stack": {
    "frontend": ["React", "TypeScript", "Tailwind"],
    "backend": ["Node.js", "Express", "PostgreSQL"],
    "deployment": "Vercel"
  },

  "agents": {
    "preferences": {
      "designer": {
        "brand_colors": ["#6366f1", "#ec4899"],
        "design_system": "shared-knowledge/design-systems/saas-design-system"
      },
      "code_writer": {
        "style": "airbnb",
        "test_framework": "jest"
      }
    },
    "memory_enabled": true
  },

  "shared_knowledge": [
    "brand-guidelines/company-brand",
    "design-systems/saas-design-system"
  ],

  "phases_completed": [
    "design",
    "implementation",
    "security-audit"
  ],

  "status": "in-progress"
}
```

---

### 3. Agent Memory System

#### Global Skills Database (`agents/skills_database.json`)

```json
{
  "version": "1.0",
  "last_updated": "2025-11-17T12:00:00Z",

  "skills": {
    "designer": {
      "design_systems": [
        {
          "id": "saas-modern-ui",
          "name": "Modern SaaS UI Pattern",
          "learned_from": "my-saas-app",
          "description": "Clean, modern design with indigo primary color",
          "colors": ["#6366f1", "#ec4899", "#10b981"],
          "typography": "Inter, system-fonts",
          "components": ["cards", "forms", "navigation"],
          "usage_count": 3,
          "success_rate": 0.95
        },
        {
          "id": "brand-ui-guidelines",
          "name": "Company Brand Guidelines",
          "learned_from": "marketing-website",
          "colors": ["#FF6B6B", "#4ECDC4"],
          "logo_usage": "...",
          "usage_count": 5,
          "success_rate": 1.0
        }
      ],

      "responsive_patterns": [
        {
          "id": "mobile-first-grid",
          "breakpoints": [768, 1024, 1280],
          "learned_from": "todo-app",
          "usage_count": 10
        }
      ]
    },

    "code_writer": {
      "code_patterns": [
        {
          "id": "react-custom-hooks",
          "pattern": "useLocalStorage",
          "language": "JavaScript",
          "learned_from": "todo-app",
          "code_sample": "...",
          "usage_count": 8
        },
        {
          "id": "error-boundary",
          "pattern": "React Error Boundary",
          "learned_from": "my-saas-app",
          "usage_count": 5
        }
      ],

      "api_patterns": [
        {
          "id": "rest-api-structure",
          "pattern": "Express REST API",
          "learned_from": "api-service",
          "usage_count": 3
        }
      ]
    },

    "security": {
      "security_rules": [
        {
          "id": "xss-prevention",
          "rule": "Use textContent instead of innerHTML",
          "severity": "high",
          "learned_from": "todo-app",
          "usage_count": 12
        },
        {
          "id": "csp-headers",
          "rule": "Implement Content-Security-Policy",
          "severity": "medium",
          "learned_from": "my-saas-app",
          "usage_count": 5
        }
      ]
    }
  },

  "patterns": {
    "successful_workflows": [
      {
        "id": "design-to-implementation",
        "phases": ["design", "implementation", "security", "qa", "docs"],
        "success_rate": 0.95,
        "projects_used": ["todo-app", "my-saas-app"]
      }
    ]
  }
}
```

#### Project-Specific Memory (`.project/agent-memory/designer.json`)

```json
{
  "project": "my-saas-app",
  "agent": "designer",
  "context": {
    "brand_colors": ["#6366f1", "#ec4899"],
    "typography": "Inter",
    "design_system_used": "saas-modern-ui",
    "components_created": [
      "dashboard",
      "user-profile",
      "settings-page"
    ],
    "decisions": [
      {
        "decision": "Use card-based layout",
        "reason": "Better for dashboard widgets",
        "date": "2025-11-17"
      }
    ]
  },

  "skills_applied": [
    "saas-modern-ui",
    "responsive-design",
    "accessibility-wcag"
  ],

  "new_skills_gained": [
    {
      "skill": "dashboard-widget-layout",
      "description": "3-column responsive dashboard grid",
      "can_be_shared": true
    }
  ]
}
```

---

### 4. Project Templates

#### Web App Template (`templates/web-app/`)

```
web-app/
├── .project/
│   └── config.json                    (Pre-configured for web apps)
├── src/
│   ├── components/
│   ├── pages/
│   ├── styles/
│   └── utils/
├── public/
├── tests/
├── docs/
│   ├── README.md
│   ├── ARCHITECTURE.md
│   └── API.md
├── .gitignore
├── package.json
├── tsconfig.json
└── README.md
```

#### API Service Template (`templates/api-service/`)

```
api-service/
├── .project/
├── src/
│   ├── routes/
│   ├── controllers/
│   ├── models/
│   ├── middleware/
│   └── utils/
├── tests/
├── docs/
│   ├── API_DOCS.md
│   └── SETUP.md
├── .env.example
├── .gitignore
└── README.md
```

---

### 5. Enhanced Orchestrator (`system/orchestrator.py`)

**New Capabilities:**

1. **Project Context Awareness:**
   ```python
   def run_with_context(task, project_name):
       # Load project configuration
       project = load_project(project_name)

       # Load agent memories for this project
       agent_memories = load_agent_memories(project)

       # Load relevant shared knowledge
       shared_knowledge = load_shared_knowledge(project.shared_knowledge)

       # Execute task with full context
       agent = select_agent(task)
       agent.set_context(project, agent_memories, shared_knowledge)
       result = agent.execute(task)

       # Save new learnings
       save_agent_memory(agent, project)
       update_skills_database(agent.new_skills)

       return result
   ```

2. **Skill Transfer:**
   ```python
   def suggest_relevant_skills(project, agent):
       # Find similar projects
       similar = find_similar_projects(project)

       # Get skills from similar projects
       relevant_skills = []
       for similar_project in similar:
           skills = get_project_skills(similar_project, agent)
           relevant_skills.extend(skills)

       return relevant_skills
   ```

3. **Cross-Project Learning:**
   ```python
   def learn_from_outcome(project, phase, outcome, success):
       skill = {
           "project": project.name,
           "phase": phase,
           "outcome": outcome,
           "success": success,
           "timestamp": now()
       }

       if success and is_reusable(skill):
           add_to_skills_database(skill)
           suggest_to_other_projects(skill)
   ```

---

## Workflow Examples

### Example 1: Starting a New Project

```bash
# User creates a new project
$ python system/project-cli.py create my-new-saas --template web-app

Creating project: my-new-saas
├── Copying web-app template...
├── Initializing project config...
├── Creating .project/ directory...
├── Initializing git repository...
└── ✓ Project created at: projects/my-new-saas/

# Initialize GitHub repository
$ python system/project-cli.py init-git my-new-saas --remote https://github.com/user/my-new-saas.git

├── Adding remote origin...
├── Creating initial commit...
├── Pushing to GitHub...
└── ✓ GitHub repository initialized

# Start working on the project
$ cd projects/my-new-saas

# Run orchestrator in project context
$ python ../../main.py task "Design a dashboard page"

Loading project context: my-new-saas
Loading agent memories...
Loading relevant skills:
  - Found: "saas-modern-ui" (used in 3 projects, 95% success rate)
  - Found: "dashboard-widget-layout" (from my-saas-app)

Designer agent starting...
Applying learned design system: saas-modern-ui
Using colors: #6366f1, #ec4899 (from previous projects)
Creating dashboard with 3-column responsive grid...

✓ Design complete: DASHBOARD_DESIGN.md
✓ New skill saved: "analytics-dashboard-pattern"
```

---

### Example 2: Reusing Brand Guidelines

```bash
# First project: Create brand guidelines
$ cd projects/marketing-website
$ python ../../main.py task "Create brand guidelines"

Designer agent:
├── Creating brand color palette...
├── Defining typography...
├── Creating logo usage rules...
└── Saving to: .project/agent-memory/designer.json

✓ Skill saved to global database: "company-brand-guidelines"

# Second project: Reuse brand guidelines
$ cd projects/internal-tool
$ python ../../main.py task "Design user interface using company brand"

Designer agent:
Loading relevant skills...
  - Found: "company-brand-guidelines" (from marketing-website)

Applying brand guidelines:
  Colors: #FF6B6B, #4ECDC4
  Typography: Montserrat, Open Sans
  Logo: [rules loaded]

✓ Design created with consistent branding
```

---

### Example 3: Cross-Project Security Learning

```bash
# First project: Security audit finds XSS vulnerability
$ cd projects/todo-app
$ python ../../main.py task "Security audit"

Security agent:
Found: XSS vulnerability (use textContent instead of innerHTML)
Severity: High
✓ Saved security rule to global database

# Second project: Security agent proactively checks
$ cd projects/my-saas-app
$ python ../../main.py task "Implement comments feature"

Code_writer agent:
Implementing comments display...

Security agent (auto-triggered):
Checking against known security rules...
  ⚠️ Warning: Using innerHTML detected
  Suggestion: Use textContent (learned from todo-app)

Code_writer agent:
✓ Applied security fix automatically
✓ Used textContent instead of innerHTML
```

---

## Implementation Plan

### Phase 1: Core Infrastructure (Week 1)
- [ ] Create `projects/` directory structure
- [ ] Implement `project-cli.py` (create, list, use commands)
- [ ] Create project templates (web-app, api-service)
- [ ] Implement `.project/config.json` system

### Phase 2: Git Integration (Week 1-2)
- [ ] Implement git initialization per project
- [ ] Add GitHub remote management
- [ ] Create `.gitignore` templates
- [ ] Add git workflow commands

### Phase 3: Agent Memory System (Week 2)
- [ ] Create `skills_database.json` schema
- [ ] Implement agent memory storage (`.project/agent-memory/`)
- [ ] Create skill saving/loading system
- [ ] Implement skill recommendation engine

### Phase 4: Enhanced Orchestrator (Week 3)
- [ ] Add project context awareness
- [ ] Implement skill transfer between projects
- [ ] Add cross-project learning
- [ ] Create learning engine

### Phase 5: Shared Knowledge Base (Week 3-4)
- [ ] Create `shared-knowledge/` directory
- [ ] Implement brand guidelines storage
- [ ] Add design system templates
- [ ] Create code pattern library

### Phase 6: Advanced Features (Week 4)
- [ ] Project similarity detection
- [ ] Automatic skill suggestions
- [ ] Project analytics dashboard
- [ ] Migration tool for existing projects

---

## Benefits

### For Users:
✅ **Professional Project Management** - Clean, isolated projects
✅ **Best Practices** - Templates enforce good structure
✅ **Git Integration** - Automatic version control setup
✅ **Consistency** - Reuse proven patterns across projects
✅ **Time Savings** - Don't recreate solutions

### For Agents:
✅ **Context Awareness** - Understand project-specific needs
✅ **Continuous Learning** - Skills improve over time
✅ **Knowledge Transfer** - Apply learnings from past projects
✅ **Better Results** - Informed by historical success

---

## Technical Considerations

### Performance
- Skills database uses indexing for fast lookups
- Project memory kept small (JSON, < 1MB per project)
- Lazy loading of shared knowledge

### Scalability
- Support for 100+ projects
- Skills database with 1000+ skills
- Efficient skill matching algorithms

### Backward Compatibility
- Original `main.py` still works (no project context)
- Existing files can be migrated to project structure
- Gradual adoption path

---

## Next Steps

1. **Review and approve architecture**
2. **Implement Phase 1 (Core Infrastructure)**
3. **Test with 2-3 sample projects**
4. **Iterate based on real usage**
5. **Add advanced features**

---

**Questions for Discussion:**

1. Should projects have sub-projects (nested structure)?
2. How to handle shared dependencies across projects?
3. Should there be project groups/workspaces?
4. How detailed should agent memory be?
5. What's the right balance between automatic and manual skill transfer?
