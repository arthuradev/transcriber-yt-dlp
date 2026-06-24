"""Tests for the download archive."""

from __future__ import annotations

from pathlib import Path

from transcriber.core.archive import archive_key
from transcriber.storage.archive import FileDownloadArchive, default_archive_path


def test_archive_key() -> None:
    assert archive_key("Youtube", "abc") == "Youtube:abc"


def test_default_archive_path_is_under_transcriber() -> None:
    path = default_archive_path()
    assert path.name == "archive.txt"
    assert path.parent.name == "Transcriber"


def test_archive_round_trip_and_reload(tmp_path: Path) -> None:
    path = tmp_path / "sub" / "archive.txt"
    archive = FileDownloadArchive(path)
    assert not archive.contains("k1")
    archive.add("k1")
    assert archive.contains("k1")
    assert path.is_file()

    reloaded = FileDownloadArchive(path)
    assert reloaded.contains("k1")


def test_archive_add_is_idempotent(tmp_path: Path) -> None:
    path = tmp_path / "archive.txt"
    archive = FileDownloadArchive(path)
    archive.add("key")
    archive.add("key")
    assert path.read_text(encoding="utf-8").splitlines().count("key") == 1
