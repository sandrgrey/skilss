from __future__ import annotations

import hashlib
import re
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

_FRONT = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
_HEAD = re.compile(r"^#{1,6}\s+(.*)$", re.MULTILINE)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_markdown(path: Path, root: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    body = text
    tags: list[str] = []
    summary = ""
    match = _FRONT.match(text)
    if match:
        body = text[match.end():]
        if yaml is not None:
            try:
                fm = yaml.safe_load(match.group(1)) or {}
            except Exception:
                fm = {}
            if isinstance(fm, dict):
                raw_tags = fm.get("tags", [])
                if isinstance(raw_tags, str):
                    tags = [raw_tags]
                elif isinstance(raw_tags, list):
                    tags = [str(x) for x in raw_tags if x]
                summary = str(fm.get("summary", "") or "")
    headings = _HEAD.findall(body)
    title = path.stem
    if headings:
        title = headings[0].strip() or title
    if not summary:
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip() and not p.lstrip().startswith("#")]
        summary = (paragraphs[0] if paragraphs else "")[:280]
    rel = path.relative_to(root)
    kind = rel.parts[0] if len(rel.parts) > 1 else "root"
    return {
        "path": str(rel).replace("\\", "/"),
        "kind": kind,
        "title": title,
        "summary": summary,
        "tags": " ".join(tags),
        "body": body,
    }
