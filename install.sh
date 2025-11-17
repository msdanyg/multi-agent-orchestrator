#!/bin/bash

################################################################################
# Multi-Agent Orchestrator - Installation Script
# Quick deployment to any project or device
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-$(pwd)}"
INSTALL_TYPE="${2:-full}"  # full, minimal, or custom

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "$1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

print_step() {
    echo -e "${BLUE}▶${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC}  $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_error "$1 is not installed"
        return 1
    fi
}

################################################################################
# Pre-flight Checks
################################################################################

preflight_checks() {
    print_header "Multi-Agent Orchestrator Installation"
    echo "Target directory: $TARGET_DIR"
    echo "Installation type: $INSTALL_TYPE"
    echo ""

    print_step "Running pre-flight checks..."
    echo ""

    local all_good=true

    # Check Python
    if python3 --version &> /dev/null; then
        python_version=$(python3 --version | awk '{print $2}')
        if python3 -c "import sys; exit(0 if sys.version_info >= (3,10) else 1)"; then
            print_success "Python $python_version (✓ 3.10+)"
        else
            print_error "Python $python_version (requires 3.10+)"
            all_good=false
        fi
    else
        print_error "Python 3 not found"
        all_good=false
    fi

    # Check TMUX
    if command -v tmux &> /dev/null; then
        tmux_version=$(tmux -V | awk '{print $2}')
        print_success "TMUX $tmux_version"
    else
        print_error "TMUX not found"
        echo "  Install: brew install tmux (macOS) or apt-get install tmux (Linux)"
        all_good=false
    fi

    # Check pip
    if python3 -m pip --version &> /dev/null; then
        print_success "pip is available"
    else
        print_warning "pip not found, will try to install"
    fi

    echo ""

    if [ "$all_good" = false ]; then
        print_error "Pre-flight checks failed. Please install missing dependencies."
        exit 1
    fi

    print_success "Pre-flight checks passed!"
}

################################################################################
# Installation Functions
################################################################################

create_directory_structure() {
    print_step "Creating directory structure..."

    mkdir -p "$TARGET_DIR"/{agents,specialists,workspace/shared,logs,config,scripts}

    print_success "Directory structure created"
}

copy_framework_files() {
    print_step "Copying framework files..."

    # Core files
    cp "$SCRIPT_DIR"/agents/*.py "$TARGET_DIR/agents/" 2>/dev/null || true
    cp "$SCRIPT_DIR"/*.py "$TARGET_DIR/" 2>/dev/null || true
    cp "$SCRIPT_DIR"/*.sh "$TARGET_DIR/" 2>/dev/null || true
    cp "$SCRIPT_DIR"/requirements.txt "$TARGET_DIR/" 2>/dev/null || true

    # Documentation
    cp "$SCRIPT_DIR"/*.md "$TARGET_DIR/" 2>/dev/null || true

    # Configuration templates
    if [ -f "$SCRIPT_DIR/.env.example" ]; then
        cp "$SCRIPT_DIR/.env.example" "$TARGET_DIR/"
    fi

    # Make scripts executable
    chmod +x "$TARGET_DIR"/*.sh 2>/dev/null || true
    chmod +x "$TARGET_DIR"/*.py 2>/dev/null || true

    print_success "Framework files copied"
}

install_dependencies() {
    print_step "Installing Python dependencies..."

    cd "$TARGET_DIR"

    # Ask about virtual environment
    if [ -t 0 ]; then  # Check if running interactively
        read -p "Create Python virtual environment? [Y/n]: " create_venv
        create_venv=${create_venv:-Y}
    else
        create_venv="Y"
    fi

    if [[ $create_venv =~ ^[Yy]$ ]]; then
        print_step "Creating virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        print_success "Virtual environment created and activated"
    fi

    # Upgrade pip
    python3 -m pip install --upgrade pip --quiet

    # Install dependencies
    if [ -f requirements.txt ]; then
        python3 -m pip install -r requirements.txt --quiet
        print_success "Dependencies installed"
    else
        # Install minimal dependencies
        python3 -m pip install python-dotenv rich --quiet
        print_success "Minimal dependencies installed"
    fi
}

configure_environment() {
    print_step "Configuring environment..."

    cd "$TARGET_DIR"

    # Create .env if it doesn't exist
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
        else
            cat > .env << 'EOF'
# Claude API Configuration
ANTHROPIC_API_KEY=your_api_key_here

# Model Configuration
ORCHESTRATOR_MODEL=claude-opus-4
WORKER_MODEL=claude-sonnet-4-5
SIMPLE_MODEL=claude-haiku-4

# System Configuration
PROJECT_ROOT=$(pwd)
MAX_PARALLEL_AGENTS=5
AGENT_TIMEOUT=600

# Logging
LOG_LEVEL=INFO
EOF
        fi
        print_success ".env file created"
        print_warning "Please edit .env and add your ANTHROPIC_API_KEY"
    else
        print_warning ".env file already exists (not overwritten)"
    fi
}

initialize_agents() {
    print_step "Initializing agent registry..."

    cd "$TARGET_DIR"

    if [ -f agents/registry.py ]; then
        python3 << 'EOF'
import sys
sys.path.insert(0, '.')
from agents import AgentRegistry
registry = AgentRegistry('agents/registry.json')
print(f"✅ Initialized {len(registry.agents)} default agents")
EOF
        print_success "Agent registry initialized"
    else
        print_warning "Agent registry not found, skipping initialization"
    fi
}

create_helper_scripts() {
    print_step "Creating helper scripts..."

    cd "$TARGET_DIR"

    # Quick start script
    cat > quick_start.sh << 'EOF'
#!/bin/bash
# Quick start helper script

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Show menu
echo "═══════════════════════════════════════════"
echo "   Multi-Agent Orchestrator - Quick Start"
echo "═══════════════════════════════════════════"
echo ""
echo "1. Check system status"
echo "2. List all agents"
echo "3. Run example task"
echo "4. Run tests"
echo "5. Generate report"
echo "6. Interactive examples"
echo ""
read -p "Select option (1-6): " choice

case $choice in
    1) python3 main.py status ;;
    2) python3 main.py agents ;;
    3) python3 main.py task "Analyze the project structure" ;;
    4) python3 test_framework.py ;;
    5) python3 main.py report ;;
    6) python3 examples.py ;;
    *) echo "Invalid choice" ;;
esac
EOF
    chmod +x quick_start.sh

    # Cleanup script
    cat > scripts/cleanup.sh << 'EOF'
#!/bin/bash
# Cleanup old TMUX sessions and temporary files

echo "Cleaning up..."

# Kill old TMUX sessions
python3 << 'PYTHON'
from agents import TmuxManager
tm = TmuxManager()
cleaned = tm.cleanup_old_sessions(max_age_hours=24)
print(f"Cleaned {cleaned} old TMUX sessions")
PYTHON

# Clean old logs (keep last 7 days)
find logs/ -name "*.log" -mtime +7 -delete 2>/dev/null || true

# Clean old workspaces
find workspace/ -type d -empty -delete 2>/dev/null || true

echo "✅ Cleanup complete"
EOF
    chmod +x scripts/cleanup.sh

    print_success "Helper scripts created"
}

run_tests() {
    print_step "Running installation tests..."

    cd "$TARGET_DIR"

    if [ -f test_framework.py ]; then
        if python3 test_framework.py; then
            print_success "All tests passed!"
        else
            print_warning "Some tests failed (may be normal for minimal install)"
        fi
    else
        print_warning "Test suite not found, skipping tests"
    fi
}

################################################################################
# Installation Types
################################################################################

install_full() {
    print_header "Full Installation"

    create_directory_structure
    copy_framework_files
    install_dependencies
    configure_environment
    initialize_agents
    create_helper_scripts
    run_tests

    print_header "Installation Complete!"
    show_next_steps
}

install_minimal() {
    print_header "Minimal Installation"

    create_directory_structure

    # Copy only essential files
    print_step "Copying essential files..."
    mkdir -p "$TARGET_DIR/agents"
    cp "$SCRIPT_DIR"/agents/*.py "$TARGET_DIR/agents/" 2>/dev/null || true
    cp "$SCRIPT_DIR"/main.py "$TARGET_DIR/" 2>/dev/null || true
    cp "$SCRIPT_DIR"/requirements.txt "$TARGET_DIR/" 2>/dev/null || true
    cp "$SCRIPT_DIR"/.env.example "$TARGET_DIR/" 2>/dev/null || true

    install_dependencies
    configure_environment
    initialize_agents

    print_header "Minimal Installation Complete!"
    show_next_steps
}

install_custom() {
    print_header "Custom Installation"

    echo "Select components to install:"
    echo ""

    # Interactive selection
    read -p "Install core framework? [Y/n]: " install_core
    read -p "Install examples? [Y/n]: " install_examples
    read -p "Install tests? [Y/n]: " install_tests
    read -p "Install documentation? [Y/n]: " install_docs
    read -p "Create virtual environment? [Y/n]: " install_venv

    echo ""
    print_step "Installing selected components..."

    create_directory_structure

    # Core framework
    if [[ ${install_core:-Y} =~ ^[Yy]$ ]]; then
        mkdir -p "$TARGET_DIR/agents"
        cp "$SCRIPT_DIR"/agents/*.py "$TARGET_DIR/agents/" 2>/dev/null || true
        cp "$SCRIPT_DIR"/main.py "$TARGET_DIR/" 2>/dev/null || true
        print_success "Core framework installed"
    fi

    # Examples
    if [[ ${install_examples:-Y} =~ ^[Yy]$ ]]; then
        cp "$SCRIPT_DIR"/examples.py "$TARGET_DIR/" 2>/dev/null || true
        print_success "Examples installed"
    fi

    # Tests
    if [[ ${install_tests:-Y} =~ ^[Yy]$ ]]; then
        cp "$SCRIPT_DIR"/test_*.py "$TARGET_DIR/" 2>/dev/null || true
        print_success "Tests installed"
    fi

    # Documentation
    if [[ ${install_docs:-Y} =~ ^[Yy]$ ]]; then
        cp "$SCRIPT_DIR"/*.md "$TARGET_DIR/" 2>/dev/null || true
        print_success "Documentation installed"
    fi

    install_dependencies
    configure_environment
    initialize_agents

    print_header "Custom Installation Complete!"
    show_next_steps
}

################################################################################
# Post-installation
################################################################################

show_next_steps() {
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║               Installation Successful! 🎉                    ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "📁 Installation directory: $TARGET_DIR"
    echo ""
    echo "Next steps:"
    echo ""
    echo "1️⃣  Configure your API key:"
    echo "   cd $TARGET_DIR"
    echo "   nano .env"
    echo "   # Add: ANTHROPIC_API_KEY=your_key_here"
    echo ""
    echo "2️⃣  Verify installation:"
    echo "   python3 main.py status"
    echo ""
    echo "3️⃣  List available agents:"
    echo "   python3 main.py agents"
    echo ""
    echo "4️⃣  Try a test task:"
    echo "   python3 main.py task \"Analyze project structure\""
    echo ""
    echo "5️⃣  Run examples:"
    echo "   python3 examples.py"
    echo ""
    echo "📚 Documentation:"
    echo "   README.md          - Main documentation"
    echo "   QUICKSTART.md      - Quick start guide"
    echo "   DEPLOYMENT_GUIDE.md - Detailed setup instructions"
    echo ""
    echo "🆘 Need help? Check the troubleshooting section in DEPLOYMENT_GUIDE.md"
    echo ""
}

show_usage() {
    echo "Usage: $0 [target_directory] [installation_type]"
    echo ""
    echo "Arguments:"
    echo "  target_directory    Target installation directory (default: current directory)"
    echo "  installation_type   Type of installation: full, minimal, custom (default: full)"
    echo ""
    echo "Examples:"
    echo "  $0                              # Full install in current directory"
    echo "  $0 /path/to/project            # Full install in specified directory"
    echo "  $0 /path/to/project minimal    # Minimal install"
    echo "  $0 /path/to/project custom     # Custom install (interactive)"
    echo ""
    exit 1
}

################################################################################
# Main Installation Flow
################################################################################

main() {
    # Parse arguments
    if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        show_usage
    fi

    # Run pre-flight checks
    preflight_checks

    # Perform installation based on type
    case $INSTALL_TYPE in
        full)
            install_full
            ;;
        minimal)
            install_minimal
            ;;
        custom)
            install_custom
            ;;
        *)
            print_error "Unknown installation type: $INSTALL_TYPE"
            show_usage
            ;;
    esac
}

# Run main installation
main "$@"
