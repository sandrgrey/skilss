from __future__ import annotations

import json
import shutil
import sys
import time
from pathlib import Path

from sandr.adapters.codex import merge_hook_config
from sandr.core.atomic_io import atomic_write_text
from sandr.core.paths import claude_home, codex_home

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = PACKAGE_ROOT / "skills"


def _backup_dir(path: Path) -> Path:
    stamp = time.strftime("%Y%m%d-%H%M%S")
    return path.with_name(path.name + f".backup-{stamp}")


def install_skills(host: str, *, source: Path | None = None, home: Path | None = None, selected: str | None = None) -> list[dict]:
    source = source or SKILLS_ROOT
    if host == "codex":
        root = (home or codex_home()) / "skills"
    elif host == "claude":
        root = (home or claude_home()) / "skills"
    else:
        raise ValueError(f"unsupported host: {host}")
    root.mkdir(parents=True, exist_ok=True)
    results = []
    skills = sorted(p for p in source.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
    if selected is not None:
        skills = [p for p in skills if p.name == selected]
        if not skills:
            raise ValueError(f"unknown skill: {selected}")
    for skill in skills:
        target = root / skill.name
        backup = None
        if target.exists():
            backup = _backup_dir(target)
            shutil.move(target, backup)
        shutil.copytree(skill, target)
        results.append({"skill": skill.name, "target": str(target), "backup": str(backup) if backup else None})
    return results


def install_config(config_source: Path, config_target: Path) -> dict:
    config_target.parent.mkdir(parents=True, exist_ok=True)
    if config_target.exists():
        return {"target": str(config_target), "created": False}
    atomic_write_text(config_target, config_source.read_text(encoding="utf-8"))
    return {"target": str(config_target), "created": True}


def install_codex_guard(*, codex_root: Path | None = None, python_executable: str | None = None, event: str = "PostToolUse") -> dict:
    root = codex_root or codex_home()
    py = python_executable or sys.executable
    command = f'"{py}" -m sandr.cli guard-hook'
    return merge_hook_config(root / "hooks.json", command, event=event)


def export_install_report(path: Path, report: dict) -> None:
    atomic_write_text(path, json.dumps(report, ensure_ascii=False, indent=2) + "\n")
