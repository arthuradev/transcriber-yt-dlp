"""Tests for transcript serialization."""

from __future__ import annotations

import json

from transcriber.core.transcript_format import to_json, to_md, to_srt, to_txt, to_vtt
from transcriber.core.transcription import Transcript, TranscriptSegment


def _transcript() -> Transcript:
    return Transcript(
        "en",
        (TranscriptSegment(0.0, 1.5, "Hello"), TranscriptSegment(1.5, 3.25, "World")),
    )


def test_to_txt() -> None:
    assert to_txt(_transcript()) == "Hello\nWorld"


def test_to_md() -> None:
    output = to_md(_transcript())
    assert output.startswith("# Transcript")
    assert "Hello" in output
    assert "World" in output


def test_to_srt() -> None:
    output = to_srt(_transcript())
    assert "1\n00:00:00,000 --> 00:00:01,500\nHello" in output
    assert "2\n00:00:01,500 --> 00:00:03,250\nWorld" in output


def test_to_vtt() -> None:
    output = to_vtt(_transcript())
    assert output.startswith("WEBVTT")
    assert "00:00:00.000 --> 00:00:01.500" in output


def test_to_json() -> None:
    data = json.loads(to_json(_transcript()))
    assert data["language"] == "en"
    assert len(data["segments"]) == 2
    assert data["segments"][0]["text"] == "Hello"
