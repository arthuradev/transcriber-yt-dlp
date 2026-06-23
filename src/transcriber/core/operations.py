"""Core domain enumerations for operations and risk levels."""

from __future__ import annotations

from enum import Enum


class OperationType(Enum):
    """Top-level operation categories supported by the application."""

    DOWNLOAD = "download"
    TRANSCRIBE = "transcribe"
    CLEANUP = "cleanup"
    METADATA = "metadata"


class RiskLevel(Enum):
    """Risk classification used by the safety pipeline."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
