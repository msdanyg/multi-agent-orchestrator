#!/usr/bin/env python3
"""
Real system test - creates delegation plan
"""
import asyncio
from agents import OrchestratorV2

async def main():
    orchestrator = OrchestratorV2()

    # First test the task analysis
    # Note: Must match pattern r'\b(review|analyze|examine|inspect)\s+(code|implementation|module|function)'
    task_desc = "Review code in calculator.py for quality and architecture issues"
    analysis = orchestrator.router.analyze_task(task_desc)

    print("\n🔍 TASK ANALYSIS:")
    print(f"  Task type: {analysis.task_type}")
    print(f"  Required capabilities: {analysis.required_capabilities}")
    print(f"  Complexity: {analysis.complexity}")

    # Simple test task - explicit code review request
    result = await orchestrator.delegate_task(
        task_description=task_desc,
        max_agents=2
    )

    print("\n" + "="*80)
    print("📋 DELEGATION PLAN READY")
    print("="*80)

    print(f"\nSuccess: {result['success']}")
    print(f"Agents assigned: {result.get('agents_assigned', [])}")

    if result['success'] and result.get('agents_assigned'):
        plan = result['delegation_plan']
        print(f"\nTotal steps: {plan['total_steps']}")

        # Print first agent's prompt
        if plan['steps']:
            step = plan['steps'][0]
            print(f"\nAgent: {step['agent']}")
            print(f"Tools: {', '.join(step['tools'])}")
            print(f"\nPrompt for Claude Code Task tool:")
            print("-"*80)
            print(step['prompt'])
            print("-"*80)
    else:
        print("\n⚠️ No agents were assigned to this task!")
        print("This might mean the task didn't match any agent capabilities.")

    return result

if __name__ == "__main__":
    result = asyncio.run(main())
