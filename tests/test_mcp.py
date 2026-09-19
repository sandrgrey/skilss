from __future__ import annotations

from sandr.mcp.tools import MemoryTools
from sandr.memory.index import update_index


def test_memory_tools_are_read_only_retrieval_surface(tmp_path):
    knowledge = tmp_path / "knowledge"
    knowledge.mkdir()
    (knowledge / "architecture.md").write_text(
        "# Architecture\n\nSQLite FTS5 is the local search cache.\n",
        encoding="utf-8",
    )
    db = tmp_path / "memory.db"
    update_index(knowledge, db, rebuild=True)

    tools = MemoryTools(db)
    hits = tools.search_memory("SQLite FTS5")

    assert hits
    full = tools.get_memory(hits[0]["id"])
    assert full["title"] == "Architecture"
    assert tools.memory_status()["documents"] == 1
