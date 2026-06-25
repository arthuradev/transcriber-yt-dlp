"""Build a health/dependency report from a system probe."""

from __future__ import annotations

from transcriber.core.health import HealthCheck, HealthReport
from transcriber.ports.system_probe import SystemProbe


def build_health_report(probe: SystemProbe) -> HealthReport:
    """Run the dependency checks and return a report."""
    return HealthReport(
        checks=(
            HealthCheck(
                "windows",
                probe.is_windows(),
                "Windows is the supported platform.",
            ),
            HealthCheck(
                "ffmpeg",
                probe.has_ffmpeg(),
                "Needed for audio extraction and some merges.",
            ),
            HealthCheck(
                "gpu",
                probe.gpu_available(),
                "Needed for transcription (GPU-only, no CPU fallback).",
            ),
        )
    )
