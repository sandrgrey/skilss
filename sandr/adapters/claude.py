from __future__ import annotations

from pathlib import Path


def settings_path(home: Path | None = None) -> Path:
    return (home or Path.home() / ".claude") / "settings.json"
