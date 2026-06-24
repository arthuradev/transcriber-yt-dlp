"""Tests for progress mapping and output-template helpers."""

from __future__ import annotations

from typing import Any

from transcriber.adapters.yt_dlp_mapping import map_progress, output_template
from transcriber.core.download import DownloadStatus


def test_map_progress_downloading() -> None:
    hook: dict[str, Any] = {
        "status": "downloading",
        "downloaded_bytes": 500,
        "total_bytes": 1000,
        "speed": 123.0,
        "eta": 5,
        "filename": "f.mp4",
    }
    progress = map_progress(hook)
    assert progress.status is DownloadStatus.DOWNLOADING
    assert progress.downloaded_bytes == 500
    assert progress.total_bytes == 1000
    assert progress.fraction == 0.5
    assert progress.speed == 123.0
    assert progress.eta_seconds == 5
    assert progress.filename == "f.mp4"


def test_map_progress_uses_total_estimate() -> None:
    hook: dict[str, Any] = {
        "status": "downloading",
        "downloaded_bytes": 250,
        "total_bytes_estimate": 1000,
    }
    progress = map_progress(hook)
    assert progress.total_bytes == 1000
    assert progress.fraction == 0.25


def test_map_progress_finished() -> None:
    progress = map_progress({"status": "finished", "downloaded_bytes": 1000, "total_bytes": 1000})
    assert progress.status is DownloadStatus.FINISHED


def test_map_progress_unknown_total() -> None:
    progress = map_progress({"status": "downloading", "downloaded_bytes": 10})
    assert progress.total_bytes is None
    assert progress.fraction is None


def test_output_template_replaces_extension() -> None:
    assert output_template("out/My Video [abc].mp4") == "out/My Video [abc].%(ext)s"
    assert output_template("out.v2/clip.webm") == "out.v2/clip.%(ext)s"
