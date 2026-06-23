"""Port for loading and persisting user configuration."""

from __future__ import annotations

from typing import Protocol

from transcriber.config.models import UserConfig


class ConfigRepository(Protocol):
    """Persistence contract for the user configuration."""

    def exists(self) -> bool:
        """Whether a stored configuration already exists."""
        ...

    def load(self) -> UserConfig:
        """Load and validate the stored configuration."""
        ...

    def save(self, config: UserConfig) -> None:
        """Persist the configuration."""
        ...
