"""Persist transcripts to disk in a chosen format."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from transcriber.core.transcript_format import to_json, to_md, to_srt, to_txt, to_vtt
from transcriber.core.transcription import Transcript

_FORMATTERS: dict[str, Callable[[Transcript], str]] = {
    "txt": to_txt,
    "md": to_md,
    "srt": to_srt,
    "vtt": to_vtt,
    "json": to_json,
}
_EXTENSIONS: dict[str, str] = {
    "txt": ".txt",
    "md": ".md",
    "srt": ".srt",
    "vtt": ".vtt",
    "json": ".json",
}


def save_transcript(transcript: Transcript, *, output_dir: str, stem: str, fmt: str) -> Path:
    """Write ``transcript`` to ``output_dir/stem.<ext>`` and return the path."""
    formatter = _FORMATTERS.get(fmt, to_txt)
    extension = _EXTENSIONS.get(fmt, ".txt")
    path = Path(output_dir) / f"{stem}{extension}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(formatter(transcript), encoding="utf-8")
    return path
