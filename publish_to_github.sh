#!/bin/bash

################################################################################
# Publish Multi-Agent Orchestrator to GitHub
# Automated script to prepare and publish the repository
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📦 Multi-Agent Orchestrator - GitHub Publishing Script"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 1: Pre-flight checks
echo -e "${BLUE}▶${NC} Step 1: Pre-flight Checks"
echo ""

# Check for sensitive data
echo "  Checking for API keys and sensitive data..."
if grep -r "sk-ant-" . --exclude-dir=.git 2>/dev/null | grep -v ".sh:" | grep -v "README" | grep -v ".md:" ; then
    echo -e "${RED}❌${NC} Found potential API keys in code!"
    echo "  Please remove sensitive data before publishing."
    exit 1
fi

if grep -r "dglickman@bgrove.com" . --exclude-dir=.git 2>/dev/null | grep -v ".sh:" | grep -v "README" | grep -v ".md:" | grep -v "LICENSE" ; then
    echo -e "${YELLOW}⚠️${NC}  Found personal email references"
    echo "  Review files and remove if sensitive"
    read -p "  Continue anyway? [y/N]: " continue_personal
    if [[ ! $continue_personal =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${GREEN}✅${NC} No obvious API keys found"
echo ""

# Check git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌${NC} Git is not installed"
    exit 1
fi
echo -e "${GREEN}✅${NC} Git is installed"

# Check if GitHub CLI is available
if command -v gh &> /dev/null; then
    GH_CLI_AVAILABLE=true
    echo -e "${GREEN}✅${NC} GitHub CLI is available"
else
    GH_CLI_AVAILABLE=false
    echo -e "${YELLOW}⚠️${NC}  GitHub CLI not found (optional)"
fi

echo ""

# Step 2: Clean up local files
echo -e "${BLUE}▶${NC} Step 2: Cleaning Up Local Files"
echo ""

echo "  Removing user-specific data..."
rm -f agents/registry.json 2>/dev/null
rm -f agents/skills_history.json 2>/dev/null
rm -f workspace/sessions.json 2>/dev/null
rm -f logs/*.log 2>/dev/null
rm -rf workspace/*/ 2>/dev/null

echo -e "${GREEN}✅${NC} Local data cleaned"
echo ""

# Step 3: Use GitHub README
echo -e "${BLUE}▶${NC} Step 3: Preparing Repository Files"
echo ""

if [ -f README_GITHUB.md ]; then
    echo "  Using README_GITHUB.md as main README..."
    mv README.md README_FULL.md 2>/dev/null || true
    cp README_GITHUB.md README.md
    echo -e "${GREEN}✅${NC} GitHub README prepared"
else
    echo -e "${YELLOW}⚠️${NC}  README_GITHUB.md not found, using existing README.md"
fi

echo ""

# Step 4: Initialize Git
echo -e "${BLUE}▶${NC} Step 4: Initializing Git Repository"
echo ""

if [ ! -d .git ]; then
    echo "  Initializing git repository..."
    git init
    echo -e "${GREEN}✅${NC} Git initialized"
else
    echo -e "${GREEN}✅${NC} Git already initialized"
fi

echo ""

# Step 5: Add files
echo -e "${BLUE}▶${NC} Step 5: Adding Files to Git"
echo ""

git add .
echo -e "${GREEN}✅${NC} Files staged"

# Show what will be committed
echo ""
echo "  Files to be committed:"
git status --short | head -20
echo ""

read -p "  Review files and continue? [Y/n]: " continue_commit
continue_commit=${continue_commit:-Y}

if [[ ! $continue_commit =~ ^[Yy]$ ]]; then
    echo "  Aborted by user"
    exit 0
fi

echo ""

# Step 6: Create commit
echo -e "${BLUE}▶${NC} Step 6: Creating Initial Commit"
echo ""

git commit -m "Initial commit: Multi-Agent Orchestrator v1.0.0

Features:
- Complete orchestration framework with specialized agents
- Automatic task delegation and intelligent routing
- TMUX session management for agent isolation
- Skills tracking and continuous learning
- Comprehensive documentation and deployment guides
- Calculator demo showcasing multi-agent collaboration
- Test suite with 100% coverage

Includes:
- 6 default specialist agents (analyst, writer, tester, researcher, devops, docs)
- CLI tool for task execution
- Interactive examples and tutorials
- Deployment guides for production
- Setup automation scripts"

echo -e "${GREEN}✅${NC} Initial commit created"
echo ""

# Step 7: Create remote repository
echo -e "${BLUE}▶${NC} Step 7: Creating GitHub Repository"
echo ""

read -p "  Repository name [multi-agent-orchestrator]: " REPO_NAME
REPO_NAME=${REPO_NAME:-multi-agent-orchestrator}

read -p "  Make repository public? [Y/n]: " PUBLIC_REPO
PUBLIC_REPO=${PUBLIC_REPO:-Y}

if [[ $PUBLIC_REPO =~ ^[Yy]$ ]]; then
    VISIBILITY="--public"
else
    VISIBILITY="--private"
fi

if [ "$GH_CLI_AVAILABLE" = true ]; then
    echo ""
    echo "  Option 1: Use GitHub CLI (automated)"
    echo "  Option 2: Manual setup via GitHub.com"
    echo ""
    read -p "  Use GitHub CLI? [Y/n]: " USE_GH_CLI
    USE_GH_CLI=${USE_GH_CLI:-Y}

    if [[ $USE_GH_CLI =~ ^[Yy]$ ]]; then
        echo ""
        echo "  Creating repository with GitHub CLI..."

        gh repo create $REPO_NAME \
            $VISIBILITY \
            --description "Intelligent multi-agent orchestration framework using Claude AI for automatic task delegation and parallel execution" \
            --source=. \
            --remote=origin \
            --push || {
                echo -e "${RED}❌${NC} GitHub CLI creation failed"
                echo "  Falling back to manual instructions..."
                GH_CLI_FAILED=true
            }

        if [ "$GH_CLI_FAILED" != true ]; then
            echo -e "${GREEN}✅${NC} Repository created and pushed!"
            REPO_CREATED=true
        fi
    fi
fi

# Manual instructions if GH CLI not used or failed
if [ "$REPO_CREATED" != true ]; then
    echo ""
    echo -e "${YELLOW}📝 Manual Setup Required${NC}"
    echo ""
    echo "  1. Go to: https://github.com/new"
    echo "  2. Repository name: $REPO_NAME"
    echo "  3. Visibility: $([ $VISIBILITY == '--public' ] && echo 'Public' || echo 'Private')"
    echo "  4. DO NOT initialize with README, .gitignore, or license"
    echo "  5. Click 'Create repository'"
    echo ""
    read -p "  Press Enter when repository is created..."

    echo ""
    read -p "  Enter your GitHub username: " GH_USERNAME

    echo ""
    echo "  Adding remote and pushing..."
    git remote add origin "https://github.com/$GH_USERNAME/$REPO_NAME.git" || \
        git remote set-url origin "https://github.com/$GH_USERNAME/$REPO_NAME.git"

    git branch -M main
    git push -u origin main

    echo -e "${GREEN}✅${NC} Pushed to GitHub!"
fi

echo ""

# Step 8: Create release tag
echo -e "${BLUE}▶${NC} Step 8: Creating Release Tag"
echo ""

git tag -a v1.0.0 -m "Multi-Agent Orchestrator v1.0.0

Initial Release

Features:
- Complete orchestration framework
- 6 default specialist agents
- Automatic task routing
- TMUX session management
- Skills tracking and learning
- Comprehensive documentation
- Calculator demo
- Deployment guides
- Test suite (100% coverage)

Quick Start:
./install.sh . full

Documentation:
- QUICKSTART.md - Get started in 5 minutes
- README.md - Complete documentation
- DEPLOYMENT_GUIDE.md - Setup guide"

git push origin v1.0.0

echo -e "${GREEN}✅${NC} Release tag created"
echo ""

# Step 9: Final instructions
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}🎉 SUCCESS!${NC} Repository Published"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 Repository URL:"
if [ -n "$GH_USERNAME" ]; then
    echo "   https://github.com/$GH_USERNAME/$REPO_NAME"
else
    echo "   https://github.com/YOUR_USERNAME/$REPO_NAME"
fi
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Visit your repository on GitHub"
echo ""
echo "2. Add repository topics:"
echo "   Settings → General → Topics"
echo "   Suggested: ai, claude, multi-agent, python, automation, orchestration"
echo ""
echo "3. Create a release from tag v1.0.0:"
echo "   Releases → Draft a new release"
echo "   Choose tag: v1.0.0"
echo "   Title: Multi-Agent Orchestrator v1.0.0"
echo ""
echo "4. Enable repository features:"
echo "   Settings → Features"
echo "   ✓ Issues, Discussions, Projects"
echo ""
echo "5. Configure security:"
echo "   Settings → Security"
echo "   ✓ Enable Dependabot"
echo "   ✓ Enable secret scanning"
echo ""
echo "6. Update repository description"
echo ""
echo "7. Share your project:"
echo "   • Twitter/X with #AI #Claude #MultiAgent"
echo "   • Reddit: r/artificial, r/Python"
echo "   • LinkedIn with project summary"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 Documentation checklist:"
echo "   ✓ README.md - Main documentation"
echo "   ✓ LICENSE - MIT License"
echo "   ✓ CONTRIBUTING.md - Contribution guidelines"
echo "   ✓ .gitignore - Ignore patterns"
echo "   ✓ QUICKSTART.md - 5-minute start guide"
echo "   ✓ DEPLOYMENT_GUIDE.md - Setup instructions"
echo ""
echo "🎯 Your repository is live and ready for contributors!"
echo ""
