"""Tests for the cookie guard integrated into the download flow."""

from __future__ import annotations

import io
from collections.abc import Callable, Sequence
from datetime import date

from rich.console import Console

from transcriber.application.executor import DownloadExecutor
from transcriber.application.planner import DownloadPlanner
from transcriber.application.probe import MediaProbeService
from transcriber.config.models import CookiesConfig, Language, PathsConfig
from transcriber.core.download import (
    DownloadProgress,
    DownloadRequest,
    DownloadResult,
    DownloadStatus,
)
from transcriber.core.media import MediaFormat, MediaMetadata, ProbeResult
from transcriber.core.profiles import DownloadProfile
from transcriber.ui.download_flow import DownloadFlow, DownloadSource
from transcriber.ui.i18n import Translator


class _Engine:
    def __init__(self) -> None:
        self.request: DownloadRequest | None = None

    def probe(self, url: str) -> ProbeResult:
        return MediaMetadata("abc", "V", "Yt", "https://x/abc", 10.0, None, ())

    def download(
        self,
        request: DownloadRequest,
        on_progress: Callable[[DownloadProgress], None],
    ) -> DownloadResult:
        self.request = request
        on_progress(DownloadProgress(DownloadStatus.FINISHED, 1, 1, None, None, None))
        return DownloadResult(True, request.output_path, None)


class _Prompts:
    def __init__(self, *, cookies_ok: bool) -> None:
        self._cookies_ok = cookies_ok

    def ask_source(self) -> DownloadSource | None:
        return DownloadSource(is_batch=False, value="https://x/abc")

    def select_profile(self, profiles: Sequence[DownloadProfile]) -> DownloadProfile | None:
        return next((p for p in profiles if p.profile_id == "video_best"), None)

    def select_format(self, formats: Sequence[MediaFormat]) -> MediaFormat | None:
        return None

    def ask_output_dir(self, default: str) -> str:
        return "out"

    def confirm(self, *, strong: bool) -> bool:
        return True

    def confirm_cookies(self) -> bool:
        return self._cookies_ok


def _flow(
    console: Console, engine: _Engine, prompts: _Prompts, cookies: CookiesConfig
) -> DownloadFlow:
    return DownloadFlow(
        probe_service=MediaProbeService(engine),
        planner=DownloadPlanner(today=lambda: date(2026, 6, 24)),
        console=console,
        translator=Translator(Language.EN_US),
        paths=PathsConfig(download_dir="out"),
        prompts=prompts,
        executor=DownloadExecutor(engine),
        cookies=cookies,
    )


def test_cookies_used_when_enabled_and_confirmed(
    console_buffer: tuple[Console, io.StringIO],
) -> None:
    console, _ = console_buffer
    engine = _Engine()
    _flow(
        console, engine, _Prompts(cookies_ok=True), CookiesConfig(enabled=True, browser="chrome")
    ).run("video")
    assert engine.request is not None
    assert engine.request.cookies_from_browser == "chrome"


def test_cookies_skipped_when_not_confirmed(
    console_buffer: tuple[Console, io.StringIO],
) -> None:
    console, _ = console_buffer
    engine = _Engine()
    _flow(
        console, engine, _Prompts(cookies_ok=False), CookiesConfig(enabled=True, browser="chrome")
    ).run("video")
    assert engine.request is not None
    assert engine.request.cookies_from_browser is None


def test_cookies_off_by_default(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, _ = console_buffer
    engine = _Engine()
    _flow(console, engine, _Prompts(cookies_ok=True), CookiesConfig()).run("video")
    assert engine.request is not None
    assert engine.request.cookies_from_browser is None
