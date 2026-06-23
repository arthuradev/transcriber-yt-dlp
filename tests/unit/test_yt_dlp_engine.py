"""Tests for the yt-dlp engine adapter (with an injected extractor)."""

from __future__ import annotations

from typing import Any

import pytest

from transcriber.adapters.yt_dlp_engine import YtDlpEngine
from transcriber.core.media import MediaError, MediaMetadata


def test_engine_maps_injected_info() -> None:
    info: dict[str, Any] = {
        "id": "x",
        "title": "T",
        "extractor": "yt",
        "webpage_url": "u",
        "formats": [],
    }
    engine = YtDlpEngine(extract=lambda url: info)
    result = engine.probe("https://x")
    assert isinstance(result, MediaMetadata)
    assert result.media_id == "x"


def test_engine_empty_url_raises() -> None:
    engine = YtDlpEngine(extract=lambda url: {"id": "x", "title": "T"})
    with pytest.raises(MediaError):
        engine.probe("   ")


def test_engine_propagates_extract_error() -> None:
    def boom(url: str) -> dict[str, Any]:
        raise MediaError("nope")

    with pytest.raises(MediaError):
        YtDlpEngine(extract=boom).probe("https://x")
