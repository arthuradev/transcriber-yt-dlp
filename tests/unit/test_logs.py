"""Tests for the redacted file logger."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from transcriber.observability.logs import FileLogger, default_log_path


def test_default_log_path() -> None:
    assert default_log_path().name == "transcriber.log"


def test_logs_redact_secrets(tmp_path: Path) -> None:
    path = tmp_path / "sub" / "t.log"
    logger = FileLogger(path, secrets=["SECRET"], now=lambda: datetime(2026, 6, 24, tzinfo=UTC))
    logger.log("INFO", "using key SECRET and https://x?token=abc123")
    content = path.read_text(encoding="utf-8")
    assert "SECRET" not in content
    assert "abc123" not in content
    assert "[INFO]" in content


def test_logs_append(tmp_path: Path) -> None:
    path = tmp_path / "t.log"
    logger = FileLogger(path)
    logger.log("INFO", "a")
    logger.log("INFO", "b")
    assert len(path.read_text(encoding="utf-8").splitlines()) == 2
