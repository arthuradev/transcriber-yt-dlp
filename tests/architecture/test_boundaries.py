"""Architecture boundary tests.

The core layer must remain pure: no imports of adapters, UI, the application
layer, storage, subprocess, or network clients. These tests scan the installed
package source with ``ast`` and fail on any forbidden import.
"""

from __future__ import annotations

import ast
from pathlib import Path

import transcriber

FORBIDDEN_IMPORTS: tuple[str, ...] = (
    "subprocess",
    "requests",
    "httpx",
    "urllib",
    "socket",
    "http.client",
    "transcriber.adapters",
    "transcriber.ui",
    "transcriber.application",
    "transcriber.storage",
)


def _package_dir(name: str) -> Path:
    assert transcriber.__file__ is not None
    return Path(transcriber.__file__).resolve().parent / name


def _core_dir() -> Path:
    return _package_dir("core")


def _imported_modules(tree: ast.Module) -> list[str]:
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None and node.level == 0:
            modules.append(node.module)
    return modules


def test_core_package_exists() -> None:
    assert _core_dir().is_dir()


def test_core_has_no_forbidden_imports() -> None:
    offenders: list[str] = []
    for path in sorted(_core_dir().rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for module in _imported_modules(tree):
            for forbidden in FORBIDDEN_IMPORTS:
                if module == forbidden or module.startswith(f"{forbidden}."):
                    offenders.append(f"{path.name}: {module}")
    assert not offenders, f"core layer imports forbidden modules: {offenders}"


def test_ui_does_not_import_adapters() -> None:
    offenders: list[str] = []
    for path in sorted(_package_dir("ui").rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for module in _imported_modules(tree):
            if module == "transcriber.adapters" or module.startswith("transcriber.adapters."):
                offenders.append(f"{path.name}: {module}")
    assert not offenders, f"ui layer imports adapters directly: {offenders}"


def test_application_does_not_import_ui_or_adapters() -> None:
    forbidden = ("transcriber.ui", "transcriber.adapters")
    offenders: list[str] = []
    for path in sorted(_package_dir("application").rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for module in _imported_modules(tree):
            for prefix in forbidden:
                if module == prefix or module.startswith(f"{prefix}."):
                    offenders.append(f"{path.name}: {module}")
    assert not offenders, f"application layer imports ui/adapters: {offenders}"
