from __future__ import annotations

from sandr.project import ingest_project, init_project


def test_project_init_is_idempotent_and_ingest_accepts_text_notes(tmp_path):
    knowledge = tmp_path / "knowledge"

    first = init_project(knowledge, "demo-project", "Demo Project")
    second = init_project(knowledge, "demo-project", "Demo Project")

    assert len(first["created"]) == 3
    assert second["created"] == []

    source = tmp_path / "notes"
    source.mkdir()
    (source / "decision.md").write_text("# Decision\n\nKeep Markdown canonical.\n", encoding="utf-8")
    (source / "debug.txt").write_text("A verified incident note.", encoding="utf-8")
    (source / "ignore.bin").write_bytes(b"ignored")

    result = ingest_project(knowledge, "demo-project", source)

    assert len(result["copied"]) == 2
    assert all(path.endswith(".md") for path in result["copied"])
