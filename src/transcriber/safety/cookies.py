"""Cookie guard.

Cookies from the browser are an advanced, opt-in feature: never auto-enabled,
allowed only when explicitly configured, and confirmed before use. This module
decides whether cookies may be used and which browser. Pure (no I/O).
"""

from __future__ import annotations

from dataclasses import dataclass

from transcriber.config.models import CookiesConfig

_SUPPORTED_BROWSERS = frozenset(
    {"brave", "chrome", "chromium", "edge", "firefox", "opera", "safari", "vivaldi", "whale"}
)

COOKIE_WARNING = (
    "Cookies from your browser will be sent to the target site. This can expose "
    "your logged-in session. Use only on sites you trust."
)


@dataclass(frozen=True)
class CookieDecision:
    """Whether browser cookies may be used, and which browser."""

    allowed: bool
    browser: str | None
    requires_confirmation: bool
    reason: str


def evaluate_cookies(config: CookiesConfig) -> CookieDecision:
    """Decide whether browser cookies may be used given the cookie config."""
    if not config.enabled:
        return CookieDecision(False, None, False, "Cookies are disabled.")
    if not config.allow_browser_cookies:
        return CookieDecision(False, None, False, "Browser cookies are not allowed.")

    browser = (config.browser or "").strip().lower()
    if not browser:
        return CookieDecision(False, None, False, "No browser is configured for cookies.")
    if browser not in _SUPPORTED_BROWSERS:
        return CookieDecision(False, None, False, f"Unsupported cookie browser: {browser}.")

    return CookieDecision(True, browser, config.require_confirmation, COOKIE_WARNING)
