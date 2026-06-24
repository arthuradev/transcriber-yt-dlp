"""User configuration models.

Typed, validated configuration for user-local settings. These are pure data
models (Pydantic) with no I/O. Secrets (API keys) are intentionally NOT modelled
here: they live in the environment / ``.env`` and never in the persisted config.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class Language(StrEnum):
    """Supported UI languages."""

    PT_BR = "pt-BR"
    EN_US = "en-US"


class UIConfig(BaseModel):
    """Presentation preferences."""

    theme: str = "default"
    startup_animation: bool = True
    clear_screen_between_operations: bool = True


class WeatherConfig(BaseModel):
    """Optional weather/personalization preferences (no API key here)."""

    enabled: bool = False
    query: str = ""
    units: Literal["metric", "imperial"] = "metric"
    show_on_startup: bool = False
    cache_minutes: int = Field(default=15, ge=0)


class LLMConfig(BaseModel):
    """Optional transcript-cleanup provider preferences (no API key here)."""

    enabled: bool = False
    provider: str = "deepseek"
    base_url: str = "https://api.deepseek.com"
    model: str = "deepseek-v4-pro"
    ask_before_cleanup: bool = True
    cleanup_mode: str = "format_only"


class CookiesConfig(BaseModel):
    """Advanced, opt-in cookie preferences."""

    enabled: bool = False
    allow_browser_cookies: bool = True
    browser: str | None = None
    require_confirmation: bool = True
    redact_from_logs: bool = True


class PathsConfig(BaseModel):
    """Output organization preferences."""

    download_dir: str = "downloads"
    organize_by_site: bool = True
    organize_by_date: bool = True
    include_media_id_in_filename: bool = True
    overwrite_policy: Literal["ask", "skip", "overwrite"] = "ask"


class GPUConfig(BaseModel):
    """GPU policy acknowledgement (transcription is GPU-only, no CPU fallback)."""

    acknowledged_gpu_only: bool = False


class TranscriptionConfig(BaseModel):
    """Transcription preferences (faster-whisper, GPU-only)."""

    model: str = "large-v3"
    language: str = ""  # "" means auto-detect
    translate: bool = False
    output_format: Literal["txt", "md", "srt", "vtt", "json"] = "txt"
    keep_audio: bool = False


class SubtitlesConfig(BaseModel):
    """Subtitle download preferences."""

    format: Literal["srt", "vtt"] = "srt"


class UserConfig(BaseModel):
    """Root user configuration, persisted locally as YAML."""

    version: int = 1
    language: Language = Language.EN_US
    ui: UIConfig = Field(default_factory=UIConfig)
    weather: WeatherConfig = Field(default_factory=WeatherConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    cookies: CookiesConfig = Field(default_factory=CookiesConfig)
    paths: PathsConfig = Field(default_factory=PathsConfig)
    gpu: GPUConfig = Field(default_factory=GPUConfig)
    transcription: TranscriptionConfig = Field(default_factory=TranscriptionConfig)
    subtitles: SubtitlesConfig = Field(default_factory=SubtitlesConfig)
