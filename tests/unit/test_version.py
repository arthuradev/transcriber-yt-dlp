"""Smoke test for the package version."""

from __future__ import annotations

import transcriber


def test_version_is_phase_one() -> None:
    assert transcriber.__version__ == "0.1.0"
