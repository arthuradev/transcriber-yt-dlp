"""First-run setup use case.

Detects whether this is the first run and, if so, drives the setup questions
through the ``FirstRunPrompts`` port and persists the resulting configuration
through the ``ConfigRepository`` port. This layer owns the flow and the mapping
to a ``UserConfig``; it knows nothing about the terminal or YAML.
"""

from __future__ import annotations

from collections.abc import Sequence

from transcriber.config.models import (
    GPUConfig,
    LLMConfig,
    PathsConfig,
    UIConfig,
    UserConfig,
    WeatherConfig,
)
from transcriber.ports.config_repository import ConfigRepository
from transcriber.ports.first_run_prompts import FirstRunPrompts


class FirstRunService:
    """Coordinates first-run detection, the setup wizard, and persistence."""

    def __init__(self, repository: ConfigRepository) -> None:
        self._repository = repository

    def is_first_run(self) -> bool:
        """Whether no configuration has been saved yet."""
        return not self._repository.exists()

    def setup(
        self,
        prompts: FirstRunPrompts,
        *,
        themes: Sequence[str],
        default_download_dir: str = "downloads",
    ) -> UserConfig:
        """Run the wizard, build the config, persist it, and return it."""
        language = prompts.ask_language()
        theme = prompts.ask_theme(themes)
        weather_enabled = prompts.ask_weather_enabled()
        city = prompts.ask_city() if weather_enabled else ""
        download_dir = prompts.ask_download_dir(default_download_dir)
        llm_enabled = prompts.ask_llm_enabled()
        gpu_acknowledged = prompts.acknowledge_gpu_only()

        config = UserConfig(
            language=language,
            ui=UIConfig(theme=theme),
            weather=WeatherConfig(
                enabled=weather_enabled,
                query=city,
                show_on_startup=weather_enabled,
            ),
            llm=LLMConfig(enabled=llm_enabled),
            paths=PathsConfig(download_dir=download_dir),
            gpu=GPUConfig(acknowledged_gpu_only=gpu_acknowledged),
        )
        self._repository.save(config)
        return config
