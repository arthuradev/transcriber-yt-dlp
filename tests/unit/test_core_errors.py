"""Unit tests for core domain errors and enumerations."""

from __future__ import annotations

from transcriber.core.errors import AppError, ErrorSeverity
from transcriber.core.operations import OperationType, RiskLevel


def test_app_error_carries_structured_fields() -> None:
    err = AppError(
        "E_TEST",
        "something went wrong",
        severity=ErrorSeverity.WARNING,
        detail="technical detail",
        recovery="try again",
    )
    assert err.code == "E_TEST"
    assert err.message == "something went wrong"
    assert err.severity is ErrorSeverity.WARNING
    assert err.detail == "technical detail"
    assert err.recovery == "try again"
    assert str(err) == "[E_TEST] something went wrong"


def test_app_error_defaults() -> None:
    err = AppError("E_X", "msg")
    assert err.severity is ErrorSeverity.ERROR
    assert err.detail is None
    assert err.recovery is None


def test_operation_and_risk_enum_values() -> None:
    assert OperationType.DOWNLOAD.value == "download"
    assert OperationType.TRANSCRIBE.value == "transcribe"
    assert RiskLevel.HIGH.value == "high"
    assert {level.value for level in RiskLevel} == {"low", "medium", "high"}
