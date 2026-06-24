"""Transcript serialization to text formats (pure)."""

from __future__ import annotations

import json

from transcriber.core.transcription import Transcript


def _clock(seconds: float, *, millis_sep: str) -> str:
    if seconds < 0:
        seconds = 0.0
    total_ms = round(seconds * 1000)
    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{millis_sep}{millis:03d}"


def to_txt(transcript: Transcript) -> str:
    """Plain text, one segment per line."""
    return "\n".join(segment.text for segment in transcript.segments)


def to_md(transcript: Transcript) -> str:
    """Markdown with a heading and the text as paragraphs."""
    lines = ["# Transcript", ""]
    lines.extend(segment.text for segment in transcript.segments)
    return "\n".join(lines)


def to_srt(transcript: Transcript) -> str:
    """SubRip (.srt) cues."""
    blocks: list[str] = []
    for index, segment in enumerate(transcript.segments, start=1):
        start = _clock(segment.start, millis_sep=",")
        end = _clock(segment.end, millis_sep=",")
        blocks.append(f"{index}\n{start} --> {end}\n{segment.text}\n")
    return "\n".join(blocks)


def to_vtt(transcript: Transcript) -> str:
    """WebVTT (.vtt) cues."""
    blocks: list[str] = ["WEBVTT", ""]
    for segment in transcript.segments:
        start = _clock(segment.start, millis_sep=".")
        end = _clock(segment.end, millis_sep=".")
        blocks.append(f"{start} --> {end}\n{segment.text}\n")
    return "\n".join(blocks)


def to_json(transcript: Transcript) -> str:
    """JSON with language and timed segments."""
    payload = {
        "language": transcript.language,
        "segments": [
            {"start": segment.start, "end": segment.end, "text": segment.text}
            for segment in transcript.segments
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)
