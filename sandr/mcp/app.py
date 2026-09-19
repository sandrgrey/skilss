from __future__ import annotations

from pathlib import Path

from sandr.config import expand_path, load_config
from .tools import MemoryTools


def build_server(config_path: Path | str | None = None):
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install project dependencies: pip install -e .") from exc

    cfg = load_config(config_path)
    db_path = expand_path(cfg["memory"]["db_path"])
    tools = MemoryTools(db_path)
    mcp = FastMCP("sandr-dev-stack")

    @mcp.tool()
    def search_memory(query: str, limit: int = 5) -> list[dict]:
        """Search the local Sandr Dev Stack knowledge index."""
        return tools.search_memory(query, limit)

    @mcp.tool()
    def get_memory(document_id: int) -> dict:
        """Get one complete memory document by id."""
        return tools.get_memory(document_id)

    @mcp.tool()
    def memory_status() -> dict:
        """Show local memory index status."""
        return tools.memory_status()

    return mcp


def main() -> None:
    build_server().run()


if __name__ == "__main__":
    main()
