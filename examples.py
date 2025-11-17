#!/usr/bin/env python3
"""
Example usage of the Multi-Agent Management Framework
"""
import asyncio
from agents import Orchestrator


async def example_code_refactoring():
    """Example: Refactoring code"""
    print("Example 1: Code Refactoring Task\n")

    orchestrator = Orchestrator()

    result = await orchestrator.execute_task(
        task_description="Refactor the authentication module to improve security and use modern best practices",
        context={
            'files': ['auth.py', 'models.py'],
            'constraints': 'Maintain backward compatibility'
        }
    )

    print(f"\nResult: {'Success' if result['success'] else 'Failed'}")
    print(f"Time: {result['execution_time']:.2f}s")


async def example_bug_fixing():
    """Example: Fixing bugs"""
    print("\nExample 2: Bug Fixing Task\n")

    orchestrator = Orchestrator()

    result = await orchestrator.execute_task(
        task_description="Fix the memory leak in the data processing pipeline",
        context={
            'files': ['pipeline.py', 'processor.py'],
        },
        max_agents=2
    )

    print(f"\nResult: {'Success' if result['success'] else 'Failed'}")


async def example_feature_implementation():
    """Example: Implementing new feature"""
    print("\nExample 3: Feature Implementation\n")

    orchestrator = Orchestrator()

    result = await orchestrator.execute_task(
        task_description="Implement a new user dashboard with analytics and charts using React and TypeScript",
        max_agents=4
    )

    print(f"\nResult: {'Success' if result['success'] else 'Failed'}")
    print(f"Agents used: {', '.join(result['agents_used'])}")


async def example_research_task():
    """Example: Research task"""
    print("\nExample 4: Research Task\n")

    orchestrator = Orchestrator()

    result = await orchestrator.execute_task(
        task_description="Research best practices for implementing microservices architecture and document findings",
        max_agents=2
    )

    print(f"\nResult: {'Success' if result['success'] else 'Failed'}")


async def example_system_status():
    """Example: Getting system status"""
    print("\nExample 5: System Status\n")

    orchestrator = Orchestrator()
    status = orchestrator.get_system_status()

    print("Registry:", status['registry'])
    print("TMUX:", status['tmux'])
    print("Skills:", status['skills'])


async def example_complex_workflow():
    """Example: Complex multi-step workflow"""
    print("\nExample 6: Complex Workflow\n")

    orchestrator = Orchestrator()

    # Step 1: Research
    print("Step 1: Research phase...")
    research_result = await orchestrator.execute_task(
        task_description="Research JWT authentication best practices for Python",
        max_agents=1
    )

    # Step 2: Implementation
    if research_result['success']:
        print("\nStep 2: Implementation phase...")
        impl_result = await orchestrator.execute_task(
            task_description="Implement JWT authentication based on researched best practices",
            context={
                'previous_results': 'Research completed successfully'
            },
            max_agents=2
        )

        # Step 3: Testing
        if impl_result['success']:
            print("\nStep 3: Testing phase...")
            test_result = await orchestrator.execute_task(
                task_description="Test the JWT authentication implementation",
                max_agents=1
            )

            print(f"\n✅ Workflow completed successfully!")


async def example_parallel_tasks():
    """Example: Executing multiple independent tasks in parallel"""
    print("\nExample 7: Parallel Task Execution\n")

    orchestrator = Orchestrator()

    tasks = [
        orchestrator.execute_task("Review the database models for optimization opportunities"),
        orchestrator.execute_task("Update the API documentation"),
        orchestrator.execute_task("Run the test suite and analyze results")
    ]

    results = await asyncio.gather(*tasks)

    for i, result in enumerate(results, 1):
        print(f"Task {i}: {'✅ Success' if result['success'] else '❌ Failed'}")


async def main():
    """Run all examples"""
    examples = [
        ("Code Refactoring", example_code_refactoring),
        ("Bug Fixing", example_bug_fixing),
        ("Feature Implementation", example_feature_implementation),
        ("Research Task", example_research_task),
        ("System Status", example_system_status),
        ("Complex Workflow", example_complex_workflow),
        ("Parallel Tasks", example_parallel_tasks),
    ]

    print("="*80)
    print("MULTI-AGENT FRAMEWORK EXAMPLES")
    print("="*80)

    for i, (name, func) in enumerate(examples, 1):
        print(f"\n{i}. {name}")

    print("\n" + "="*80)

    choice = input("\nSelect example to run (1-7, or 'all' for all): ").strip()

    if choice.lower() == 'all':
        for name, func in examples:
            await func()
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        await examples[int(choice) - 1][1]()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    asyncio.run(main())
