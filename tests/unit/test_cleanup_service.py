"""Tests for the cleanup service (chunking + provider orchestration)."""

from __future__ import annotations

import pytest

from transcriber.application.cleanup import CleanupService
from transcriber.core.cleanup import CleanupProfile, LLMError, get_cleanup_profile


def _profile() -> CleanupProfile:
    profile = get_cleanup_profile("readable")
    assert profile is not None
    return profile


class _Provider:
    def __init__(self, *, fail: bool = False) -> None:
        self.calls: list[str] = []
        self._fail = fail

    def complete(self, system: str, user: str, model: str) -> str:
        self.calls.append(user)
        if self._fail:
            raise LLMError("boom")
        return f"[{user}]"


def test_clean_chunks_and_joins() -> None:
    provider = _Provider()
    text = "\n".join(["line"] * 10)
    result = CleanupService(provider, max_chars=12).clean(text, _profile(), "m")
    assert len(provider.calls) > 1
    assert "[" in result


def test_clean_empty_returns_empty() -> None:
    provider = _Provider()
    assert CleanupService(provider).clean("", _profile(), "m") == ""
    assert provider.calls == []


def test_clean_propagates_error() -> None:
    with pytest.raises(LLMError):
        CleanupService(_Provider(fail=True)).clean("some text", _profile(), "m")
