"""Tests for the interactive subtitle flow."""

from __future__ import annotations

import io
from collections.abc import Sequence
from datetime import date

from rich.console import Console

from transcriber.application.probe import MediaProbeService
from transcriber.application.subtitles import SubtitleService
from transcriber.config.models import Language, PathsConfig
from transcriber.core.media import MediaMetadata, PlaylistEntry, PlaylistMetadata, ProbeResult
from transcriber.core.subtitles import SubtitleRequest, SubtitleResult
from transcriber.ui.i18n import Translator
from transcriber.ui.subtitle_flow import SubtitleFlow


class _Engine:
    def __init__(self, probe_result: ProbeResult, sub_result: SubtitleResult) -> None:
        self._probe = probe_result
        self._sub = sub_result
        self.requests: list[SubtitleRequest] = []

    def probe(self, url: str) -> ProbeResult:
        return self._probe

    def download_subtitles(self, request: SubtitleRequest) -> SubtitleResult:
        self.requests.append(request)
        return self._sub


class _Prompts:
    def __init__(self, *, url: str, language: str | None) -> None:
        self._url = url
        self._language = language

    def ask_url(self) -> str:
        return self._url

    def select_language(self, languages: Sequence[str]) -> str | None:
        return self._language


def _media(subs: tuple[str, ...] = ("en", "es"), auto: tuple[str, ...] = ("fr",)) -> MediaMetadata:
    return MediaMetadata("abc", "My Video", "Youtube", "https://x/abc", 100.0, None, (), subs, auto)


def _flow(console: Console, engine: _Engine, prompts: _Prompts) -> SubtitleFlow:
    return SubtitleFlow(
        probe_service=MediaProbeService(engine),
        subtitle_service=SubtitleService(engine),
        console=console,
        translator=Translator(Language.EN_US),
        paths=PathsConfig(download_dir="out"),
        subtitle_format="srt",
        prompts=prompts,
        today=lambda: date(2026, 6, 24),
    )


def test_flow_downloads_subtitles(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    saved = SubtitleResult(True, ("out/Youtube/2026-06-24/My Video [abc].en.srt",), None)
    engine = _Engine(_media(), saved)
    _flow(console, engine, _Prompts(url="https://x/abc", language="en")).run()
    output = buffer.getvalue()
    assert "Subtitles saved" in output
    assert engine.requests[0].languages == ("en",)
    assert engine.requests[0].output_base.endswith("My Video [abc]")


def test_flow_no_subtitles(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    engine = _Engine(_media(subs=(), auto=()), SubtitleResult(False, (), None))
    _flow(console, engine, _Prompts(url="https://x/abc", language="en")).run()
    assert "No subtitles found" in buffer.getvalue()


def test_flow_playlist_unsupported(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    playlist = PlaylistMetadata("PL", "L", "Yt", "https://x/PL", 1, (PlaylistEntry("v", "T", "u"),))
    engine = _Engine(playlist, SubtitleResult(False, (), None))
    _flow(console, engine, _Prompts(url="https://x/PL", language="en")).run()
    assert "single video" in buffer.getvalue()
