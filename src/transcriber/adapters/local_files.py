"""Local filesystem text reader (implements TextFileReader)."""

from __future__ import annotations

from pathlib import Path


class LocalTextFileReader:
    """Reads UTF-8 text files from the local filesystem."""

    def read_text(self, path: str) -> str:
        return Path(path).read_text(encoding="utf-8")
