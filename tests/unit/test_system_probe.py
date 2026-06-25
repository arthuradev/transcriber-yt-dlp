"""Tests for the local system probe (must not crash; returns booleans)."""

from __future__ import annotations

from transcriber.adapters.system import LocalSystemProbe


def test_probe_methods_return_booleans() -> None:
    probe = LocalSystemProbe()
    assert isinstance(probe.is_windows(), bool)
    assert isinstance(probe.has_ffmpeg(), bool)
    assert isinstance(probe.gpu_available(), bool)
