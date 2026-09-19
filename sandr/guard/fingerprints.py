from __future__ import annotations

import hashlib
import re

_VOLATILE = re.compile(r"(?:0x[0-9a-f]+|\b\d{4,}\b|/[A-Za-z0-9_.\-/]+|[A-Za-z]:\\[^\s]+)", re.I)
_SPACE = re.compile(r"\s+")


def command_family(command: str) -> str:
    parts = command.strip().split()
    if not parts:
        return ""
    head = parts[0].lower()
    if head in {"python", "python3", "py"} and len(parts) > 1:
        return f"python {parts[1]}"
    if head in {"npm", "pnpm", "yarn", "pip", "pip3", "git", "pytest", "cargo", "go"} and len(parts) > 1:
        return f"{head} {parts[1].lower()}"
    return head


def normalize_error(output: str, limit: int = 1200) -> str:
    text = (output or "").strip().lower()
    text = _VOLATILE.sub("<var>", text)
    text = _SPACE.sub(" ", text)
    return text[-limit:]


def make_fingerprint(operation_type: str, command: str, exit_code: int | None, output: str) -> str:
    raw = "\n".join([
        operation_type.strip().lower(),
        command_family(command),
        str(exit_code),
        normalize_error(output),
    ])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]
