"""Port for reading text files (e.g. batch URL lists)."""

from __future__ import annotations

from typing import Protocol


class TextFileReader(Protocol):
    """Reads a local text file as a string."""

    def read_text(self, path: str) -> str:
        """Return the file's contents. Raises ``OSError`` if it cannot be read."""
        ...
