"""Build operation reports from domain results."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime

from transcriber.core.download import DownloadOutcome
from transcriber.core.plan import DownloadPlan
from transcriber.core.report import OperationReport


def build_download_report(
    plan: DownloadPlan,
    outcome: DownloadOutcome,
    *,
    now: Callable[[], datetime] | None = None,
) -> OperationReport:
    """Build a secret-free report for a completed download."""
    timestamp = (now if now is not None else (lambda: datetime.now(UTC)))()
    if outcome.ok:
        status = "ok"
    elif outcome.succeeded > 0:
        status = "partial"
    else:
        status = "failed"

    detail = f"profile={plan.profile_id} cookies={'yes' if plan.cookies_from_browser else 'no'}"
    return OperationReport(
        kind="download",
        status=status,
        item_count=plan.item_count,
        succeeded=outcome.succeeded,
        skipped=outcome.skipped,
        failed=outcome.failed,
        outputs=outcome.output_paths,
        warnings=plan.warnings,
        timestamp=timestamp,
        detail=detail,
    )
