"""Local YAML persistence for the user configuration.

Implements the ``ConfigRepository`` port. The config lives in a user-local
directory and is never committed (see ``.gitignore``). Secrets are not stored
here; API keys belong in the environment / ``.env``.
"""

from __future__ import annotations

import os
from pathlib import Path

import yaml

from transcriber.config.models import UserConfig


def default_config_path() -> Path:
    """Return the default user-local config path.

    Uses ``%APPDATA%\\Transcriber\\config.yaml`` on Windows, falling back to
    ``~/.config/Transcriber/config.yaml`` elsewhere.
    """
    appdata = os.environ.get("APPDATA")
    root = Path(appdata) if appdata else Path.home() / ".config"
    return root / "Transcriber" / "config.yaml"


class ConfigStore:
    """File-backed user configuration store."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def exists(self) -> bool:
        """Whether the configuration file exists."""
        return self.path.is_file()

    def load(self) -> UserConfig:
        """Load and validate the configuration from disk."""
        raw: object = yaml.safe_load(self.path.read_text(encoding="utf-8")) or {}
        return UserConfig.model_validate(raw)

    def save(self, config: UserConfig) -> None:
        """Write the configuration to disk, creating parent directories."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = config.model_dump(mode="json")
        text = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
        self.path.write_text(text, encoding="utf-8")
