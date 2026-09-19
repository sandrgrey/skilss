from __future__ import annotations

import json

from sandr.adapters.codex import MARKER, merge_hook_config
from sandr.install import install_skills


def test_skill_install_preserves_previous_version_as_backup(tmp_path):
    source = tmp_path / "source"
    skill = source / "debugger"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("version one\n", encoding="utf-8")
    home = tmp_path / "codex"

    first = install_skills("codex", source=source, home=home)
    assert first[0]["backup"] is None

    (skill / "SKILL.md").write_text("version two\n", encoding="utf-8")
    second = install_skills("codex", source=source, home=home)

    assert (home / "skills" / "debugger" / "SKILL.md").read_text(encoding="utf-8") == "version two\n"
    backup = second[0]["backup"]
    assert backup is not None


def test_codex_hook_merge_preserves_unrelated_hooks(tmp_path):
    config = tmp_path / "hooks.json"
    config.write_text(
        json.dumps({
            "hooks": {
                "UserPromptSubmit": [
                    {"hooks": [{"type": "command", "command": "echo keep", "statusMessage": "other"}]}
                ]
            }
        }),
        encoding="utf-8",
    )

    merge_hook_config(config, "python -m sandr.cli guard-hook", event="PostToolUse")
    data = json.loads(config.read_text(encoding="utf-8"))

    assert data["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"] == "echo keep"
    handlers = data["hooks"]["PostToolUse"][0]["hooks"]
    assert handlers[0]["statusMessage"] == MARKER
