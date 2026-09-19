from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OperationEvent:
    operation_type: str
    command: str
    exit_code: int | None
    output: str
    affected_files: tuple[str, ...] = ()
