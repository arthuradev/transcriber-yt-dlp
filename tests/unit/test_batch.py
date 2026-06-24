"""Tests for batch URL parsing and the batch probe service."""

from __future__ import annotations

from transcriber.application.batch import BatchProbeService
from transcriber.core.batch import parse_url_list
from transcriber.core.media import MediaError, MediaMetadata, ProbeResult


def test_parse_url_list_skips_blanks_and_comments() -> None:
    text = "https://a\n\n  # comment\nhttps://b  \n#x\nhttps://c"
    assert parse_url_list(text) == ["https://a", "https://b", "https://c"]


class _Reader:
    def __init__(self, text: str = "", *, error: bool = False) -> None:
        self._text = text
        self._error = error

    def read_text(self, path: str) -> str:
        if self._error:
            raise OSError("cannot read")
        return self._text


class _Engine:
    def __init__(self, ok_urls: set[str]) -> None:
        self._ok = ok_urls

    def probe(self, url: str) -> ProbeResult:
        if url in self._ok:
            return MediaMetadata(url, "T", "Yt", url, None, None, ())
        raise MediaError("bad url")


def test_batch_probe_collects_results_and_errors() -> None:
    reader = _Reader("https://a\nhttps://bad\nhttps://c")
    engine = _Engine({"https://a", "https://c"})
    result = BatchProbeService(engine, reader).probe_file("f.txt")
    assert len(result.results) == 2
    assert len(result.errors) == 1
    assert "https://bad" in result.errors[0]


def test_batch_file_read_error_is_reported() -> None:
    result = BatchProbeService(_Engine(set()), _Reader(error=True)).probe_file("missing.txt")
    assert result.results == ()
    assert len(result.errors) == 1
