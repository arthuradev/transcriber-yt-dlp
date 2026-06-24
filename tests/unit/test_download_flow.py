"""Tests for the interactive download flow (driven by scripted prompts)."""

from __future__ import annotations

import io
from collections.abc import Sequence
from datetime import date

from rich.console import Console

from transcriber.application.planner import DownloadPlanner
from transcriber.application.probe import MediaProbeService
from transcriber.config.models import Language, PathsConfig
from transcriber.core.media import MediaError, MediaFormat, MediaMetadata, ProbeResult
from transcriber.core.profiles import MANUAL_PROFILE_ID, DownloadProfile
from transcriber.ui.download_flow import DownloadFlow, DownloadSource
from transcriber.ui.i18n import Translator


class _FakeEngine:
    def __init__(self, result: ProbeResult) -> None:
        self._result = result

    def probe(self, url: str) -> ProbeResult:
        return self._result


class _FailingEngine:
    def probe(self, url: str) -> ProbeResult:
        raise MediaError("bad url")


class _ScriptedPrompts:
    def __init__(
        self,
        *,
        url: str,
        profile_id: str,
        output_dir: str,
        confirm: bool,
        fmt: MediaFormat | None = None,
    ) -> None:
        self._url = url
        self._profile_id = profile_id
        self._output_dir = output_dir
        self._confirm = confirm
        self._fmt = fmt

    def ask_source(self) -> DownloadSource | None:
        return DownloadSource(is_batch=False, value=self._url)

    def select_profile(self, profiles: Sequence[DownloadProfile]) -> DownloadProfile | None:
        return next((p for p in profiles if p.profile_id == self._profile_id), None)

    def select_format(self, formats: Sequence[MediaFormat]) -> MediaFormat | None:
        return self._fmt

    def ask_output_dir(self, default: str) -> str:
        return self._output_dir

    def confirm(self, *, strong: bool) -> bool:
        return self._confirm

    def confirm_cookies(self) -> bool:
        return False


def _media() -> MediaMetadata:
    return MediaMetadata(
        media_id="abc",
        title="My Video",
        extractor="Youtube",
        webpage_url="https://x/abc",
        duration_seconds=100.0,
        uploader=None,
        formats=(),
    )


def _flow(
    console: Console,
    engine: _FakeEngine | _FailingEngine,
    prompts: _ScriptedPrompts,
) -> DownloadFlow:
    return DownloadFlow(
        probe_service=MediaProbeService(engine),
        planner=DownloadPlanner(today=lambda: date(2026, 6, 24)),
        console=console,
        translator=Translator(Language.EN_US),
        paths=PathsConfig(download_dir="out"),
        prompts=prompts,
    )


def test_flow_renders_metadata_plan_and_proceeds(
    console_buffer: tuple[Console, io.StringIO],
) -> None:
    console, buffer = console_buffer
    prompts = _ScriptedPrompts(
        url="https://x/abc", profile_id="video_best", output_dir="out", confirm=True
    )
    _flow(console, _FakeEngine(_media()), prompts).run("video")
    output = buffer.getvalue()
    assert "My Video" in output
    assert "video_best" in output
    assert "Execution will be available" in output


def test_flow_cancel(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    prompts = _ScriptedPrompts(
        url="https://x/abc", profile_id="video_best", output_dir="out", confirm=False
    )
    _flow(console, _FakeEngine(_media()), prompts).run("video")
    output = buffer.getvalue()
    assert "Cancelled" in output
    assert "Execution will be available" not in output


def test_flow_probe_error(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    prompts = _ScriptedPrompts(url="bad", profile_id="video_best", output_dir="out", confirm=True)
    _flow(console, _FailingEngine(), prompts).run("video")
    assert "Could not read metadata" in buffer.getvalue()


def test_flow_manual_format_builds_manual_profile(
    console_buffer: tuple[Console, io.StringIO],
) -> None:
    console, buffer = console_buffer
    fmt = MediaFormat("248", "webm", 1080, 5_000_000, "vp9", "none", "1080p")
    media = MediaMetadata(
        media_id="abc",
        title="My Video",
        extractor="Youtube",
        webpage_url="https://x/abc",
        duration_seconds=100.0,
        uploader=None,
        formats=(fmt,),
    )
    prompts = _ScriptedPrompts(
        url="https://x/abc",
        profile_id=MANUAL_PROFILE_ID,
        output_dir="out",
        confirm=True,
        fmt=fmt,
    )
    _flow(console, _FakeEngine(media), prompts).run("video")
    assert "manual:248" in buffer.getvalue()
