"""Port for collecting first-run setup answers.

The application drives first-run setup through this contract; the UI owns the
localized prompt text and input handling. Keeping it a port lets the setup flow
be tested with a scripted implementation and no terminal.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from transcriber.config.models import Language


class FirstRunPrompts(Protocol):
    """Questions asked once, on first run, to build the initial config."""

    def ask_language(self) -> Language:
        """Ask which UI language to use (shown bilingually)."""
        ...

    def ask_theme(self, available: Sequence[str]) -> str:
        """Ask which theme to use, given the available theme names."""
        ...

    def ask_weather_enabled(self) -> bool:
        """Ask whether to show weather on startup."""
        ...

    def ask_city(self) -> str:
        """Ask the weather city/query (only when weather is enabled)."""
        ...

    def ask_download_dir(self, default: str) -> str:
        """Ask the output folder, offering a default."""
        ...

    def ask_llm_enabled(self) -> bool:
        """Ask whether optional LLM transcript cleanup is desired."""
        ...

    def acknowledge_gpu_only(self) -> bool:
        """Confirm the user understands transcription is GPU-only (no CPU fallback)."""
        ...
