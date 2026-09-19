from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .atomic_io import atomic_write_bytes, make_backup

Validator = Callable[[Path], None]


@dataclass
class TransactionResult:
    target: Path
    backup: Path | None
    committed: bool


class FileTransaction:
    """Safe single-file mutation: exact backup, validate candidate, atomic replace, rollback."""

    def __init__(self, target: Path | str, *, label: str = "update", validator: Validator | None = None):
        self.target = Path(target)
        self.label = label
        self.validator = validator
        self.backup: Path | None = None
        self.original: bytes | None = None
        self._candidate: bytes | None = None
        self._committed = False

    def __enter__(self) -> "FileTransaction":
        self.original = self.target.read_bytes() if self.target.exists() else None
        self.backup = make_backup(self.target, label=self.label)
        return self

    def stage_bytes(self, data: bytes) -> None:
        self._candidate = data

    def stage_text(self, text: str) -> None:
        self.stage_bytes(text.encode("utf-8"))

    def commit(self) -> TransactionResult:
        if self._candidate is None:
            raise RuntimeError("no candidate staged")
        tmp = self.target.parent / f".{self.target.name}.sandr-candidate"
        atomic_write_bytes(tmp, self._candidate)
        try:
            if self.validator:
                self.validator(tmp)
            atomic_write_bytes(self.target, self._candidate)
            if self.validator:
                self.validator(self.target)
            self._committed = True
        except BaseException:
            self.rollback()
            raise
        finally:
            tmp.unlink(missing_ok=True)
        return TransactionResult(self.target, self.backup, True)

    def rollback(self) -> None:
        if self.original is None:
            self.target.unlink(missing_ok=True)
        else:
            atomic_write_bytes(self.target, self.original)
        self._committed = False

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc is not None and not self._committed:
            self.rollback()
        return False
