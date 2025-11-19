#!/usr/bin/env python3
"""
Multi-Agent Workflow Test
Demonstrates real agent collaboration
"""
import asyncio
from agents import OrchestratorV2

async def main():
    orchestrator = OrchestratorV2()

    # Task that requires implementation + testing
    # Must match pattern: r'\b(implement|create|build|add|write)\s+(feature|functionality|function|class|module)'
    task_desc = "Implement feature in calculator.py: add power function that raises a number to an exponent"

    print("\n" + "="*80)
    print("🎯 MULTI-AGENT WORKFLOW TEST")
    print("="*80)
    print(f"Task: {task_desc}\n")

    # Get delegation plan
    result = await orchestrator.delegate_task(
        task_description=task_desc,
        max_agents=3
    )

    if result['success']:
        plan = result['delegation_plan']

        print("\n" + "="*80)
        print("📋 AGENTS ASSIGNED:")
        print("="*80)

        for i, step in enumerate(plan['steps'], 1):
            if step['type'] == 'parallel':
                print(f"\n{i}. PARALLEL EXECUTION:")
                for p in step['parallel_steps']:
                    print(f"   - {p['agent']}: {p['agent_description']}")
            else:
                print(f"\n{i}. {step['agent'].upper()} ({step['type']})")
                print(f"   Description: {step['agent_description']}")
                print(f"   Confidence: {step['confidence']:.0%}")
                print(f"   Reasoning: {step['reasoning']}")

        print("\n" + "="*80)
        print("✅ Ready to execute agents sequentially")
        print("="*80)

        return plan
    else:
        print(f"\n❌ Failed: {result.get('error')}")
        return None

if __name__ == "__main__":
    plan = asyncio.run(main())

    if plan:
        print("\n📝 Next: Execute each agent using Claude Code's Task tool")
