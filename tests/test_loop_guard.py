from __future__ import annotations

from sandr.core.events import OperationEvent
from sandr.guard.loop_guard import LoopGuard


def test_loop_guard_escalates_repeated_failure(tmp_path):
    guard = LoopGuard(tmp_path / "guard.json", warning_after=2, reset_after=3, audit_after=4)
    event = OperationEvent("shell", "npm install", 1, "ERESOLVE dependency tree")

    levels = [guard.record(event).level for _ in range(4)]

    assert levels == [0, 1, 2, 3]


def test_loop_guard_success_resets_streak(tmp_path):
    guard = LoopGuard(tmp_path / "guard.json")
    failed = OperationEvent("shell", "pytest", 1, "AssertionError")
    ok = OperationEvent("shell", "pytest", 0, "9 passed")

    guard.record(failed)
    guard.record(failed)
    decision = guard.record(ok)

    assert decision.level == 0
    assert decision.streak == 0
