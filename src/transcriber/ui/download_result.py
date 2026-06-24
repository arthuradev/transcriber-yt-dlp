"""Render the final download outcome."""

from __future__ import annotations

from rich.console import Console
from rich.markup import escape
from rich.panel import Panel

from transcriber.core.download import DownloadOutcome
from transcriber.ui.i18n import Translator


def render_download_summary(console: Console, outcome: DownloadOutcome, t: Translator) -> None:
    """Render a success/partial/failure panel with output paths and errors."""
    if outcome.ok:
        title, style = t("download.success_title"), "success"
    elif outcome.succeeded > 0:
        title, style = t("download.partial_title"), "warning"
    else:
        title, style = t("download.failed_title"), "error"

    lines = [t("download.summary", ok=outcome.succeeded, failed=outcome.failed)]
    for path in outcome.output_paths:
        lines.append(escape(path))
    for result in outcome.results:
        if not result.ok and result.error:
            lines.append(f"[error]{escape(result.error)}[/error]")

    console.print(Panel("\n".join(lines), title=title, border_style=style))
