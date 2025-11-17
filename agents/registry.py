"""
Agent Registry System
Manages agent definitions, capabilities, and performance tracking
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum


class SkillLevel(Enum):
    """Agent skill progression levels"""
    NOVICE = "novice"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"
    MASTER = "master"


@dataclass
class AgentMetrics:
    """Performance metrics for an agent"""
    total_tasks: int = 0
    successful_tasks: int = 0
    failed_tasks: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    avg_completion_time: float = 0.0
    last_used: Optional[str] = None

    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage"""
        if self.total_tasks == 0:
            return 0.0
        return (self.successful_tasks / self.total_tasks) * 100


@dataclass
class AgentDefinition:
    """Complete agent specification"""
    name: str
    description: str
    role: str
    tools: List[str]
    capabilities: List[str]
    system_prompt: str
    model: str = "claude-sonnet-4-5"
    skill_level: str = SkillLevel.NOVICE.value
    metrics: Optional[AgentMetrics] = None

    def __post_init__(self):
        if self.metrics is None:
            self.metrics = AgentMetrics()


class AgentRegistry:
    """Central registry for managing agents"""

    def __init__(self, registry_path: str = "agents/registry.json"):
        self.registry_path = Path(registry_path)
        self.agents: Dict[str, AgentDefinition] = {}
        self.load_registry()

    def load_registry(self):
        """Load agent registry from disk"""
        if self.registry_path.exists():
            with open(self.registry_path, 'r') as f:
                data = json.load(f)
                for name, agent_data in data.items():
                    metrics_data = agent_data.pop('metrics', {})
                    metrics = AgentMetrics(**metrics_data)
                    agent_data['metrics'] = metrics
                    self.agents[name] = AgentDefinition(**agent_data)
        else:
            # Initialize with default agents
            self._initialize_default_agents()
            self.save_registry()

    def save_registry(self):
        """Persist registry to disk"""
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        data = {}
        for name, agent in self.agents.items():
            agent_dict = asdict(agent)
            data[name] = agent_dict

        with open(self.registry_path, 'w') as f:
            json.dump(data, f, indent=2)

    def register_agent(self, agent: AgentDefinition) -> None:
        """Register a new agent"""
        self.agents[agent.name] = agent
        self.save_registry()

    def get_agent(self, name: str) -> Optional[AgentDefinition]:
        """Retrieve agent by name"""
        return self.agents.get(name)

    def find_agents_by_capability(self, capability: str) -> List[AgentDefinition]:
        """Find all agents with a specific capability"""
        return [
            agent for agent in self.agents.values()
            if capability.lower() in [c.lower() for c in agent.capabilities]
        ]

    def find_best_agent(self, capabilities: List[str], exclude: List[str] = None) -> Optional[AgentDefinition]:
        """Find the best agent matching required capabilities"""
        exclude = exclude or []
        candidates = []

        for agent in self.agents.values():
            if agent.name in exclude:
                continue

            # Calculate capability match score
            agent_caps = set(c.lower() for c in agent.capabilities)
            required_caps = set(c.lower() for c in capabilities)

            match_count = len(agent_caps.intersection(required_caps))
            if match_count > 0:
                # Score based on: capability match, success rate, skill level
                skill_bonus = {
                    SkillLevel.NOVICE.value: 1.0,
                    SkillLevel.INTERMEDIATE.value: 1.2,
                    SkillLevel.EXPERT.value: 1.5,
                    SkillLevel.MASTER.value: 2.0
                }.get(agent.skill_level, 1.0)

                success_rate = agent.metrics.success_rate if agent.metrics else 50.0
                score = match_count * skill_bonus * (success_rate / 100)

                candidates.append((score, agent))

        if not candidates:
            return None

        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]

    def update_metrics(self, agent_name: str, success: bool, tokens: int, cost: float, duration: float):
        """Update agent performance metrics"""
        agent = self.get_agent(agent_name)
        if not agent or not agent.metrics:
            return

        metrics = agent.metrics
        metrics.total_tasks += 1
        if success:
            metrics.successful_tasks += 1
        else:
            metrics.failed_tasks += 1

        metrics.total_tokens += tokens
        metrics.total_cost += cost

        # Update rolling average completion time
        if metrics.avg_completion_time == 0:
            metrics.avg_completion_time = duration
        else:
            metrics.avg_completion_time = (metrics.avg_completion_time * (metrics.total_tasks - 1) + duration) / metrics.total_tasks

        metrics.last_used = datetime.now().isoformat()

        # Update skill level based on performance
        self._update_skill_level(agent)

        self.save_registry()

    def _update_skill_level(self, agent: AgentDefinition):
        """Automatically upgrade agent skill level based on performance"""
        if not agent.metrics:
            return

        tasks = agent.metrics.total_tasks
        success_rate = agent.metrics.success_rate

        # Progression thresholds
        if tasks >= 50 and success_rate >= 90 and agent.skill_level == SkillLevel.EXPERT.value:
            agent.skill_level = SkillLevel.MASTER.value
        elif tasks >= 20 and success_rate >= 85 and agent.skill_level == SkillLevel.INTERMEDIATE.value:
            agent.skill_level = SkillLevel.EXPERT.value
        elif tasks >= 5 and success_rate >= 75 and agent.skill_level == SkillLevel.NOVICE.value:
            agent.skill_level = SkillLevel.INTERMEDIATE.value

    def get_all_agents(self) -> List[AgentDefinition]:
        """Get all registered agents"""
        return list(self.agents.values())

    def get_agent_stats(self) -> Dict[str, Any]:
        """Get registry-wide statistics"""
        total_agents = len(self.agents)
        total_tasks = sum(a.metrics.total_tasks for a in self.agents.values() if a.metrics)
        total_cost = sum(a.metrics.total_cost for a in self.agents.values() if a.metrics)

        skill_distribution = {}
        for level in SkillLevel:
            count = sum(1 for a in self.agents.values() if a.skill_level == level.value)
            skill_distribution[level.value] = count

        return {
            "total_agents": total_agents,
            "total_tasks_completed": total_tasks,
            "total_cost": total_cost,
            "skill_distribution": skill_distribution
        }

    def _initialize_default_agents(self):
        """Create default specialist agents"""

        # Code Analyst
        self.agents["code_analyst"] = AgentDefinition(
            name="code_analyst",
            description="Expert in code analysis, architecture review, and refactoring recommendations",
            role="Analyzes code structure, identifies issues, suggests improvements",
            tools=["Read", "Grep", "Glob"],
            capabilities=["code_review", "architecture", "python", "javascript", "typescript", "refactoring", "best_practices"],
            system_prompt="""You are an expert code analyst specializing in:
- Code architecture analysis and design pattern identification
- Code quality assessment and technical debt identification
- Refactoring recommendations and best practices
- Performance optimization opportunities
- Security vulnerability detection

Always provide specific, actionable recommendations with file paths and line numbers.
Focus on clarity and practical improvements.""",
            model="claude-sonnet-4-5"
        )

        # Code Writer
        self.agents["code_writer"] = AgentDefinition(
            name="code_writer",
            description="Implements features, fixes bugs, and writes clean, maintainable code",
            role="Writes and modifies code based on specifications",
            tools=["Read", "Write", "Edit", "Glob"],
            capabilities=["implementation", "python", "javascript", "typescript", "bug_fixing", "feature_development"],
            system_prompt="""You are an expert software developer specializing in:
- Clean, maintainable code implementation
- Following established code patterns and conventions
- Writing comprehensive inline documentation
- Bug fixing with minimal changes
- Feature implementation with proper error handling

Always test your code logic before writing. Follow existing code style and patterns.""",
            model="claude-sonnet-4-5"
        )

        # Tester
        self.agents["tester"] = AgentDefinition(
            name="tester",
            description="Runs tests, validates functionality, and ensures quality",
            role="Executes test suites and validates code quality",
            tools=["Bash", "Read", "Grep"],
            capabilities=["testing", "qa", "validation", "pytest", "jest", "unittest"],
            system_prompt="""You are a quality assurance specialist focusing on:
- Running comprehensive test suites
- Analyzing test results and failures
- Identifying untested code paths
- Validating edge cases
- Performance testing

Provide clear summaries of test results with failure details and suggestions for fixes.""",
            model="claude-sonnet-4-5"
        )

        # Researcher
        self.agents["researcher"] = AgentDefinition(
            name="researcher",
            description="Gathers information, researches best practices, and finds documentation",
            role="Conducts research and information gathering",
            tools=["WebSearch", "WebFetch", "Read", "Write"],
            capabilities=["research", "documentation", "best_practices", "libraries", "apis"],
            system_prompt="""You are a research specialist excellent at:
- Finding relevant documentation and examples
- Researching best practices and industry standards
- Comparing libraries and tools
- Gathering technical specifications
- Synthesizing information from multiple sources

Always cite sources and provide actionable insights, not just summaries.""",
            model="claude-sonnet-4-5"
        )

        # DevOps Engineer
        self.agents["devops"] = AgentDefinition(
            name="devops",
            description="Handles builds, deployments, environment setup, and infrastructure",
            role="Manages development operations and infrastructure",
            tools=["Bash", "Read", "Write", "Edit"],
            capabilities=["devops", "deployment", "docker", "ci_cd", "build", "environment"],
            system_prompt="""You are a DevOps engineer specializing in:
- Build system configuration and optimization
- Deployment automation
- Environment setup and configuration
- Docker and containerization
- CI/CD pipeline management

Focus on reliability, reproducibility, and clear documentation of setup steps.""",
            model="claude-sonnet-4-5"
        )

        # Documentation Writer
        self.agents["docs_writer"] = AgentDefinition(
            name="docs_writer",
            description="Creates clear, comprehensive documentation and guides",
            role="Writes technical documentation",
            tools=["Read", "Write", "Glob"],
            capabilities=["documentation", "technical_writing", "markdown", "tutorials", "api_docs"],
            system_prompt="""You are a technical documentation specialist expert in:
- Writing clear, user-friendly documentation
- Creating tutorials and getting-started guides
- Documenting APIs and code interfaces
- Structuring information logically
- Using proper markdown formatting

Always write for your target audience and include practical examples.""",
            model="claude-sonnet-4-5"
        )
