# Sandr Dev Stack

A local, lightweight development layer for Codex/Claude-style coding agents.

It combines five ideas in one small Python project:

- portable agent **skills**;
- durable **Markdown project memory** indexed with SQLite FTS5;
- read-only **MCP tools** for memory retrieval;
- **LoopGuard** for detecting repeated failing strategies;
- **transaction-safe configuration writes** with exact backups and rollback.

The implementation is clean-room. It is inspired by architectural patterns observed in public projects by `howdeploy`, but does not copy code from repositories without a clear license.

## Requirements

- Python 3.11+
- SQLite compiled with FTS5

Install for development:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"
```

## First run

```bash
sandr doctor
sandr memory build
sandr memory search "authentication"
```

Install portable skills into Codex:

```bash
sandr install --host codex
```

The LoopGuard Codex hook is deliberately **opt-in/experimental** because host hook schemas can change:

```bash
sandr install --host codex --guard
```

If your Codex version uses a different post-tool event name, set it explicitly:

```bash
sandr install --host codex --guard --hook-event PostToolUse
```

## Memory layout

```text
knowledge/
├── raw/
├── projects/
├── decisions/
├── architecture/
├── solutions/
└── incidents/
```

Markdown is the source of truth. The SQLite database is disposable and can always be rebuilt.

```bash
sandr memory build
sandr memory update
sandr memory status
sandr memory search "postgresql decision"
sandr memory get 12
```

## LoopGuard

Manual recording is stable and host-independent:

```bash
sandr guard record \
  --type shell \
  --command "npm install" \
  --exit-code 1 \
  --output "ERESOLVE unable to resolve dependency tree"
```

Default policy:

- same failure x2 -> L1 warning;
- x3 -> L2 strategy reset;
- x4 -> L3 independent-audit boundary.

A successful operation resets the streak.

## MCP

Run the read-only MCP server:

```bash
sandr-mcp
```

Tools:

- `search_memory(query, limit=5)`
- `get_memory(document_id)`
- `memory_status()`

The server exposes the SQLite index, not arbitrary filesystem access.

## Safe file transactions

```python
from sandr.core.transactions import FileTransaction

with FileTransaction("config.json", label="change-auth", validator=validate) as tx:
    tx.stage_text(new_config)
    tx.commit()
```

The transaction keeps the exact backup for that operation and restores the original on validation failure.

## Tests

```bash
pytest
```

## Status

This is an MVP. Memory, safe transactions, skill installation, doctor checks, MCP access, and host-independent LoopGuard recording are implemented. Automatic Codex post-tool interception is intentionally marked experimental until verified against the exact installed Codex hook schema.
