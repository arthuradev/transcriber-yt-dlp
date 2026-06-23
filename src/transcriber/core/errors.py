"""Core application error types.

Pure domain errors with no dependency on UI, adapters, or I/O. Every error is
structured: it carries a machine-readable code, a user-facing message, a
severity, optional technical detail, and an optional recovery suggestion.
"""

from __future__ import annotations

from enum import Enum


class ErrorSeverity(Enum):
    """Severity levels for application errors."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AppError(Exception):
    """Base class for structured application errors."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        detail: str | None = None,
        recovery: str | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.severity = severity
        self.detail = detail
        self.recovery = recovery

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"
