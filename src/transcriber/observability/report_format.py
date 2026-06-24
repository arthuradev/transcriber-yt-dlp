"""Operation report serialization (pure)."""

from __future__ import annotations

import json

from transcriber.core.report import OperationReport


def report_to_json(report: OperationReport) -> str:
    """Serialize a report to pretty JSON."""
    payload = {
        "kind": report.kind,
        "status": report.status,
        "item_count": report.item_count,
        "succeeded": report.succeeded,
        "skipped": report.skipped,
        "failed": report.failed,
        "outputs": list(report.outputs),
        "warnings": list(report.warnings),
        "timestamp": report.timestamp.isoformat(),
        "detail": report.detail,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def report_to_markdown(report: OperationReport) -> str:
    """Serialize a report to Markdown."""
    lines = [
        f"# {report.kind} report",
        "",
        f"- Status: {report.status}",
        f"- Items: {report.item_count}",
        f"- Succeeded: {report.succeeded}",
        f"- Skipped: {report.skipped}",
        f"- Failed: {report.failed}",
        f"- Time: {report.timestamp.isoformat()}",
    ]
    if report.detail:
        lines.append(f"- Detail: {report.detail}")
    if report.outputs:
        lines.extend(["", "## Outputs", *[f"- {path}" for path in report.outputs]])
    if report.warnings:
        lines.extend(["", "## Warnings", *[f"- {warning}" for warning in report.warnings]])
    return "\n".join(lines)
