"""Port for probing the host system for dependencies."""

from __future__ import annotations

from typing import Protocol


class SystemProbe(Protocol):
    """Queries the host for required tools and capabilities."""

    def is_windows(self) -> bool:
        """Whether the host is Windows (the supported platform)."""
        ...

    def has_ffmpeg(self) -> bool:
        """Whether ffmpeg is on PATH."""
        ...

    def gpu_available(self) -> bool:
        """Whether a CUDA GPU (and the transcription stack) is available."""
        ...
