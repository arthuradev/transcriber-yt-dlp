"""Audit event modeling.

Records what sensitive actions happened, at what risk level, with a secret-free
detail string. In-memory for now; persistence/reporting arrives in Phase 15.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime

from transcriber.core.operations import RiskLevel


@dataclass(frozen=True)
class AuditEvent:
    """A single recorded sensitive action."""

    action: str
    risk: RiskLevel
    detail: str
    timestamp: datetime


class AuditLog:
    """Collects audit events in memory."""

    def __init__(self, *, now: Callable[[], datetime] | None = None) -> None:
        self._now = now if now is not None else (lambda: datetime.now(UTC))
        self._events: list[AuditEvent] = []

    def record(self, action: str, risk: RiskLevel, detail: str = "") -> AuditEvent:
        """Record an event. ``detail`` must not contain secrets or transcript text."""
        event = AuditEvent(action=action, risk=risk, detail=detail, timestamp=self._now())
        self._events.append(event)
        return event

    @property
    def events(self) -> tuple[AuditEvent, ...]:
        return tuple(self._events)
