from __future__ import annotations

from pathlib import Path

from sandr.memory.search import get_document, search, status


class MemoryTools:
    def __init__(self, db_path: Path | str):
        self.db_path = Path(db_path).expanduser()

    def search_memory(self, query: str, limit: int = 5) -> list[dict]:
        """Search project memory and return compact snippets."""
        return search(self.db_path, query, limit)

    def get_memory(self, document_id: int) -> dict:
        """Return the full memory document for an id returned by search_memory."""
        return get_document(self.db_path, document_id)

    def memory_status(self) -> dict:
        """Return index existence and document count."""
        return status(self.db_path)
