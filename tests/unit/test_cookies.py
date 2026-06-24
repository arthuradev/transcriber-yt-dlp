"""Tests for the cookie guard."""

from __future__ import annotations

from transcriber.config.models import CookiesConfig
from transcriber.safety.cookies import evaluate_cookies


def test_disabled_by_default() -> None:
    decision = evaluate_cookies(CookiesConfig())
    assert not decision.allowed
    assert decision.browser is None


def test_not_allowed_when_browser_cookies_off() -> None:
    decision = evaluate_cookies(
        CookiesConfig(enabled=True, allow_browser_cookies=False, browser="chrome")
    )
    assert not decision.allowed


def test_no_browser_configured() -> None:
    decision = evaluate_cookies(CookiesConfig(enabled=True, browser=None))
    assert not decision.allowed


def test_unsupported_browser() -> None:
    decision = evaluate_cookies(CookiesConfig(enabled=True, browser="netscape"))
    assert not decision.allowed


def test_allowed_with_confirmation() -> None:
    decision = evaluate_cookies(
        CookiesConfig(enabled=True, browser="Chrome", require_confirmation=True)
    )
    assert decision.allowed
    assert decision.browser == "chrome"
    assert decision.requires_confirmation
    assert decision.reason
