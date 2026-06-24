"""Redaction helpers for safe logging.

Never let secrets or token-bearing URLs reach logs/reports. Pure string helpers.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

_TOKEN_PARAM = re.compile(
    r"([?&](?:token|key|api_key|apikey|access_token|sig|signature|auth|password|pwd)=)[^&\s]+",
    re.IGNORECASE,
)

_REDACTED = "***"


def redact_secrets(text: str, secrets: Iterable[str]) -> str:
    """Replace each non-empty secret occurrence in ``text`` with ``***``."""
    for secret in secrets:
        if secret:
            text = text.replace(secret, _REDACTED)
    return text


def redact_url_tokens(text: str) -> str:
    """Replace token/key/auth query-parameter values with ``***``."""
    return _TOKEN_PARAM.sub(rf"\1{_REDACTED}", text)


def redact(text: str, secrets: Iterable[str] = ()) -> str:
    """Redact both known secrets and token-bearing URL parameters."""
    return redact_url_tokens(redact_secrets(text, secrets))
