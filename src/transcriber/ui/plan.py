"""Dry-run plan renderer."""

from __future__ import annotations

from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table

from transcriber.core.operations import RiskLevel
from transcriber.core.plan import DownloadPlan
from transcriber.ui.i18n import Translator

_MAX_ITEMS = 15

_RISK_STYLE: dict[RiskLevel, str] = {
    RiskLevel.LOW: "success",
    RiskLevel.MEDIUM: "warning",
    RiskLevel.HIGH: "error",
}
_RISK_KEY: dict[RiskLevel, str] = {
    RiskLevel.LOW: "risk.low",
    RiskLevel.MEDIUM: "risk.medium",
    RiskLevel.HIGH: "risk.high",
}


def render_plan(console: Console, plan: DownloadPlan, t: Translator) -> None:
    """Render a download dry-run plan to the console."""
    risk_style = _RISK_STYLE[plan.risk]

    summary = Table(show_header=False, box=None)
    summary.add_column(style="muted")
    summary.add_column()
    summary.add_row(t("plan.profile"), escape(plan.profile_id))
    if plan.format_selector:
        summary.add_row(t("plan.format"), escape(plan.format_selector))
    summary.add_row(t("plan.output"), escape(plan.output_dir))
    summary.add_row(t("plan.items"), str(plan.item_count))
    summary.add_row(t("plan.risk"), f"[{risk_style}]{t(_RISK_KEY[plan.risk])}[/{risk_style}]")
    console.print(Panel(summary, title=t("plan.title"), border_style=risk_style))

    if plan.warnings:
        console.print(f"[warning]{t('plan.warnings')}:[/warning]")
        for warning in plan.warnings:
            console.print(f"  [warning]-[/warning] {escape(warning)}")

    if plan.items:
        table = Table(title=t("plan.items"), title_style="menu.title")
        table.add_column("#", style="muted")
        table.add_column("title")
        table.add_column("output")
        for index, item in enumerate(plan.items[:_MAX_ITEMS], start=1):
            label = item.title or item.media_id or "?"
            if item.is_duplicate:
                label = f"{label} (skip)"
            table.add_row(str(index), escape(label), escape(item.output_path))
        console.print(table)
        extra = len(plan.items) - _MAX_ITEMS
        if extra > 0:
            console.print(f"[muted]... +{extra}[/muted]")
