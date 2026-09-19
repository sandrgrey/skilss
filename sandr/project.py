from __future__ import annotations

import re
import shutil
from datetime import date
from pathlib import Path

from sandr.core.atomic_io import atomic_write_text

_SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def validate_slug(slug: str) -> str:
    if not _SLUG.fullmatch(slug):
        raise ValueError("project slug must be lowercase kebab-case")
    return slug


def init_project(knowledge_dir: Path | str, slug: str, title: str | None = None) -> dict:
    slug = validate_slug(slug)
    root = Path(knowledge_dir) / "projects" / slug
    root.mkdir(parents=True, exist_ok=True)
    title = title or slug.replace("-", " ").title()
    files = {
        "overview.md": f"---\ntags: [project, overview]\nsummary: Project overview for {title}\n---\n# {title}\n\n## Purpose\n\nDescribe the project purpose here.\n\n## Current state\n\nInitial project memory scaffold.\n",
        "architecture.md": f"---\ntags: [project, architecture]\nsummary: Architecture notes for {title}\n---\n# {title} Architecture\n\n## Components\n\n- TODO\n\n## Data flow\n\n- TODO\n",
        "conventions.md": f"---\ntags: [project, conventions]\nsummary: Stable conventions for {title}\n---\n# {title} Conventions\n\nRecord verified, durable conventions only.\n",
    }
    created = []
    for name, body in files.items():
        path = root / name
        if not path.exists():
            atomic_write_text(path, body)
            created.append(str(path))
    return {"project": slug, "root": str(root), "created": created}


def ingest_project(knowledge_dir: Path | str, slug: str, source: Path | str) -> dict:
    slug = validate_slug(slug)
    src = Path(source).expanduser().resolve()
    if not src.exists():
        raise FileNotFoundError(src)
    target = Path(knowledge_dir) / "raw" / "projects" / slug
    target.mkdir(parents=True, exist_ok=True)
    candidates = [src] if src.is_file() else sorted(p for p in src.rglob("*") if p.is_file())
    copied = []
    for path in candidates:
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        safe = re.sub(r"[^A-Za-z0-9._-]+", "-", path.name).strip("-") or "input.md"
        if not safe.lower().endswith(".md"):
            safe = safe.rsplit(".", 1)[0] + ".md"
        dest = target / f"{date.today().isoformat()}-{safe}"
        n = 1
        while dest.exists():
            dest = target / f"{date.today().isoformat()}-{n}-{safe}"
            n += 1
        if path.suffix.lower() == ".md":
            shutil.copy2(path, dest)
        else:
            body = path.read_text(encoding="utf-8", errors="replace")
            atomic_write_text(dest, f"# Imported: {path.name}\n\n{body}\n")
        copied.append(str(dest))
    return {"project": slug, "source": str(src), "copied": copied}
