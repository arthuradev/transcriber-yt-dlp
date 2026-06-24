"""Tests for the audit log."""

from __future__ import annotations

from datetime import UTC, datetime

from transcriber.core.operations import RiskLevel
from transcriber.safety.audit import AuditLog


def test_records_event() -> None:
    fixed = datetime(2026, 6, 24, tzinfo=UTC)
    log = AuditLog(now=lambda: fixed)
    event = log.record("download", RiskLevel.HIGH, "items=3")
    assert event.action == "download"
    assert event.risk is RiskLevel.HIGH
    assert event.detail == "items=3"
    assert event.timestamp == fixed
    assert log.events == (event,)


def test_records_multiple_events() -> None:
    log = AuditLog()
    log.record("a", RiskLevel.LOW)
    log.record("b", RiskLevel.MEDIUM)
    assert len(log.events) == 2
