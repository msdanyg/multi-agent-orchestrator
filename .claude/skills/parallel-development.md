# Parallel Development Pattern

## Purpose
Enable multiple agents to work simultaneously on independent components that integrate later.

## When to Use
- **Frontend + Backend** development that can progress independently
- **Multiple microservices** that share contracts but separate implementation
- **Research + Implementation** where research informs but doesn't block
- **Component development** with clear interfaces

## Pattern Diagram
```
Orchestrator
    ├─> Frontend Agent (UI components)
    ├─> Backend Agent (API endpoints)
    ├─> Database Agent (Schema design)
    └─> Test Agent (Test scenarios)
        ↓
    Integration & Validation
```

## Implementation Example

```python
async def parallel_development_pattern(requirements):
    """Execute parallel development workflow"""

    # Break down into independent tasks
    tasks = {
        'frontend': {
            'agent': 'code_writer',
            'task': f"Build React UI for: {requirements['ui']}",
            'dependencies': []
        },
        'backend': {
            'agent': 'code_writer',
            'task': f"Build FastAPI endpoints for: {requirements['api']}",
            'dependencies': []
        },
        'tests': {
            'agent': 'tester',
            'task': f"Write integration tests for: {requirements['tests']}",
            'dependencies': ['frontend', 'backend']  # Runs after
        }
    }

    # Execute independent tasks in parallel
    parallel_tasks = [
        delegate_to_agent(task['agent'], task['task'])
        for task in tasks.values()
        if not task['dependencies']
    ]

    results = await asyncio.gather(*parallel_tasks)

    # Execute dependent tasks
    test_result = await delegate_to_agent(
        tasks['tests']['agent'],
        tasks['tests']['task']
    )

    return aggregate_results(results + [test_result])
```

## Coordination Points

### 1. Contract Definition
Before parallel work begins:
- Define API contracts
- Agree on data models
- Establish interface boundaries
- Document shared types

### 2. Progress Checkpoints
During parallel execution:
- Regular status updates
- Blocker identification
- Dependency verification
- Integration readiness check

### 3. Integration Phase
After parallel work completes:
- Merge outputs
- Run integration tests
- Resolve conflicts
- Validate end-to-end

## Success Criteria
- ✅ 2x-3x faster than sequential
- ✅ No blocking dependencies
- ✅ Clear integration points
- ✅ Independent testing possible
- ✅ Minimal rework during integration

## Common Pitfalls

### ❌ Unclear Interfaces
**Problem:** Agents make conflicting assumptions
**Solution:** Define contracts upfront in CLAUDE.md

### ❌ Hidden Dependencies
**Problem:** "Independent" tasks actually depend on each other
**Solution:** Map dependencies explicitly before delegation

### ❌ Integration Hell
**Problem:** Components don't fit together
**Solution:** Define integration tests before parallel work

### ❌ Duplicate Work
**Problem:** Multiple agents implement same functionality
**Solution:** Clear responsibility assignment

## Metrics to Track
- **Parallelization Factor**: Tasks completed / Wall clock time
- **Integration Issues**: Conflicts found during merge
- **Rework Percentage**: Code changed after integration
- **Time to Integration**: How fast components connect

## Example Use Cases

### Use Case 1: Full-Stack Feature
```
Research Agent → (Frontend Agent || Backend Agent) → Integration Test → Deploy
```

### Use Case 2: Microservices
```
Service A Agent || Service B Agent || Service C Agent → Integration → Deploy
```

### Use Case 3: Multi-Platform
```
iOS Agent || Android Agent || Web Agent → QA Agent → Release
```

## Best Practices
1. Define contracts before parallel work
2. Use mocks/stubs for missing dependencies
3. Regular synchronization points
4. Automated integration testing
5. Clear ownership boundaries
6. Document assumptions
7. Plan for integration time

## Related Patterns
- **Sequential Pipeline**: When tasks must be sequential
- **Review & Approval**: Add review after parallel work
- **Meta-Agent Hierarchy**: For complex multi-team coordination
