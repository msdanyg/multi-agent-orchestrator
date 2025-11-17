#!/usr/bin/env python3
"""
Agent Management CLI Tool
Easy viewing and editing of agent configurations
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import subprocess

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

REGISTRY_PATH = "agents/registry.json"
CLAUDE_AGENTS_DIR = ".claude/agents"

def print_header(text: str):
    """Print a colored header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.ENDC}\n")

def print_section(text: str):
    """Print a section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{text}{Colors.ENDC}")
    print(f"{Colors.BLUE}{'-' * len(text)}{Colors.ENDC}")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

def load_registry() -> Dict:
    """Load the agent registry"""
    try:
        with open(REGISTRY_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print_error(f"Registry file not found: {REGISTRY_PATH}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print_error(f"Invalid JSON in registry: {e}")
        sys.exit(1)

def save_registry(registry: Dict):
    """Save the agent registry"""
    try:
        with open(REGISTRY_PATH, 'w') as f:
            json.dump(registry, f, indent=2)
        print_success("Registry saved successfully")
    except Exception as e:
        print_error(f"Failed to save registry: {e}")
        sys.exit(1)

def list_agents(detailed: bool = False):
    """List all agents"""
    registry = load_registry()
    print_header("REGISTERED AGENTS")

    for i, (name, agent) in enumerate(registry.items(), 1):
        print(f"\n{Colors.BOLD}{i}. {name.upper()}{Colors.ENDC}")
        print(f"   {Colors.CYAN}Description:{Colors.ENDC} {agent['description']}")
        print(f"   {Colors.CYAN}Role:{Colors.ENDC} {agent['role']}")
        print(f"   {Colors.CYAN}Model:{Colors.ENDC} {agent['model']}")
        print(f"   {Colors.CYAN}Skill Level:{Colors.ENDC} {agent['skill_level']}")

        if detailed:
            print(f"   {Colors.CYAN}Tools:{Colors.ENDC} {', '.join(agent['tools'])}")
            print(f"   {Colors.CYAN}Capabilities:{Colors.ENDC} {', '.join(agent['capabilities'][:5])}", end="")
            if len(agent['capabilities']) > 5:
                print(f" (+{len(agent['capabilities']) - 5} more)")
            else:
                print()

            metrics = agent['metrics']
            print(f"   {Colors.CYAN}Performance:{Colors.ENDC}")
            print(f"      Tasks: {metrics['total_tasks']} | Success: {metrics['successful_tasks']} | Failed: {metrics['failed_tasks']}")
            if metrics['total_tasks'] > 0:
                success_rate = (metrics['successful_tasks'] / metrics['total_tasks']) * 100
                print(f"      Success Rate: {success_rate:.1f}%")
                print(f"      Avg Time: {metrics['avg_completion_time']:.2f}s")

def view_agent(agent_name: str):
    """View detailed information about a specific agent"""
    registry = load_registry()

    if agent_name not in registry:
        print_error(f"Agent '{agent_name}' not found")
        print("\nAvailable agents:")
        for name in registry.keys():
            print(f"  - {name}")
        return

    agent = registry[agent_name]
    print_header(f"AGENT: {agent_name.upper()}")

    print_section("Basic Information")
    print(f"{Colors.CYAN}Name:{Colors.ENDC} {agent['name']}")
    print(f"{Colors.CYAN}Description:{Colors.ENDC} {agent['description']}")
    print(f"{Colors.CYAN}Role:{Colors.ENDC} {agent['role']}")
    print(f"{Colors.CYAN}Model:{Colors.ENDC} {agent['model']}")
    print(f"{Colors.CYAN}Skill Level:{Colors.ENDC} {agent['skill_level']}")

    print_section("Tools")
    for tool in agent['tools']:
        print(f"  • {tool}")

    print_section("Capabilities")
    for i, cap in enumerate(agent['capabilities'], 1):
        print(f"  {i}. {cap}")

    print_section("System Prompt")
    prompt = agent['system_prompt']
    if len(prompt) > 500:
        print(prompt[:500] + "...")
        print(f"\n{Colors.YELLOW}[Truncated - full prompt is {len(prompt)} characters]{Colors.ENDC}")
    else:
        print(prompt)

    print_section("Performance Metrics")
    metrics = agent['metrics']
    print(f"{Colors.CYAN}Total Tasks:{Colors.ENDC} {metrics['total_tasks']}")
    print(f"{Colors.CYAN}Successful:{Colors.ENDC} {metrics['successful_tasks']}")
    print(f"{Colors.CYAN}Failed:{Colors.ENDC} {metrics['failed_tasks']}")
    if metrics['total_tasks'] > 0:
        success_rate = (metrics['successful_tasks'] / metrics['total_tasks']) * 100
        print(f"{Colors.CYAN}Success Rate:{Colors.ENDC} {success_rate:.1f}%")
        print(f"{Colors.CYAN}Avg Time:{Colors.ENDC} {metrics['avg_completion_time']:.2f}s")
    print(f"{Colors.CYAN}Total Cost:{Colors.ENDC} ${metrics['total_cost']:.4f}")
    print(f"{Colors.CYAN}Last Used:{Colors.ENDC} {metrics['last_used'] or 'Never'}")

    # Check if .claude/agents file exists
    claude_file = Path(CLAUDE_AGENTS_DIR) / f"{agent_name}.md"
    if claude_file.exists():
        print_section("Claude Instructions")
        print(f"{Colors.GREEN}✓{Colors.ENDC} Instructions file exists: {claude_file}")
    else:
        print_section("Claude Instructions")
        print(f"{Colors.YELLOW}⚠{Colors.ENDC} No instructions file found: {claude_file}")

def edit_agent(agent_name: str):
    """Open agent configuration in editor"""
    registry = load_registry()

    if agent_name not in registry:
        print_error(f"Agent '{agent_name}' not found")
        return

    # Create temp file with agent config
    temp_file = f"/tmp/agent_{agent_name}.json"
    with open(temp_file, 'w') as f:
        json.dump(registry[agent_name], f, indent=2)

    # Open in editor
    editor = os.environ.get('EDITOR', 'nano')
    print(f"\nOpening {agent_name} in {editor}...")
    print("Save and exit when done.\n")

    try:
        subprocess.run([editor, temp_file])

        # Load edited config
        with open(temp_file, 'r') as f:
            edited_agent = json.load(f)

        # Validate
        required_fields = ['name', 'description', 'role', 'tools', 'capabilities',
                          'system_prompt', 'model', 'skill_level', 'metrics']
        for field in required_fields:
            if field not in edited_agent:
                print_error(f"Missing required field: {field}")
                return

        # Confirm changes
        print("\nDo you want to save these changes? (y/n): ", end='')
        if input().lower() == 'y':
            registry[agent_name] = edited_agent
            save_registry(registry)
            print_success(f"Agent '{agent_name}' updated successfully")
        else:
            print_warning("Changes discarded")

        # Clean up
        os.remove(temp_file)

    except Exception as e:
        print_error(f"Error editing agent: {e}")

def create_agent_from_template():
    """Create a new agent from template"""
    print_header("CREATE NEW AGENT")

    # Get basic info
    print("Agent name (lowercase, no spaces): ", end='')
    name = input().strip().lower().replace(' ', '_')

    if not name:
        print_error("Agent name cannot be empty")
        return

    registry = load_registry()
    if name in registry:
        print_error(f"Agent '{name}' already exists")
        return

    print("Description (one line): ", end='')
    description = input().strip()

    print("Role (what the agent does): ", end='')
    role = input().strip()

    print("Model (claude-sonnet-4-5, claude-opus-4, claude-haiku-4): ", end='')
    model = input().strip() or "claude-sonnet-4-5"

    print("\nAvailable tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch")
    print("Tools (comma-separated): ", end='')
    tools = [t.strip() for t in input().split(',')]

    print("\nCapabilities (comma-separated, e.g., python, testing, api_design): ", end='')
    capabilities = [c.strip() for c in input().split(',')]

    print("\nSystem prompt (detailed instructions for the agent):")
    print("(Type your prompt, press Enter twice when done)")
    prompt_lines = []
    while True:
        line = input()
        if line == "" and prompt_lines and prompt_lines[-1] == "":
            prompt_lines.pop()
            break
        prompt_lines.append(line)
    system_prompt = "\n".join(prompt_lines)

    # Create agent
    new_agent = {
        "name": name,
        "description": description,
        "role": role,
        "tools": tools,
        "capabilities": capabilities,
        "system_prompt": system_prompt,
        "model": model,
        "skill_level": "novice",
        "metrics": {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "total_tokens": 0,
            "total_cost": 0.0,
            "avg_completion_time": 0.0,
            "last_used": None
        }
    }

    # Preview
    print_section("Preview")
    print(json.dumps(new_agent, indent=2))

    print("\nCreate this agent? (y/n): ", end='')
    if input().lower() == 'y':
        registry[name] = new_agent
        save_registry(registry)
        print_success(f"Agent '{name}' created successfully")

        # Offer to create .claude/agents file
        print("\nCreate .claude/agents instruction file? (y/n): ", end='')
        if input().lower() == 'y':
            create_claude_instructions(name, description, tools, model, system_prompt)
    else:
        print_warning("Agent creation cancelled")

def create_claude_instructions(name: str, description: str, tools: List[str],
                               model: str, system_prompt: str):
    """Create .claude/agents instruction file"""
    claude_agents_dir = Path(CLAUDE_AGENTS_DIR)
    claude_agents_dir.mkdir(parents=True, exist_ok=True)

    instruction_file = claude_agents_dir / f"{name}.md"

    content = f"""---
name: {name}
description: {description}
allowed_tools: {json.dumps(tools)}
model: {model}
---

{system_prompt}
"""

    with open(instruction_file, 'w') as f:
        f.write(content)

    print_success(f"Created instruction file: {instruction_file}")

def delete_agent(agent_name: str):
    """Delete an agent"""
    registry = load_registry()

    if agent_name not in registry:
        print_error(f"Agent '{agent_name}' not found")
        return

    print_warning(f"Are you sure you want to delete agent '{agent_name}'? (y/n): ", end='')
    if input().lower() != 'y':
        print("Deletion cancelled")
        return

    del registry[agent_name]
    save_registry(registry)
    print_success(f"Agent '{agent_name}' deleted")

    # Also delete .claude/agents file if exists
    claude_file = Path(CLAUDE_AGENTS_DIR) / f"{agent_name}.md"
    if claude_file.exists():
        print(f"Delete instruction file {claude_file}? (y/n): ", end='')
        if input().lower() == 'y':
            claude_file.unlink()
            print_success("Instruction file deleted")

def compare_agents(agent1: str, agent2: str):
    """Compare two agents"""
    registry = load_registry()

    if agent1 not in registry or agent2 not in registry:
        print_error("One or both agents not found")
        return

    print_header(f"COMPARING: {agent1} vs {agent2}")

    a1 = registry[agent1]
    a2 = registry[agent2]

    print_section("Basic Info")
    print(f"{Colors.CYAN}Description:{Colors.ENDC}")
    print(f"  {agent1}: {a1['description']}")
    print(f"  {agent2}: {a2['description']}")

    print(f"\n{Colors.CYAN}Model:{Colors.ENDC}")
    print(f"  {agent1}: {a1['model']}")
    print(f"  {agent2}: {a2['model']}")

    print_section("Tools")
    tools1 = set(a1['tools'])
    tools2 = set(a2['tools'])
    shared = tools1 & tools2
    unique1 = tools1 - tools2
    unique2 = tools2 - tools1

    if shared:
        print(f"{Colors.GREEN}Shared:{Colors.ENDC} {', '.join(shared)}")
    if unique1:
        print(f"{Colors.CYAN}{agent1} only:{Colors.ENDC} {', '.join(unique1)}")
    if unique2:
        print(f"{Colors.CYAN}{agent2} only:{Colors.ENDC} {', '.join(unique2)}")

    print_section("Capabilities")
    caps1 = set(a1['capabilities'])
    caps2 = set(a2['capabilities'])
    shared_caps = caps1 & caps2
    unique_caps1 = caps1 - caps2
    unique_caps2 = caps2 - caps1

    if shared_caps:
        print(f"{Colors.GREEN}Shared:{Colors.ENDC} {', '.join(list(shared_caps)[:10])}")
    if unique_caps1:
        print(f"{Colors.CYAN}{agent1} only:{Colors.ENDC} {', '.join(list(unique_caps1)[:10])}")
    if unique_caps2:
        print(f"{Colors.CYAN}{agent2} only:{Colors.ENDC} {', '.join(list(unique_caps2)[:10])}")

    print_section("Performance")
    m1 = a1['metrics']
    m2 = a2['metrics']

    print(f"{Colors.CYAN}Tasks Completed:{Colors.ENDC}")
    print(f"  {agent1}: {m1['total_tasks']}")
    print(f"  {agent2}: {m2['total_tasks']}")

    if m1['total_tasks'] > 0:
        sr1 = (m1['successful_tasks'] / m1['total_tasks']) * 100
        print(f"\n{Colors.CYAN}Success Rate:{Colors.ENDC}")
        print(f"  {agent1}: {sr1:.1f}%")

    if m2['total_tasks'] > 0:
        sr2 = (m2['successful_tasks'] / m2['total_tasks']) * 100
        if m1['total_tasks'] == 0:
            print(f"\n{Colors.CYAN}Success Rate:{Colors.ENDC}")
        print(f"  {agent2}: {sr2:.1f}%")

def show_menu():
    """Show interactive menu"""
    print_header("AGENT MANAGEMENT TOOL")

    print(f"{Colors.BOLD}Available Commands:{Colors.ENDC}")
    print(f"  {Colors.CYAN}list{Colors.ENDC}              - List all agents (brief)")
    print(f"  {Colors.CYAN}list --detailed{Colors.ENDC}   - List all agents (detailed)")
    print(f"  {Colors.CYAN}view <name>{Colors.ENDC}       - View specific agent details")
    print(f"  {Colors.CYAN}edit <name>{Colors.ENDC}       - Edit agent configuration")
    print(f"  {Colors.CYAN}create{Colors.ENDC}            - Create new agent from template")
    print(f"  {Colors.CYAN}delete <name>{Colors.ENDC}     - Delete an agent")
    print(f"  {Colors.CYAN}compare <n1> <n2>{Colors.ENDC} - Compare two agents")
    print(f"  {Colors.CYAN}help{Colors.ENDC}              - Show this menu")
    print(f"  {Colors.CYAN}exit{Colors.ENDC}              - Exit")

    print(f"\n{Colors.YELLOW}Examples:{Colors.ENDC}")
    print(f"  {Colors.GREEN}view designer{Colors.ENDC}")
    print(f"  {Colors.GREEN}edit security{Colors.ENDC}")
    print(f"  {Colors.GREEN}compare code_writer designer{Colors.ENDC}")

def main():
    """Main entry point"""
    if len(sys.argv) == 1:
        # Interactive mode
        show_menu()
        while True:
            try:
                print(f"\n{Colors.BOLD}>{Colors.ENDC} ", end='')
                cmd = input().strip().split()

                if not cmd:
                    continue

                action = cmd[0].lower()

                if action == 'exit':
                    print("Goodbye!")
                    break
                elif action == 'help':
                    show_menu()
                elif action == 'list':
                    detailed = '--detailed' in cmd
                    list_agents(detailed)
                elif action == 'view' and len(cmd) > 1:
                    view_agent(cmd[1])
                elif action == 'edit' and len(cmd) > 1:
                    edit_agent(cmd[1])
                elif action == 'create':
                    create_agent_from_template()
                elif action == 'delete' and len(cmd) > 1:
                    delete_agent(cmd[1])
                elif action == 'compare' and len(cmd) > 2:
                    compare_agents(cmd[1], cmd[2])
                else:
                    print_error("Invalid command. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print_error(f"Error: {e}")

    else:
        # Command line mode
        action = sys.argv[1].lower()

        if action == 'list':
            detailed = '--detailed' in sys.argv
            list_agents(detailed)
        elif action == 'view' and len(sys.argv) > 2:
            view_agent(sys.argv[2])
        elif action == 'edit' and len(sys.argv) > 2:
            edit_agent(sys.argv[2])
        elif action == 'create':
            create_agent_from_template()
        elif action == 'delete' and len(sys.argv) > 2:
            delete_agent(sys.argv[2])
        elif action == 'compare' and len(sys.argv) > 3:
            compare_agents(sys.argv[2], sys.argv[3])
        else:
            show_menu()

if __name__ == '__main__':
    main()
