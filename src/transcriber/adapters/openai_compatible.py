"""OpenAI-compatible chat provider adapter (DeepSeek and similar).

Calls ``POST {base_url}/chat/completions`` with a system+user message. The API
key is sent as a Bearer header, never logged, and redacted from error detail. The
transcript text is never logged. The HTTP transport is injectable so the adapter
is testable offline. Uses stdlib ``urllib`` (no new dependency).
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from collections.abc import Callable
from typing import Any

from transcriber.core.cleanup import LLMError

# (url, json_body, api_key, timeout) -> response text
HttpPost = Callable[[str, str, str, float], str]


def _urllib_post(url: str, body: str, api_key: str, timeout: float) -> str:
    request = urllib.request.Request(
        url,
        data=body.encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "transcriber",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload: bytes = response.read()
    return payload.decode("utf-8")


def _redact(text: str, secret: str) -> str:
    return text.replace(secret, "***") if secret else text


class OpenAICompatibleProvider:
    """Chat-completion provider for OpenAI-compatible endpoints."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        http_post: HttpPost = _urllib_post,
        timeout: float = 60.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._http_post = http_post
        self._timeout = timeout

    def complete(self, system: str, user: str, model: str) -> str:
        url = f"{self._base_url}/chat/completions"
        body = json.dumps(
            {
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "temperature": 0.2,
                "stream": False,
            }
        )
        try:
            response = self._http_post(url, body, self._api_key, self._timeout)
            data: Any = json.loads(response)
            return str(data["choices"][0]["message"]["content"])
        except (urllib.error.URLError, OSError, ValueError, KeyError, IndexError, TypeError) as exc:
            raise LLMError(
                "LLM request failed",
                detail=_redact(str(exc), self._api_key),
            ) from exc
