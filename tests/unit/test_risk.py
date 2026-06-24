"""Tests for download risk classification."""

from __future__ import annotations

from transcriber.core.operations import RiskLevel
from transcriber.safety.risk import classify_download


def test_metadata_is_low_risk() -> None:
    assessment = classify_download(item_count=1, profile_kind="metadata", overwrite=False)
    assert assessment.level is RiskLevel.LOW
    assert not assessment.requires_confirmation


def test_single_download_is_medium() -> None:
    assessment = classify_download(item_count=1, profile_kind="video", overwrite=False)
    assert assessment.level is RiskLevel.MEDIUM
    assert assessment.requires_confirmation
    assert not assessment.requires_strong_confirmation


def test_batch_over_limit_is_high() -> None:
    assessment = classify_download(item_count=6, profile_kind="video", overwrite=False)
    assert assessment.level is RiskLevel.HIGH
    assert assessment.requires_strong_confirmation


def test_overwrite_is_high() -> None:
    assessment = classify_download(item_count=1, profile_kind="audio", overwrite=True)
    assert assessment.level is RiskLevel.HIGH


def test_cookies_is_high() -> None:
    assessment = classify_download(
        item_count=1, profile_kind="video", overwrite=False, uses_cookies=True
    )
    assert assessment.level is RiskLevel.HIGH
