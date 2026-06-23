"""WeatherAPI.com adapter (implements WeatherPort).

Performs a single ``current.json`` GET. The API key is passed as a query
parameter but the URL is never logged, and the key is redacted from any error
detail. The HTTP transport is injectable so the adapter is testable offline.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from collections.abc import Callable
from typing import Any
from urllib.parse import urlencode

from transcriber.core.weather import WeatherError, WeatherSnapshot

HttpGet = Callable[[str, float], str]

_DEFAULT_BASE_URL = "https://api.weatherapi.com/v1"


def _urllib_get(url: str, timeout: float) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "transcriber"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body: bytes = response.read()
    return body.decode("utf-8")


def _redact(text: str, secret: str) -> str:
    return text.replace(secret, "***") if secret else text


class WeatherApiAdapter:
    """Fetches weather from WeatherAPI.com."""

    def __init__(
        self,
        api_key: str,
        *,
        http_get: HttpGet = _urllib_get,
        timeout: float = 4.0,
        base_url: str = _DEFAULT_BASE_URL,
    ) -> None:
        self._api_key = api_key
        self._http_get = http_get
        self._timeout = timeout
        self._base_url = base_url.rstrip("/")

    def fetch(self, query: str, units: str) -> WeatherSnapshot:
        params = urlencode({"key": self._api_key, "q": query, "aqi": "no"})
        url = f"{self._base_url}/current.json?{params}"
        try:
            body = self._http_get(url, self._timeout)
            data: Any = json.loads(body)
        except (urllib.error.URLError, OSError, ValueError, TimeoutError) as exc:
            raise WeatherError(
                "Weather request failed",
                detail=_redact(str(exc), self._api_key),
            ) from exc
        return self._parse(data, units)

    def _parse(self, data: Any, units: str) -> WeatherSnapshot:
        try:
            location = data["location"]
            current = data["current"]
            if units == "imperial":
                temperature = float(current["temp_f"])
                unit = "F"
            else:
                temperature = float(current["temp_c"])
                unit = "C"
            return WeatherSnapshot(
                location=str(location["name"]),
                temperature=temperature,
                unit=unit,
                condition=str(current["condition"]["text"]),
                local_time=str(location["localtime"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise WeatherError("Unexpected weather response", detail=str(exc)) from exc
