from __future__ import annotations

from pathlib import Path

from .parser import parse_markdown, sha256_file
from .schema import connect, ensure_schema

SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".sandr-backups"}


def _scan(root: Path) -> dict[str, tuple[Path, int, int]]:
    out: dict[str, tuple[Path, int, int]] = {}
    if not root.exists():
        return out
    for path in root.rglob("*.md"):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        st = path.stat()
        out[str(rel).replace("\\", "/")] = (path, st.st_mtime_ns, st.st_size)
    return out


def update_index(knowledge_dir: Path | str, db_path: Path | str, *, rebuild: bool = False, tokenizer: str = "unicode61") -> dict:
    root = Path(knowledge_dir).expanduser().resolve()
    db = Path(db_path).expanduser()
    conn = connect(db)
    try:
        if rebuild:
            conn.execute("DROP TABLE IF EXISTS documents_fts")
            conn.execute("DROP TABLE IF EXISTS documents")
        ensure_schema(conn, tokenizer)
        disk = _scan(root)
        current = {
            row["path"]: (row["id"], row["mtime_ns"], row["size"], row["sha256"])
            for row in conn.execute("SELECT id,path,mtime_ns,size,sha256 FROM documents")
        }
        changed = 0
        skipped = 0
        removed = 0
        for rel, (path, mtime_ns, size) in disk.items():
            old = current.get(rel)
            if old and old[1] == mtime_ns and old[2] == size:
                skipped += 1
                continue
            digest = sha256_file(path)
            if old and old[3] == digest:
                conn.execute("UPDATE documents SET mtime_ns=?,size=? WHERE id=?", (mtime_ns, size, old[0]))
                skipped += 1
                continue
            parsed = parse_markdown(path, root)
            if old:
                doc_id = old[0]
                conn.execute(
                    "UPDATE documents SET kind=?,title=?,summary=?,tags=?,body=?,mtime_ns=?,size=?,sha256=? WHERE id=?",
                    (parsed["kind"], parsed["title"], parsed["summary"], parsed["tags"], parsed["body"], mtime_ns, size, digest, doc_id),
                )
                conn.execute("DELETE FROM documents_fts WHERE document_id=?", (doc_id,))
            else:
                cur = conn.execute(
                    "INSERT INTO documents(path,kind,title,summary,tags,body,mtime_ns,size,sha256) VALUES(?,?,?,?,?,?,?,?,?)",
                    (parsed["path"], parsed["kind"], parsed["title"], parsed["summary"], parsed["tags"], parsed["body"], mtime_ns, size, digest),
                )
                doc_id = int(cur.lastrowid)
            conn.execute(
                "INSERT INTO documents_fts(title,summary,tags,body,path,document_id) VALUES(?,?,?,?,?,?)",
                (parsed["title"], parsed["summary"], parsed["tags"], parsed["body"], parsed["path"], doc_id),
            )
            changed += 1
        for rel, (doc_id, *_rest) in current.items():
            if rel not in disk:
                conn.execute("DELETE FROM documents_fts WHERE document_id=?", (doc_id,))
                conn.execute("DELETE FROM documents WHERE id=?", (doc_id,))
                removed += 1
        conn.commit()
        total = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        return {"changed": changed, "skipped": skipped, "removed": removed, "total": total, "db": str(db)}
    finally:
        conn.close()
