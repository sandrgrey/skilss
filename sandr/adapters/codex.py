from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sandr.core.atomic_io import atomic_write_text, make_backup

MARKER = "Sandr Dev Stack LoopGuard"


def merge_hook_config(path: Path | str, command: str, *, event: str = "PostToolUse") -> dict:
    """Merge one Sandr-owned hook without removing unrelated host configuration.

    The event is configurable because Codex hook surfaces may evolve. The installer
    defaults to PostToolUse, which is the right semantic boundary for recording
    command outcomes when the host exposes it.
    """
    target = Path(path).expanduser()
    original = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {}
    if not isinstance(original, dict):
        raise ValueError("hooks config root must be an object")
    data: dict[str, Any] = json.loads(json.dumps(original))
    hooks = data.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError("hooks must be an object")
    for groups in hooks.values():
        if not isinstance(groups, list):
            raise ValueError("every hook event must be a list")
        kept = []
        for group in groups:
            handlers = group.get("hooks", []) if isinstance(group, dict) else []
            filtered = [h for h in handlers if h.get("statusMessage") != MARKER]
            if filtered:
                clone = dict(group)
                clone["hooks"] = filtered
                kept.append(clone)
            elif not handlers:
                kept.append(group)
        groups[:] = kept
    hooks.setdefault(event, []).append({
        "hooks": [{
            "type": "command",
            "command": command,
            "statusMessage": MARKER,
            "timeout": 15,
        }]
    })
    backup = make_backup(target, label="codex-hooks")
    atomic_write_text(target, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    return {"config": str(target), "backup": str(backup) if backup else None, "event": event}


def parse_hook_payload(payload: dict) -> dict:
    """Best-effort normalization for host hook payloads without trusting arbitrary fields."""
    tool = str(payload.get("tool_name") or payload.get("tool") or payload.get("name") or "tool")
    command = str(payload.get("command") or payload.get("input") or payload.get("tool_input") or "")
    result = payload.get("result") or payload.get("tool_result") or payload.get("output") or ""
    if isinstance(result, (dict, list)):
        result = json.dumps(result, ensure_ascii=False)
    exit_code = payload.get("exit_code")
    if exit_code is None and isinstance(payload.get("result"), dict):
        exit_code = payload["result"].get("exit_code") or payload["result"].get("code")
    try:
        exit_code = int(exit_code) if exit_code is not None else None
    except (TypeError, ValueError):
        exit_code = None
    return {"operation_type": tool, "command": command, "output": str(result), "exit_code": exit_code}
