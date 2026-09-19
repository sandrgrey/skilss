from __future__ import annotations

import sqlite3
from pathlib import Path


def connect(path: Path | str, *, readonly: bool = False) -> sqlite3.Connection:
    db = Path(path).expanduser()
    if readonly:
        conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    else:
        db.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(db)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=5000")
    conn.row_factory = sqlite3.Row
    return conn


def ensure_schema(conn: sqlite3.Connection, tokenizer: str = "unicode61") -> None:
    tok = "unicode61 remove_diacritics 2" if tokenizer != "trigram" else "trigram"
    conn.execute(
        """CREATE TABLE IF NOT EXISTS documents(
        id INTEGER PRIMARY KEY,
        path TEXT UNIQUE NOT NULL,
        kind TEXT NOT NULL,
        title TEXT NOT NULL,
        summary TEXT NOT NULL,
        tags TEXT NOT NULL,
        body TEXT NOT NULL,
        mtime_ns INTEGER NOT NULL,
        size INTEGER NOT NULL,
        sha256 TEXT NOT NULL
        )"""
    )
    conn.execute(
        f"""CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
        title, summary, tags, body, path UNINDEXED, document_id UNINDEXED,
        tokenize=\"{tok}\", prefix='2 3'
        )"""
    )
    conn.commit()
