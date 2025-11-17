#!/bin/bash

# Multi-Agent Framework Setup Script

set -e

echo "=================================================="
echo "Multi-Agent Management Framework Setup"
echo "=================================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3,10) else 1)"; then
    echo "❌ Error: Python 3.10+ required. Found: $python_version"
    exit 1
fi
echo "✅ Python $python_version detected"
echo ""

# Check TMUX
echo "Checking TMUX installation..."
if ! command -v tmux &> /dev/null; then
    echo "❌ TMUX not found. Please install TMUX first:"
    echo ""
    echo "  macOS:        brew install tmux"
    echo "  Ubuntu/Debian: sudo apt-get install tmux"
    echo "  Fedora:       sudo dnf install tmux"
    echo ""
    exit 1
fi
tmux_version=$(tmux -V)
echo "✅ $tmux_version detected"
echo ""

# Create virtual environment (optional but recommended)
read -p "Create Python virtual environment? (recommended) [Y/n]: " create_venv
create_venv=${create_venv:-Y}

if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
    echo "To activate: source venv/bin/activate"
    source venv/bin/activate
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Setup environment file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your ANTHROPIC_API_KEY"
else
    echo "✅ .env file already exists"
fi
echo ""

# Make scripts executable
echo "Making scripts executable..."
chmod +x main.py
chmod +x examples.py
chmod +x setup.sh
echo "✅ Scripts are executable"
echo ""

# Create necessary directories
echo "Creating directory structure..."
mkdir -p workspace/shared
mkdir -p logs
mkdir -p config
mkdir -p specialists
echo "✅ Directories created"
echo ""

# Initialize agent registry
echo "Initializing agent registry..."
python3 -c "
from agents import AgentRegistry
registry = AgentRegistry('agents/registry.json')
print('✅ Agent registry initialized with', len(registry.agents), 'default agents')
"
echo ""

# Test TMUX functionality
echo "Testing TMUX functionality..."
if tmux new-session -d -s test-session 2>/dev/null; then
    tmux kill-session -t test-session
    echo "✅ TMUX working correctly"
else
    echo "⚠️  TMUX test failed, but installation will continue"
fi
echo ""

# Display setup summary
echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Configure your API key:"
echo "   Edit .env and add your ANTHROPIC_API_KEY"
echo ""
echo "2. Verify installation:"
echo "   python main.py status"
echo ""
echo "3. List available agents:"
echo "   python main.py agents"
echo ""
echo "4. Try an example task:"
echo "   python main.py task \"Analyze the codebase structure\""
echo ""
echo "5. Run examples:"
echo "   python examples.py"
echo ""
echo "For more information, see README.md"
echo "=================================================="
