"""Risk classification for download operations.

Pure classification (no I/O) following the safety pipeline:
- metadata-only reads are low risk;
- a normal public download is medium risk (simple confirmation);
- batches over the normal limit, forced overwrite, or cookies are high risk
  (strong confirmation).
"""

from __future__ import annotations

from dataclasses import dataclass

from transcriber.core.operations import RiskLevel

# Mirrors configs/safety.example.yaml.
BATCH_NORMAL_LIMIT = 5
BATCH_HIGH_LIMIT = 50

_RANK: dict[RiskLevel, int] = {RiskLevel.LOW: 0, RiskLevel.MEDIUM: 1, RiskLevel.HIGH: 2}


@dataclass(frozen=True)
class RiskAssessment:
    """The classified risk of an operation and what confirmation it needs."""

    level: RiskLevel
    requires_confirmation: bool
    requires_strong_confirmation: bool
    reasons: tuple[str, ...]


def _escalate(current: RiskLevel, candidate: RiskLevel) -> RiskLevel:
    return candidate if _RANK[candidate] > _RANK[current] else current


def classify_download(
    *,
    item_count: int,
    profile_kind: str,
    overwrite: bool,
    uses_cookies: bool = False,
) -> RiskAssessment:
    """Classify a download request into a risk level and confirmation needs."""
    if profile_kind == "metadata":
        return RiskAssessment(
            level=RiskLevel.LOW,
            requires_confirmation=False,
            requires_strong_confirmation=False,
            reasons=("Metadata only; nothing is downloaded.",),
        )

    level = RiskLevel.MEDIUM
    reasons: list[str] = []

    if item_count > BATCH_NORMAL_LIMIT:
        level = _escalate(level, RiskLevel.HIGH)
        reasons.append(f"Batch of {item_count} items (more than {BATCH_NORMAL_LIMIT}).")
    if item_count > BATCH_HIGH_LIMIT:
        reasons.append(f"Very large batch (more than {BATCH_HIGH_LIMIT} items).")
    if overwrite:
        level = _escalate(level, RiskLevel.HIGH)
        reasons.append("Existing files may be overwritten.")
    if uses_cookies:
        level = _escalate(level, RiskLevel.HIGH)
        reasons.append("Browser cookies are in use.")

    return RiskAssessment(
        level=level,
        requires_confirmation=level is not RiskLevel.LOW,
        requires_strong_confirmation=level is RiskLevel.HIGH,
        reasons=tuple(reasons),
    )
