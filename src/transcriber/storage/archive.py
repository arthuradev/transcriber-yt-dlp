"""File-backed download archive (implements DownloadArchive).

Stores one key per line in a user-local text file. Keys are cached in memory and
appended on ``add``. The archive contains only ``extractor:id`` keys, no URLs or
secrets.
"""

from __future__ import annotations

import os
from pathlib import Path


def default_archive_path() -> Path:
    """Return the default user-local archive path."""
    appdata = os.environ.get("APPDATA")
    root = Path(appdata) if appdata else Path.home() / ".config"
    return root / "Transcriber" / "archive.txt"


class FileDownloadArchive:
    """Text-file-backed set of downloaded keys."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._keys: set[str] = set()
        if path.is_file():
            for line in path.read_text(encoding="utf-8").splitlines():
                key = line.strip()
                if key:
                    self._keys.add(key)

    def contains(self, key: str) -> bool:
        return key in self._keys

    def add(self, key: str) -> None:
        if key in self._keys:
            return
        self._keys.add(key)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(f"{key}\n")
