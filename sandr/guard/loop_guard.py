from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from sandr.core.events import OperationEvent
from .fingerprints import make_fingerprint
from .state import load_state, save_state


@dataclass(frozen=True)
class GuardDecision:
    level: int
    action: str
    streak: int
    fingerprint: str
    message: str


class LoopGuard:
    def __init__(self, state_path: Path | str, *, warning_after: int = 2, reset_after: int = 3, audit_after: int = 4):
        self.state_path = Path(state_path).expanduser()
        self.warning_after = warning_after
        self.reset_after = reset_after
        self.audit_after = audit_after

    def record(self, event: OperationEvent) -> GuardDecision:
        fp = make_fingerprint(event.operation_type, event.command, event.exit_code, event.output)
        state = load_state(self.state_path)
        failed = event.exit_code not in (None, 0)
        if not failed:
            streak = 0
            state["last_fingerprint"] = None
        elif state.get("last_fingerprint") == fp:
            streak = int(state.get("streak", 0)) + 1
            state["last_fingerprint"] = fp
        else:
            streak = 1
            state["last_fingerprint"] = fp
        state["streak"] = streak
        level = 0
        action = "continue"
        message = "No retry loop detected."
        if failed and streak >= self.audit_after:
            level, action = 3, "audit"
            message = "Repeated failure loop detected. Stop mutations and run an independent read-only audit."
        elif failed and streak >= self.reset_after:
            level, action = 2, "strategy-reset"
            message = "Same failure repeated. Do not retry the same strategy; form a new hypothesis first."
        elif failed and streak >= self.warning_after:
            level, action = 1, "warning"
            message = "Same failure seen twice. Re-check assumptions before another retry."
        record = {
            "time": datetime.now(timezone.utc).isoformat(),
            "fingerprint": fp,
            "streak": streak,
            "level": level,
            "action": action,
            "operation_type": event.operation_type,
            "command": event.command[:300],
            "exit_code": event.exit_code,
        }
        history = list(state.get("history", []))[-99:]
        history.append(record)
        state["history"] = history
        save_state(self.state_path, state)
        return GuardDecision(level, action, streak, fp, message)

    def reset(self) -> None:
        save_state(self.state_path, {"last_fingerprint": None, "streak": 0, "history": []})
