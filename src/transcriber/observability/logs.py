"""Secret-safe file logging.

Every line is passed through redaction before being written, so secrets and
token-bearing URLs never reach the log. Logs are user-local (gitignored).
"""

from __future__ import annotations

import os
from collections.abc import Callable, Iterable
from datetime import UTC, datetime
from pathlib import Path

from transcriber.safety.redaction import redact


def default_log_path() -> Path:
    """Return the default user-local log file path."""
    appdata = os.environ.get("APPDATA")
    root = Path(appdata) if appdata else Path.home() / ".config"
    return root / "Transcriber" / "logs" / "transcriber.log"


class FileLogger:
    """Appends redacted, timestamped lines to a log file."""

    def __init__(
        self,
        path: Path,
        *,
        secrets: Iterable[str] = (),
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self._path = path
        self._secrets = tuple(secrets)
        self._now = now if now is not None else (lambda: datetime.now(UTC))

    def log(self, level: str, message: str) -> None:
        """Write one redacted log line."""
        line = f"{self._now().isoformat()} [{level}] {redact(message, self._secrets)}"
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(f"{line}\n")
