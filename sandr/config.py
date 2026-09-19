from __future__ import annotations

import os
from copy import deepcopy
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None

DEFAULTS = {
    "general": {"language": "ru"},
    "memory": {
        "knowledge_dir": "./knowledge",
        "db_path": "~/.cache/sandr-dev-stack/memory.db",
        "tokenizer": "unicode61",
    },
    "guard": {
        "enabled": True,
        "warning_after": 2,
        "reset_after": 3,
        "audit_after": 4,
        "state_path": "~/.local/state/sandr-dev-stack/guard.json",
        "auditor": "none",
    },
    "hosts": {"install_codex": True, "install_claude": False},
}


def _merge(base: dict, extra: dict) -> dict:
    out = deepcopy(base)
    for key, value in extra.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _merge(out[key], value)
        else:
            out[key] = value
    return out


def default_config_path() -> Path:
    env = os.environ.get("SANDR_CONFIG")
    if env:
        return Path(env).expanduser()
    return Path.home() / ".config" / "sandr-dev-stack" / "config.toml"


def load_config(path: Path | str | None = None) -> dict:
    cfg_path = Path(path).expanduser() if path else default_config_path()
    if not cfg_path.exists():
        return deepcopy(DEFAULTS)
    if tomllib is None:
        raise RuntimeError("Python 3.11+ with tomllib is required")
    with cfg_path.open("rb") as handle:
        parsed = tomllib.load(handle)
    return _merge(DEFAULTS, parsed)


def expand_path(value: str, *, base: Path | None = None) -> Path:
    p = Path(value).expanduser()
    if not p.is_absolute() and base is not None:
        p = base / p
    return p.resolve()
