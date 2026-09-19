from __future__ import annotations

import importlib.util
import shutil
import sqlite3
import sys
from pathlib import Path

from sandr.config import expand_path, load_config
from sandr.core.paths import codex_home
from sandr.memory.search import status


def run_checks(config_path: Path | str | None = None) -> list[dict]:
    cfg = load_config(config_path)
    checks = []

    def add(name: str, ok: bool, detail: str, severity: str = "error") -> None:
        checks.append({"name": name, "ok": ok, "detail": detail, "severity": severity})

    add("Python", sys.version_info >= (3, 11), sys.version.split()[0])
    try:
        c = sqlite3.connect(":memory:")
        c.execute("CREATE VIRTUAL TABLE t USING fts5(x)")
        c.close()
        add("SQLite FTS5", True, sqlite3.sqlite_version)
    except sqlite3.OperationalError as exc:
        add("SQLite FTS5", False, str(exc))
    add("MCP package", importlib.util.find_spec("mcp") is not None, "installed" if importlib.util.find_spec("mcp") else "missing", "warn")
    add("Codex CLI", shutil.which("codex") is not None, shutil.which("codex") or "not found", "warn")
    hooks = codex_home() / "hooks.json"
    add("Codex hooks", hooks.exists(), str(hooks), "warn")
    db = expand_path(cfg["memory"]["db_path"])
    st = status(db)
    add("Memory index", st["exists"], f"{st['documents']} documents @ {st['db']}", "warn")
    knowledge = expand_path(cfg["memory"]["knowledge_dir"], base=Path.cwd())
    add("Knowledge directory", knowledge.exists(), str(knowledge), "warn")
    return checks
