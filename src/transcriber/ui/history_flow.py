"""History view: show recent operations from the history repository."""

from __future__ import annotations

from rich.console import Console
from rich.markup import escape
from rich.table import Table

from transcriber.ports.history import HistoryRepositoryPort
from transcriber.ui.i18n import Translator

_STATUS_STYLE = {"ok": "success", "partial": "warning", "failed": "error"}


class HistoryFlow:
    """Renders the most recent operation-history entries."""

    def __init__(
        self,
        *,
        history: HistoryRepositoryPort,
        console: Console,
        translator: Translator,
        limit: int = 20,
    ) -> None:
        self._history = history
        self._console = console
        self._t = translator
        self._limit = limit

    def run(self) -> None:
        entries = self._history.recent(self._limit)
        if not entries:
            self._console.print(f"[muted]{self._t('history.empty')}[/muted]")
        else:
            table = Table(title=self._t("history.title"), title_style="menu.title")
            table.add_column(self._t("history.time"), style="muted")
            table.add_column(self._t("history.operation"))
            table.add_column(self._t("history.status"))
            table.add_column("ok/skip/fail", style="muted")
            for entry in entries:
                style = _STATUS_STYLE.get(entry.status, "info")
                table.add_row(
                    entry.timestamp.strftime("%Y-%m-%d %H:%M"),
                    escape(entry.kind),
                    f"[{style}]{escape(entry.status)}[/{style}]",
                    f"{entry.succeeded}/{entry.skipped}/{entry.failed}",
                )
            self._console.print(table)
        self._pause()

    def _pause(self) -> None:
        if self._console.is_terminal:
            self._console.input(f"[muted]{self._t('shell.press_enter')}[/muted] ")
