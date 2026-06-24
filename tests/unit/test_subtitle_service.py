"""Tests for the subtitle service."""

from __future__ import annotations

from transcriber.application.subtitles import SubtitleService
from transcriber.core.subtitles import SubtitleRequest, SubtitleResult


class _Engine:
    def __init__(self, result: SubtitleResult) -> None:
        self._result = result
        self.received: SubtitleRequest | None = None

    def download_subtitles(self, request: SubtitleRequest) -> SubtitleResult:
        self.received = request
        return self._result


def _request(languages: tuple[str, ...] = ("en",)) -> SubtitleRequest:
    return SubtitleRequest("https://x", languages, "srt", "out/stem")


def test_delegates_to_engine() -> None:
    engine = _Engine(SubtitleResult(True, ("out/stem.en.srt",), None))
    result = SubtitleService(engine).download(_request())
    assert result.ok
    assert engine.received is not None


def test_empty_languages_is_rejected() -> None:
    engine = _Engine(SubtitleResult(True, (), None))
    result = SubtitleService(engine).download(_request(languages=()))
    assert not result.ok
    assert engine.received is None
