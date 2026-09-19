from __future__ import annotations

from sandr.core.events import OperationEvent


def event_from_dict(data: dict) -> OperationEvent:
    return OperationEvent(
        operation_type=str(data.get("operation_type", "tool")),
        command=str(data.get("command", "")),
        exit_code=data.get("exit_code"),
        output=str(data.get("output", "")),
        affected_files=tuple(data.get("affected_files", ()) or ()),
    )
