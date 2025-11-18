"""
Task Router
Analyzes tasks and selects optimal agents for execution
"""
import re
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from .registry import AgentRegistry, AgentDefinition


@dataclass
class TaskAnalysis:
    """Results of task analysis"""
    task_type: str
    required_capabilities: List[str]
    complexity: str  # simple, medium, complex
    can_parallelize: bool
    estimated_subtasks: int
    keywords: List[str]


@dataclass
class AgentAssignment:
    """Agent assignment for a task"""
    agent: AgentDefinition
    priority: str  # primary, supporting, optional
    confidence_score: float
    reason: str


class TaskRouter:
    """Intelligent task routing and agent selection"""

    # Task type patterns (regex patterns -> task type, capabilities)
    TASK_PATTERNS = {
        r'\b(review|analyze|examine|inspect)\s+(code|implementation|module|function)': (
            'code_analysis',
            ['code_review', 'architecture', 'best_practices']
        ),
        r'\b(implement|create|build|add|write)\s+(feature|functionality|function|class|module)': (
            'implementation',
            ['implementation', 'feature_development']
        ),
        r'\b(refactor|improve|optimize|clean\s*up)\s+(code|implementation)': (
            'refactoring',
            ['refactoring', 'code_review', 'implementation']
        ),
        r'\b(fix|resolve|debug)\s+(bug|issue|error|problem)': (
            'bug_fixing',
            ['bug_fixing', 'implementation']
        ),
        r'\b(test|validate|verify|check)\s+(code|functionality|feature|implementation)': (
            'testing',
            ['testing', 'qa', 'validation']
        ),
        r'\b(research|investigate|find|search\s*for)\s+(documentation|library|best\s*practice|solution)': (
            'research',
            ['research', 'documentation', 'best_practices']
        ),
        r'\b(document|write\s*docs|create\s*documentation|add\s*comments)': (
            'documentation',
            ['documentation', 'technical_writing']
        ),
        r'\b(deploy|build|setup|configure)\s+(application|environment|pipeline|infrastructure)': (
            'devops',
            ['devops', 'deployment', 'environment']
        ),
        r'\b(docker|containerize|kubernetes)': (
            'devops',
            ['devops', 'docker']
        ),
    }

    # Language detection patterns
    LANGUAGE_PATTERNS = {
        r'\bpython\b': 'python',
        r'\bjavascript\b|\bjs\b|\bnode\b': 'javascript',
        r'\btypescript\b|\bts\b': 'typescript',
        r'\bjava\b': 'java',
        r'\bgo\b|\bgolang\b': 'go',
        r'\brust\b': 'rust',
        r'\bc\+\+\b|\bcpp\b': 'cpp',
    }

    # Complexity indicators
    COMPLEXITY_HIGH = [
        'refactor', 'architecture', 'system', 'multiple', 'complex',
        'scalable', 'distributed', 'migration'
    ]
    COMPLEXITY_MEDIUM = [
        'implement', 'feature', 'integration', 'api', 'module'
    ]

    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    def analyze_task(self, task_description: str) -> TaskAnalysis:
        """Analyze a task to determine requirements and characteristics"""
        task_lower = task_description.lower()

        # Detect task type and base capabilities
        task_type = "general"
        capabilities = []

        for pattern, (ttype, caps) in self.TASK_PATTERNS.items():
            if re.search(pattern, task_lower, re.IGNORECASE):
                task_type = ttype
                capabilities.extend(caps)
                break

        # Detect programming language
        for pattern, lang in self.LANGUAGE_PATTERNS.items():
            if re.search(pattern, task_lower, re.IGNORECASE):
                capabilities.append(lang)

        # Determine complexity
        complexity = "simple"
        high_count = sum(1 for keyword in self.COMPLEXITY_HIGH if keyword in task_lower)
        medium_count = sum(1 for keyword in self.COMPLEXITY_MEDIUM if keyword in task_lower)

        if high_count >= 2:
            complexity = "complex"
        elif high_count >= 1 or medium_count >= 2:
            complexity = "medium"

        # Determine if parallelizable
        can_parallelize = self._can_parallelize(task_description, task_type)

        # Estimate subtasks
        estimated_subtasks = self._estimate_subtasks(task_description, complexity)

        # Extract keywords
        keywords = self._extract_keywords(task_description)

        return TaskAnalysis(
            task_type=task_type,
            required_capabilities=list(set(capabilities)),
            complexity=complexity,
            can_parallelize=can_parallelize,
            estimated_subtasks=estimated_subtasks,
            keywords=keywords
        )

    def select_agents(self, task_description: str, max_agents: int = 3) -> List[AgentAssignment]:
        """Select optimal agents for a task"""
        analysis = self.analyze_task(task_description)
        assignments = []

        # Find agents matching required capabilities
        if analysis.required_capabilities:
            primary_agent = self.registry.find_best_agent(analysis.required_capabilities)
            if primary_agent:
                assignments.append(AgentAssignment(
                    agent=primary_agent,
                    priority="primary",
                    confidence_score=self._calculate_confidence(primary_agent, analysis),
                    reason=f"Best match for {', '.join(analysis.required_capabilities[:2])}"
                ))

        # Add supporting agents based on task type
        supporting_agents = self._find_supporting_agents(analysis, exclude=[a.agent.name for a in assignments])
        assignments.extend(supporting_agents[:max_agents - len(assignments)])

        # Fallback: if no agents selected, use code_writer as default
        if not assignments:
            code_writer = self.registry.get_agent('code_writer')
            if code_writer:
                assignments.append(AgentAssignment(
                    agent=code_writer,
                    priority="primary",
                    confidence_score=0.0,
                    reason="Default agent for general tasks"
                ))

        return assignments

    def _calculate_confidence(self, agent: AgentDefinition, analysis: TaskAnalysis) -> float:
        """Calculate confidence score for agent assignment"""
        # Base score on capability overlap
        agent_caps = set(c.lower() for c in agent.capabilities)
        required_caps = set(c.lower() for c in analysis.required_capabilities)

        if not required_caps:
            overlap = 0.5
        else:
            overlap = len(agent_caps.intersection(required_caps)) / len(required_caps)

        # Adjust for success rate
        success_rate = agent.metrics.success_rate / 100 if agent.metrics else 0.5

        # Adjust for skill level
        skill_multiplier = {
            'novice': 0.8,
            'intermediate': 1.0,
            'expert': 1.2,
            'master': 1.5
        }.get(agent.skill_level, 1.0)

        confidence = overlap * success_rate * skill_multiplier

        # Cap at 0.95
        return min(confidence, 0.95)

    def _find_supporting_agents(self, analysis: TaskAnalysis, exclude: List[str]) -> List[AgentAssignment]:
        """Find supporting agents based on task analysis"""
        supporting = []

        # For implementation tasks, add tester
        if analysis.task_type in ['implementation', 'bug_fixing', 'refactoring']:
            tester = self.registry.get_agent('tester')
            if tester and tester.name not in exclude:
                supporting.append(AgentAssignment(
                    agent=tester,
                    priority="supporting",
                    confidence_score=0.8,
                    reason="Validate implementation"
                ))

        # For complex tasks, add researcher
        if analysis.complexity == 'complex':
            researcher = self.registry.get_agent('researcher')
            if researcher and researcher.name not in exclude:
                supporting.append(AgentAssignment(
                    agent=researcher,
                    priority="optional",
                    confidence_score=0.6,
                    reason="Research best practices for complex task"
                ))

        # For implementation, add code analyst for review
        if analysis.task_type == 'implementation' and analysis.complexity in ['medium', 'complex']:
            analyst = self.registry.get_agent('code_analyst')
            if analyst and analyst.name not in exclude:
                supporting.append(AgentAssignment(
                    agent=analyst,
                    priority="supporting",
                    confidence_score=0.7,
                    reason="Review implementation quality"
                ))

        return supporting

    def _can_parallelize(self, task_description: str, task_type: str) -> bool:
        """Determine if task can be parallelized"""
        # Keywords indicating sequential work
        sequential_keywords = ['then', 'after', 'before', 'first', 'next', 'finally', 'step']

        task_lower = task_description.lower()
        has_sequential = any(keyword in task_lower for keyword in sequential_keywords)

        # Research and analysis can often be parallelized
        parallelizable_types = ['research', 'code_analysis', 'testing']

        return task_type in parallelizable_types and not has_sequential

    def _estimate_subtasks(self, task_description: str, complexity: str) -> int:
        """Estimate number of subtasks"""
        # Count explicit task markers
        task_markers = ['and', ',', ';', 'then', 'also', 'plus']
        count = 1  # Base task

        task_lower = task_description.lower()
        for marker in task_markers:
            count += task_lower.count(marker)

        # Adjust for complexity
        complexity_multiplier = {
            'simple': 1,
            'medium': 1.5,
            'complex': 2
        }.get(complexity, 1)

        return max(1, int(count * complexity_multiplier))

    def _extract_keywords(self, task_description: str) -> List[str]:
        """Extract important keywords from task description"""
        # Remove common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during'
        }

        words = re.findall(r'\b\w+\b', task_description.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 3]

        # Return top 10 most relevant
        return keywords[:10]

    def generate_agent_prompt(self, agent: AgentDefinition, task_description: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate a specialized prompt for an agent"""
        prompt_parts = [task_description]

        # Add context if available
        if context:
            if 'files' in context:
                prompt_parts.append(f"\nRelevant files: {', '.join(context['files'])}")
            if 'previous_results' in context:
                prompt_parts.append(f"\nPrevious results: {context['previous_results']}")
            if 'constraints' in context:
                prompt_parts.append(f"\nConstraints: {context['constraints']}")

        # Add agent-specific guidance
        prompt_parts.append(f"\nYou are the {agent.role}. Focus on your area of expertise.")

        return "\n".join(prompt_parts)
