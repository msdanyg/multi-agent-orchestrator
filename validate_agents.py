#!/usr/bin/env python3
"""
Agent Configuration Validator
Checks for common issues in agent configurations
"""

import json
import sys
from pathlib import Path
from typing import List, Tuple

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

REGISTRY_PATH = "agents/registry.json"
REQUIRED_FIELDS = [
    'name', 'description', 'role', 'tools', 'capabilities',
    'system_prompt', 'model', 'skill_level', 'metrics'
]
VALID_MODELS = ['claude-sonnet-4-5', 'claude-opus-4', 'claude-haiku-4']
VALID_SKILL_LEVELS = ['novice', 'intermediate', 'expert', 'master']
VALID_TOOLS = [
    'Read', 'Write', 'Edit', 'Glob', 'Grep', 'Bash',
    'WebSearch', 'WebFetch', 'TodoWrite', 'Task'
]

def load_registry():
    """Load registry file"""
    try:
        with open(REGISTRY_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Colors.RED}✗ Registry file not found: {REGISTRY_PATH}{Colors.ENDC}")
        return None
    except json.JSONDecodeError as e:
        print(f"{Colors.RED}✗ Invalid JSON: {e}{Colors.ENDC}")
        return None

def validate_agent(agent_name: str, agent_data: dict) -> List[Tuple[str, str]]:
    """Validate a single agent configuration"""
    issues = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in agent_data:
            issues.append(('error', f"Missing required field: {field}"))

    # Validate name matches key
    if 'name' in agent_data and agent_data['name'] != agent_name:
        issues.append(('warning', f"Agent name '{agent_data['name']}' doesn't match key '{agent_name}'"))

    # Validate model
    if 'model' in agent_data and agent_data['model'] not in VALID_MODELS:
        issues.append(('warning', f"Unknown model: {agent_data['model']}. Valid: {VALID_MODELS}"))

    # Validate skill level
    if 'skill_level' in agent_data and agent_data['skill_level'] not in VALID_SKILL_LEVELS:
        issues.append(('error', f"Invalid skill level: {agent_data['skill_level']}. Valid: {VALID_SKILL_LEVELS}"))

    # Validate tools
    if 'tools' in agent_data:
        if not isinstance(agent_data['tools'], list):
            issues.append(('error', "Tools must be a list"))
        else:
            for tool in agent_data['tools']:
                if tool not in VALID_TOOLS:
                    issues.append(('warning', f"Unknown tool: {tool}"))

    # Validate capabilities
    if 'capabilities' in agent_data:
        if not isinstance(agent_data['capabilities'], list):
            issues.append(('error', "Capabilities must be a list"))
        elif len(agent_data['capabilities']) == 0:
            issues.append(('warning', "Agent has no capabilities defined"))

    # Validate metrics structure
    if 'metrics' in agent_data:
        metrics = agent_data['metrics']
        required_metrics = [
            'total_tasks', 'successful_tasks', 'failed_tasks',
            'total_tokens', 'total_cost', 'avg_completion_time', 'last_used'
        ]
        for metric in required_metrics:
            if metric not in metrics:
                issues.append(('warning', f"Missing metric: {metric}"))

    # Check for empty strings
    for field in ['description', 'role', 'system_prompt']:
        if field in agent_data and not agent_data[field]:
            issues.append(('warning', f"Empty {field}"))

    # Validate system prompt length
    if 'system_prompt' in agent_data:
        prompt_len = len(agent_data['system_prompt'])
        if prompt_len < 50:
            issues.append(('warning', f"System prompt is very short ({prompt_len} chars)"))
        elif prompt_len > 5000:
            issues.append(('warning', f"System prompt is very long ({prompt_len} chars)"))

    return issues

def main():
    """Main validation function"""
    print(f"\n{Colors.BOLD}=== Agent Configuration Validator ==={Colors.ENDC}\n")

    registry = load_registry()
    if registry is None:
        sys.exit(1)

    total_agents = len(registry)
    agents_with_issues = 0
    total_errors = 0
    total_warnings = 0

    for agent_name, agent_data in registry.items():
        issues = validate_agent(agent_name, agent_data)

        if issues:
            agents_with_issues += 1
            print(f"{Colors.BOLD}Agent: {agent_name}{Colors.ENDC}")

            for issue_type, message in issues:
                if issue_type == 'error':
                    total_errors += 1
                    print(f"  {Colors.RED}✗ ERROR: {message}{Colors.ENDC}")
                else:
                    total_warnings += 1
                    print(f"  {Colors.YELLOW}⚠ WARNING: {message}{Colors.ENDC}")
            print()

    # Summary
    print(f"{Colors.BOLD}{'='*50}{Colors.ENDC}")
    print(f"{Colors.BOLD}Summary:{Colors.ENDC}")
    print(f"  Total Agents: {total_agents}")
    print(f"  Agents with Issues: {agents_with_issues}")

    if total_errors > 0:
        print(f"  {Colors.RED}Errors: {total_errors}{Colors.ENDC}")
    else:
        print(f"  {Colors.GREEN}Errors: 0{Colors.ENDC}")

    if total_warnings > 0:
        print(f"  {Colors.YELLOW}Warnings: {total_warnings}{Colors.ENDC}")
    else:
        print(f"  {Colors.GREEN}Warnings: 0{Colors.ENDC}")

    if total_errors == 0 and total_warnings == 0:
        print(f"\n{Colors.GREEN}✓ All agents validated successfully!{Colors.ENDC}\n")
        return 0
    elif total_errors == 0:
        print(f"\n{Colors.YELLOW}⚠ Validation completed with warnings{Colors.ENDC}\n")
        return 0
    else:
        print(f"\n{Colors.RED}✗ Validation failed with errors{Colors.ENDC}\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
