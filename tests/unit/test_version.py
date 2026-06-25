"""Version smoke tests and release-consistency check."""

from __future__ import annotations

import tomllib
from pathlib import Path

import transcriber


def test_version() -> None:
    assert transcriber.__version__ == "0.20.0"


def test_version_matches_pyproject() -> None:
    assert transcriber.__file__ is not None
    repo_root = Path(transcriber.__file__).resolve().parent.parent.parent
    pyproject = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["version"] == transcriber.__version__
