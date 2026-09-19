from __future__ import annotations

from sandr.memory.index import update_index
from sandr.memory.search import get_document, search, status


def test_memory_build_search_and_get(tmp_path):
    knowledge = tmp_path / "knowledge"
    knowledge.mkdir()
    (knowledge / "auth.md").write_text(
        "---\ntags: [auth, jwt]\nsummary: Authentication decision\n---\n"
        "# Authentication\n\nUse JWT refresh tokens for the API.\n",
        encoding="utf-8",
    )
    db = tmp_path / "memory.db"

    result = update_index(knowledge, db, rebuild=True)

    assert result["changed"] == 1
    assert status(db)["documents"] == 1
    hits = search(db, "authentication jwt")
    assert hits
    doc = get_document(db, hits[0]["id"])
    assert doc["path"] == "auth.md"
    assert "refresh tokens" in doc["body"]


def test_memory_incremental_update_skips_unchanged_files(tmp_path):
    knowledge = tmp_path / "knowledge"
    knowledge.mkdir()
    note = knowledge / "note.md"
    note.write_text("# Deploy\n\nAtomic rollback strategy.\n", encoding="utf-8")
    db = tmp_path / "memory.db"

    update_index(knowledge, db, rebuild=True)
    second = update_index(knowledge, db)

    assert second["changed"] == 0
    assert second["skipped"] == 1
    assert second["total"] == 1
