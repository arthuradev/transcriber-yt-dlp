"""Tests for plain-text persistence."""

from __future__ import annotations

from pathlib import Path

from transcriber.storage.text_store import save_text


def test_save_text_creates_parents(tmp_path: Path) -> None:
    path = save_text("hello", output_dir=str(tmp_path / "sub"), stem="t.clean", ext=".txt")
    assert path.name == "t.clean.txt"
    assert path.read_text(encoding="utf-8") == "hello"
