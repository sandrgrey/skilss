from __future__ import annotations

import json
from pathlib import Path

from sandr.core.atomic_io import atomic_write_text


def load_state(path: Path | str) -> dict:
    p = Path(path).expanduser()
    if not p.exists():
        return {"last_fingerprint": None, "streak": 0, "history": []}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"last_fingerprint": None, "streak": 0, "history": []}
    if not isinstance(data, dict):
        return {"last_fingerprint": None, "streak": 0, "history": []}
    data.setdefault("last_fingerprint", None)
    data.setdefault("streak", 0)
    data.setdefault("history", [])
    return data


def save_state(path: Path | str, state: dict) -> None:
    p = Path(path).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(p, json.dumps(state, ensure_ascii=False, indent=2) + "\n")
