"""Architecture boundary tests.

Strict, data-driven enforcement of the layered dependency rules: each layer may
only depend inward. Source is scanned with ``ast`` and any forbidden import
fails the build.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

import transcriber

# For each layer, the import prefixes it must NOT use.
LAYER_FORBIDDEN: dict[str, tuple[str, ...]] = {
    "core": (
        "transcriber.adapters",
        "transcriber.ui",
        "transcriber.application",
        "transcriber.storage",
        "transcriber.observability",
        "transcriber.safety",
        "transcriber.ports",
        "transcriber.config",
        "subprocess",
        "requests",
        "httpx",
        "urllib",
        "socket",
        "http.client",
    ),
    "ports": (
        "transcriber.adapters",
        "transcriber.ui",
        "transcriber.application",
        "transcriber.storage",
        "transcriber.observability",
        "transcriber.safety",
    ),
    "safety": (
        "transcriber.adapters",
        "transcriber.ui",
        "transcriber.application",
        "transcriber.storage",
        "transcriber.observability",
        "transcriber.ports",
    ),
    "application": (
        "transcriber.adapters",
        "transcriber.ui",
        "transcriber.storage",
        "transcriber.observability",
    ),
    "adapters": (
        "transcriber.ui",
        "transcriber.application",
        "transcriber.storage",
        "transcriber.observability",
    ),
    "storage": (
        "transcriber.ui",
        "transcriber.application",
        "transcriber.adapters",
        "transcriber.observability",
    ),
    "observability": (
        "transcriber.ui",
        "transcriber.application",
        "transcriber.adapters",
    ),
    "ui": ("transcriber.adapters",),
}


def _package_dir(name: str) -> Path:
    assert transcriber.__file__ is not None
    return Path(transcriber.__file__).resolve().parent / name


def _imported_modules(tree: ast.Module) -> list[str]:
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None and node.level == 0:
            modules.append(node.module)
    return modules


def _violations(layer: str, forbidden: tuple[str, ...]) -> list[str]:
    offenders: list[str] = []
    for path in sorted(_package_dir(layer).rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for module in _imported_modules(tree):
            for prefix in forbidden:
                if module == prefix or module.startswith(f"{prefix}."):
                    offenders.append(f"{layer}/{path.name}: imports {module}")
    return offenders


def test_all_layers_exist() -> None:
    for layer in LAYER_FORBIDDEN:
        assert _package_dir(layer).is_dir(), f"missing layer: {layer}"


@pytest.mark.parametrize("layer", list(LAYER_FORBIDDEN))
def test_layer_import_boundaries(layer: str) -> None:
    offenders = _violations(layer, LAYER_FORBIDDEN[layer])
    assert not offenders, f"forbidden imports in {layer}: {offenders}"
