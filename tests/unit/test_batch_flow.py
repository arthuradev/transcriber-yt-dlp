"""Test the download flow's batch (.txt) path."""

from __future__ import annotations

import io
from collections.abc import Sequence
from datetime import date

from rich.console import Console

from transcriber.application.batch import BatchProbeService
from transcriber.application.planner import DownloadPlanner
from transcriber.application.probe import MediaProbeService
from transcriber.config.models import Language, PathsConfig
from transcriber.core.media import MediaFormat, MediaMetadata, ProbeResult
from transcriber.core.profiles import DownloadProfile
from transcriber.ui.download_flow import DownloadFlow, DownloadSource
from transcriber.ui.i18n import Translator


class _Engine:
    def __init__(self) -> None:
        self.probed: list[str] = []

    def probe(self, url: str) -> ProbeResult:
        self.probed.append(url)
        return MediaMetadata(url, f"Title {url}", "Yt", url, None, None, ())


class _Reader:
    def __init__(self, text: str) -> None:
        self._text = text

    def read_text(self, path: str) -> str:
        return self._text


class _Prompts:
    def __init__(self, *, path: str, profile_id: str) -> None:
        self._path = path
        self._profile_id = profile_id

    def ask_source(self) -> DownloadSource | None:
        return DownloadSource(is_batch=True, value=self._path)

    def select_profile(self, profiles: Sequence[DownloadProfile]) -> DownloadProfile | None:
        return next((p for p in profiles if p.profile_id == self._profile_id), None)

    def select_format(self, formats: Sequence[MediaFormat]) -> MediaFormat | None:
        return None

    def ask_output_dir(self, default: str) -> str:
        return "out"

    def confirm(self, *, strong: bool) -> bool:
        return True

    def confirm_cookies(self) -> bool:
        return False


def test_batch_flow_probes_and_plans_all_urls(
    console_buffer: tuple[Console, io.StringIO],
) -> None:
    console, buffer = console_buffer
    engine = _Engine()
    reader = _Reader("https://a\nhttps://b\nhttps://c")
    flow = DownloadFlow(
        probe_service=MediaProbeService(engine),
        planner=DownloadPlanner(today=lambda: date(2026, 6, 24)),
        console=console,
        translator=Translator(Language.EN_US),
        paths=PathsConfig(download_dir="out"),
        prompts=_Prompts(path="urls.txt", profile_id="video_best"),
        batch_service=BatchProbeService(engine, reader),
    )
    flow.run("video")
    output = buffer.getvalue()
    assert "3 item" in output
    assert engine.probed == ["https://a", "https://b", "https://c"]
