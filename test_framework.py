#!/usr/bin/env python3
"""
Basic tests for the Multi-Agent Framework
"""
import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agents import (
    AgentRegistry,
    TaskRouter,
    TmuxManager,
    SkillsSystem,
    Orchestrator
)


def test_agent_registry():
    """Test agent registry functionality"""
    print("Testing Agent Registry...")

    registry = AgentRegistry("agents/test_registry.json")

    # Check default agents loaded
    assert len(registry.agents) > 0, "No agents loaded"
    print(f"  ✅ Loaded {len(registry.agents)} agents")

    # Test finding agents
    code_agents = registry.find_agents_by_capability("python")
    assert len(code_agents) > 0, "No Python agents found"
    print(f"  ✅ Found {len(code_agents)} Python-capable agents")

    # Test best agent selection
    best = registry.find_best_agent(["code_review", "python"])
    assert best is not None, "Could not find best agent"
    print(f"  ✅ Best agent for code review: {best.name}")

    # Cleanup
    Path("agents/test_registry.json").unlink(missing_ok=True)

    print("  ✅ Agent Registry tests passed\n")


def test_task_router():
    """Test task routing functionality"""
    print("Testing Task Router...")

    registry = AgentRegistry("agents/test_registry.json")
    router = TaskRouter(registry)

    # Test task analysis
    analysis = router.analyze_task(
        "Refactor the Python authentication module to use JWT tokens"
    )

    # Verify task analysis works
    print(f"  ✅ Task type identified: {analysis.task_type}")
    assert analysis.task_type is not None, "Task type is None"

    # Verify capability detection
    assert len(analysis.required_capabilities) > 0 or "python" in [c.lower() for c in analysis.keywords], "Failed to detect capabilities or keywords"
    print(f"  ✅ Capabilities/Keywords detected: {', '.join(analysis.required_capabilities) if analysis.required_capabilities else ', '.join(analysis.keywords[:3])}")

    # Test agent selection
    assignments = router.select_agents(
        "Fix bugs in the payment processing system"
    )

    assert len(assignments) > 0, "No agents selected"
    print(f"  ✅ Selected {len(assignments)} agents")

    # Cleanup
    Path("agents/test_registry.json").unlink(missing_ok=True)

    print("  ✅ Task Router tests passed\n")


def test_tmux_manager():
    """Test TMUX manager functionality"""
    print("Testing TMUX Manager...")

    manager = TmuxManager("workspace/test")

    # Check TMUX installed
    assert manager.check_tmux_installed(), "TMUX not installed"
    print("  ✅ TMUX is installed")

    # Test session creation
    session_id = manager.create_session("test_agent", "task123")
    assert manager.session_exists(session_id), "Session not created"
    print(f"  ✅ Created session: {session_id}")

    # Test session info
    info = manager.get_session_info(session_id)
    assert info is not None, "Session info not found"
    assert info.agent_name == "test_agent", "Wrong agent name"
    print(f"  ✅ Session info retrieved")

    # Test cleanup
    manager.kill_session(session_id)
    print(f"  ✅ Session terminated")

    # Cleanup
    Path("workspace/test/sessions.json").unlink(missing_ok=True)

    print("  ✅ TMUX Manager tests passed\n")


def test_skills_system():
    """Test skills/learning system"""
    print("Testing Skills System...")

    from agents.skills_system import TaskOutcome
    from datetime import datetime

    skills = SkillsSystem("agents/test_skills.json")

    # Test recording outcome
    outcome = TaskOutcome(
        task_id="test123",
        agent_name="code_writer",
        task_description="Test task",
        task_type="implementation",
        success=True,
        execution_time=10.5,
        tokens_used=1000,
        cost=0.05,
        error_message=None,
        prompt_used="Test prompt",
        timestamp=datetime.now().isoformat()
    )

    skills.record_outcome(outcome)
    print("  ✅ Recorded task outcome")

    # Test performance retrieval
    perf = skills.get_agent_performance("code_writer")
    assert perf['total_tasks'] == 1, "Task not recorded"
    print(f"  ✅ Performance tracked: {perf['total_tasks']} tasks")

    # Test suggestions
    suggestions = skills.suggest_improvements("code_writer")
    assert len(suggestions) > 0, "No suggestions generated"
    print(f"  ✅ Generated {len(suggestions)} suggestions")

    # Cleanup
    Path("agents/test_skills.json").unlink(missing_ok=True)

    print("  ✅ Skills System tests passed\n")


async def test_orchestrator_basic():
    """Test basic orchestrator functionality"""
    print("Testing Orchestrator (basic)...")

    orchestrator = Orchestrator(
        workspace_dir="workspace/test",
        registry_path="agents/test_registry.json",
        skills_path="agents/test_skills.json"
    )

    # Test system status
    status = orchestrator.get_system_status()
    assert 'registry' in status, "Missing registry status"
    assert 'tmux' in status, "Missing tmux status"
    print("  ✅ System status retrieved")

    # Test agent listing
    agents = orchestrator.registry.get_all_agents()
    assert len(agents) > 0, "No agents available"
    print(f"  ✅ {len(agents)} agents available")

    # Cleanup
    Path("agents/test_registry.json").unlink(missing_ok=True)
    Path("agents/test_skills.json").unlink(missing_ok=True)

    print("  ✅ Orchestrator basic tests passed\n")


def run_all_tests():
    """Run all tests"""
    print("="*80)
    print("MULTI-AGENT FRAMEWORK TEST SUITE")
    print("="*80)
    print()

    tests = [
        ("Agent Registry", test_agent_registry),
        ("Task Router", test_task_router),
        ("TMUX Manager", test_tmux_manager),
        ("Skills System", test_skills_system),
        ("Orchestrator", lambda: asyncio.run(test_orchestrator_basic()))
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"  ❌ {name} test failed: {e}\n")
            failed += 1

    print("="*80)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*80)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
