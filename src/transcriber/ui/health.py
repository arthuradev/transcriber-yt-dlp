"""Render a system health/dependency report."""

from __future__ import annotations

from rich.console import Console
from rich.markup import escape
from rich.table import Table

from transcriber.core.health import HealthReport
from transcriber.ui.i18n import Translator


def render_health(console: Console, report: HealthReport, t: Translator) -> None:
    """Render the dependency checks as a status table."""
    table = Table(title=t("health.title"), title_style="menu.title")
    table.add_column(t("health.check"))
    table.add_column(t("health.status"))
    table.add_column(t("health.detail"), style="muted")
    for check in report.checks:
        style = "success" if check.ok else "warning"
        mark = t("health.ok") if check.ok else t("health.missing")
        table.add_row(escape(check.name), f"[{style}]{mark}[/{style}]", escape(check.detail))
    console.print(table)
