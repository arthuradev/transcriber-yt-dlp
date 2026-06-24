"""Tests for redaction helpers."""

from __future__ import annotations

from transcriber.safety.redaction import redact, redact_secrets, redact_url_tokens


def test_redact_secrets() -> None:
    assert redact_secrets("key is SECRET here", ["SECRET"]) == "key is *** here"
    assert redact_secrets("nothing", [""]) == "nothing"


def test_redact_url_tokens() -> None:
    output = redact_url_tokens("https://x/y?token=abc123&q=1")
    assert "abc123" not in output
    assert "token=***" in output
    assert "q=1" in output


def test_redact_combined() -> None:
    output = redact("https://x?api_key=KEYVAL&user=SECRETUSER", secrets=["SECRETUSER"])
    assert "KEYVAL" not in output
    assert "SECRETUSER" not in output
