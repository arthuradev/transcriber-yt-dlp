"""Tests for the OpenAI-compatible LLM provider adapter."""

from __future__ import annotations

import json
from collections.abc import Callable

import pytest

from transcriber.adapters.openai_compatible import OpenAICompatibleProvider
from transcriber.core.cleanup import LLMError


def _ok(content: str) -> str:
    return json.dumps({"choices": [{"message": {"content": content}}]})


def _fake_post(response: str) -> Callable[[str, str, str, float], str]:
    def post(url: str, body: str, api_key: str, timeout: float) -> str:
        return response

    return post


def test_complete_returns_content() -> None:
    provider = OpenAICompatibleProvider(
        base_url="https://api.x", api_key="K", http_post=_fake_post(_ok("cleaned"))
    )
    assert provider.complete("sys", "user", "m") == "cleaned"


def test_complete_builds_request() -> None:
    captured: dict[str, str] = {}

    def post(url: str, body: str, api_key: str, timeout: float) -> str:
        captured["url"] = url
        captured["body"] = body
        captured["key"] = api_key
        return _ok("x")

    OpenAICompatibleProvider(base_url="https://api.x/", api_key="SECRET", http_post=post).complete(
        "S", "U", "model-1"
    )
    assert captured["url"] == "https://api.x/chat/completions"
    assert captured["key"] == "SECRET"
    data = json.loads(captured["body"])
    assert data["model"] == "model-1"
    assert data["messages"][0]["content"] == "S"
    assert data["messages"][1]["content"] == "U"


def test_error_redacts_key() -> None:
    def boom(url: str, body: str, api_key: str, timeout: float) -> str:
        raise OSError("failed with key=SECRET")

    provider = OpenAICompatibleProvider(base_url="https://x", api_key="SECRET", http_post=boom)
    with pytest.raises(LLMError) as exc_info:
        provider.complete("s", "u", "m")
    assert "SECRET" not in str(exc_info.value)
    assert exc_info.value.detail is not None
    assert "SECRET" not in exc_info.value.detail


def test_malformed_response_raises() -> None:
    provider = OpenAICompatibleProvider(
        base_url="https://x", api_key="K", http_post=_fake_post('{"bad": true}')
    )
    with pytest.raises(LLMError):
        provider.complete("s", "u", "m")
