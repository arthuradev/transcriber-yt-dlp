"""Tests for transcript persistence."""

from __future__ import annotations

from pathlib import Path

from transcriber.core.transcription import Transcript, TranscriptSegment
from transcriber.storage.transcript_store import save_transcript


def _transcript() -> Transcript:
    return Transcript("en", (TranscriptSegment(0.0, 1.0, "Hello"),))


def test_save_txt_creates_parents(tmp_path: Path) -> None:
    path = save_transcript(_transcript(), output_dir=str(tmp_path / "sub"), stem="clip", fmt="txt")
    assert path.name == "clip.txt"
    assert path.read_text(encoding="utf-8") == "Hello"


def test_save_srt(tmp_path: Path) -> None:
    path = save_transcript(_transcript(), output_dir=str(tmp_path), stem="clip", fmt="srt")
    assert path.suffix == ".srt"
    assert "Hello" in path.read_text(encoding="utf-8")


def test_unknown_format_defaults_to_txt(tmp_path: Path) -> None:
    path = save_transcript(_transcript(), output_dir=str(tmp_path), stem="c", fmt="weird")
    assert path.suffix == ".txt"
