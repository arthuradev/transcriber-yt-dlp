"""Local system probe (implements SystemProbe)."""

from __future__ import annotations

import shutil
import sys

from transcriber.adapters.faster_whisper_engine import FasterWhisperEngine


class LocalSystemProbe:
    """Probes the local host for required tools and capabilities."""

    def is_windows(self) -> bool:
        return sys.platform.startswith("win")

    def has_ffmpeg(self) -> bool:
        return shutil.which("ffmpeg") is not None

    def gpu_available(self) -> bool:
        return FasterWhisperEngine().gpu_available()
