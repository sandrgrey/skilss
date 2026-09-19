---
tags: [adr, memory, sqlite, markdown]
summary: Keep Markdown as canonical memory and use SQLite FTS5 only as a rebuildable local index.
---
# ADR-0001: Markdown-first project memory

## Decision

Durable project knowledge is stored in Markdown. SQLite FTS5 is derived state and may be deleted and rebuilt at any time.

## Consequences

Knowledge stays inspectable, diffable, portable, and independent of a vector database or embedding provider. Search is lexical in the MVP; semantic embeddings may be added later as an optional secondary index.
