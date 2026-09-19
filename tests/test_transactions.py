from __future__ import annotations

import pytest

from sandr.core.transactions import FileTransaction


def test_transaction_commits_with_exact_backup(tmp_path):
    target = tmp_path / "config.txt"
    target.write_text("old\n", encoding="utf-8")

    def validate(path):
        assert path.read_text(encoding="utf-8") == "new\n"

    with FileTransaction(target, label="test", validator=validate) as tx:
        tx.stage_text("new\n")
        result = tx.commit()

    assert target.read_text(encoding="utf-8") == "new\n"
    assert result.committed is True
    assert result.backup is not None
    assert result.backup.read_text(encoding="utf-8") == "old\n"


def test_transaction_rolls_back_on_validation_failure(tmp_path):
    target = tmp_path / "config.txt"
    target.write_text("old\n", encoding="utf-8")

    def validate(path):
        if path.read_text(encoding="utf-8") == "bad\n":
            raise ValueError("invalid config")

    with pytest.raises(ValueError):
        with FileTransaction(target, label="test", validator=validate) as tx:
            tx.stage_text("bad\n")
            tx.commit()

    assert target.read_text(encoding="utf-8") == "old\n"
