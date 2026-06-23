"""Tests for the media probe service."""

from __future__ import annotations

import pytest

from transcriber.application.probe import MediaProbeService
from transcriber.core.media import MediaError, MediaMetadata, ProbeResult


def _media() -> MediaMetadata:
    return MediaMetadata(
        media_id="i",
        title="t",
        extractor="e",
        webpage_url="u",
        duration_seconds=None,
        uploader=None,
        formats=(),
    )


class _FakeEngine:
    def __init__(self, result: ProbeResult) -> None:
        self.result = result
        self.received: str | None = None

    def probe(self, url: str) -> ProbeResult:
        self.received = url
        return self.result


def test_probe_trims_and_delegates() -> None:
    engine = _FakeEngine(_media())
    result = MediaProbeService(engine).probe("  https://x/y  ")
    assert result is engine.result
    assert engine.received == "https://x/y"


def test_empty_url_raises() -> None:
    with pytest.raises(MediaError):
        MediaProbeService(_FakeEngine(_media())).probe("   ")
