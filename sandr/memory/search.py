from __future__ import annotations

import re
from pathlib import Path

from .schema import connect

_TOKEN = re.compile(r"[0-9A-Za-zА-Яа-яЁё_\-]+")


def _fts(text: str) -> str | None:
    tokens = _TOKEN.findall(text or "")
    if not tokens:
        return None
    return " OR ".join(f'"{t}"' for t in tokens)


def search(db_path: Path | str, query: str, limit: int = 5) -> list[dict]:
    match = _fts(query)
    if not match:
        return []
    conn = connect(db_path, readonly=True)
    try:
        rows = conn.execute(
            """SELECT d.id,d.path,d.kind,d.title,d.summary,
            snippet(documents_fts,3,'[',']','…',18) AS snippet
            FROM documents_fts JOIN documents d ON d.id=documents_fts.document_id
            WHERE documents_fts MATCH ? ORDER BY rank LIMIT ?""",
            (match, max(1, min(int(limit), 50))),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_document(db_path: Path | str, document_id: int) -> dict:
    conn = connect(db_path, readonly=True)
    try:
        row = conn.execute("SELECT * FROM documents WHERE id=?", (int(document_id),)).fetchone()
        if row is None:
            raise KeyError(document_id)
        return dict(row)
    finally:
        conn.close()


def status(db_path: Path | str) -> dict:
    db = Path(db_path).expanduser()
    if not db.exists():
        return {"exists": False, "documents": 0, "db": str(db)}
    conn = connect(db, readonly=True)
    try:
        n = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        return {"exists": True, "documents": n, "db": str(db)}
    finally:
        conn.close()
