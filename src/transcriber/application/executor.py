"""Download execution use case.

Executes a plan's items sequentially through the ``DownloadEnginePort``,
forwarding progress and aggregating results. No I/O of its own; the engine does
the downloading.
"""

from __future__ import annotations

from transcriber.core.download import (
    DownloadOutcome,
    DownloadRequest,
    DownloadResult,
    ProgressCallback,
)
from transcriber.core.plan import DownloadPlan
from transcriber.ports.media_engine import DownloadEnginePort


class DownloadExecutor:
    """Runs the download plan and collects results."""

    def __init__(self, engine: DownloadEnginePort) -> None:
        self._engine = engine

    def execute(self, plan: DownloadPlan, *, on_progress: ProgressCallback) -> DownloadOutcome:
        results: list[DownloadResult] = []
        for item in plan.items:
            request = DownloadRequest(
                url=item.url,
                format_selector=plan.format_selector,
                output_path=item.output_path,
                extract_audio=plan.extract_audio,
                audio_format=plan.audio_format,
            )
            results.append(self._engine.download(request, on_progress))
        return DownloadOutcome(results=tuple(results))
