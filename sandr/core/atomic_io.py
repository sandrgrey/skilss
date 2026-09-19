from __future__ import annotations

import os
import shutil
import tempfile
import time
from pathlib import Path


def _sync_dir(path: Path) -> None:
    if os.name == "nt":
        return
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_write_bytes(path: Path | str, data: bytes, mode: int | None = None) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=target.name + ".", dir=target.parent)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if mode is not None:
            os.chmod(tmp, mode)
        os.replace(tmp, target)
        _sync_dir(target.parent)
    finally:
        try:
            tmp.unlink(missing_ok=True)
        except OSError:
            pass


def atomic_write_text(path: Path | str, text: str, mode: int | None = None) -> None:
    atomic_write_bytes(path, text.encode("utf-8"), mode=mode)


def make_backup(path: Path | str, *, label: str = "backup", backup_dir: Path | None = None) -> Path | None:
    src = Path(path)
    if not src.exists():
        return None
    root = backup_dir or src.parent / ".sandr-backups"
    root.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    candidate = root / f"{src.name}.{stamp}.{label}.bak"
    counter = 1
    while candidate.exists():
        candidate = root / f"{src.name}.{stamp}.{label}.{counter}.bak"
        counter += 1
    shutil.copy2(src, candidate)
    return candidate
