"""System health/dependency report domain (pure)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HealthCheck:
    """The result of one dependency/environment check."""

    name: str
    ok: bool
    detail: str


@dataclass(frozen=True)
class HealthReport:
    """A collection of health checks."""

    checks: tuple[HealthCheck, ...]

    @property
    def all_ok(self) -> bool:
        return all(check.ok for check in self.checks)
