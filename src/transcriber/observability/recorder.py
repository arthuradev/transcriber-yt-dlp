"""Operation recorder.

Bundles the durable record sinks for a completed operation: appends a history
entry, writes a secret-safe log line, and optionally writes a JSON report file.
All inputs are secret-free by construction (built from ``OperationReport``).
"""

from __future__ import annotations

from transcriber.core.report import OperationReport
from transcriber.observability.logs import FileLogger
from transcriber.observability.report_format import report_to_json
from transcriber.ports.history import HistoryRepositoryPort
from transcriber.storage.text_store import save_text


class OperationRecorder:
    """Records an operation to history, logs, and (optionally) a report file."""

    def __init__(
        self,
        *,
        history: HistoryRepositoryPort | None = None,
        logger: FileLogger | None = None,
        report_dir: str | None = None,
    ) -> None:
        self._history = history
        self._logger = logger
        self._report_dir = report_dir

    def record(self, report: OperationReport) -> None:
        if self._history is not None:
            self._history.add(report.to_history_entry())
        if self._logger is not None:
            self._logger.log("INFO", f"{report.kind} {report.status}: {report.detail}")
        if self._report_dir is not None:
            stem = f"report-{report.timestamp.strftime('%Y%m%d-%H%M%S')}-{report.kind}"
            save_text(report_to_json(report), output_dir=self._report_dir, stem=stem, ext=".json")
