"""Project quality gate.

Runs structural and safety checks that complement ruff/pyright/pytest:

1. No secret/private files are present in the working tree.
2. The expected package skeleton exists.
3. The ``core`` layer does not import forbidden modules (adapters, UI, the
   application layer, subprocess, or network clients).

Exits with a non-zero status if any check fails so it can be used in CI.
"""

from __future__ import annotations

import ast
from collections.abc import Iterable
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src" / "transcriber"
CORE_ROOT = SRC_ROOT / "core"

# Glob patterns for files that must never appear in the working tree.
# ``.env.example`` is explicitly allowed and excluded below.
FORBIDDEN_GLOBS: tuple[str, ...] = (
    ".env",
    "config.yaml",
    "*.local.yaml",
    "cookies.txt",
    "*cookies*.txt",
    "*.token",
    "*.key",
)
ALLOWED_FILES: frozenset[str] = frozenset({".env.example"})

# Top-level packages that the architecture requires to exist.
REQUIRED_PACKAGES: tuple[str, ...] = (
    "core",
    "application",
    "ports",
    "adapters",
    "ui",
    "safety",
    "storage",
    "observability",
    "config",
)

# Import prefixes that the core layer must never use.
FORBIDDEN_CORE_IMPORTS: tuple[str, ...] = (
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


def _iter_module_names(tree: ast.Module) -> Iterable[str]:
    """Yield the imported module names found in a parsed module."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom) and node.module is not None and node.level == 0:
            yield node.module


def check_no_secret_files() -> list[str]:
    """Return a list of failures for any secret/private files present."""
    failures: list[str] = []
    for pattern in FORBIDDEN_GLOBS:
        for match in REPO_ROOT.rglob(pattern):
            if match.name in ALLOWED_FILES:
                continue
            if not match.is_file():
                continue
            failures.append(f"forbidden file present: {match.relative_to(REPO_ROOT)}")
    return failures


def check_package_skeleton() -> list[str]:
    """Return a list of failures for any missing required package."""
    failures: list[str] = []
    if not (SRC_ROOT / "__init__.py").is_file():
        failures.append("missing package: src/transcriber/__init__.py")
    for package in REQUIRED_PACKAGES:
        init_file = SRC_ROOT / package / "__init__.py"
        if not init_file.is_file():
            failures.append(f"missing package: src/transcriber/{package}/__init__.py")
    return failures


def check_core_boundaries() -> list[str]:
    """Return a list of failures for forbidden imports inside the core layer."""
    failures: list[str] = []
    if not CORE_ROOT.is_dir():
        return ["missing core layer: src/transcriber/core"]
    for path in sorted(CORE_ROOT.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for module in _iter_module_names(tree):
            for forbidden in FORBIDDEN_CORE_IMPORTS:
                if module == forbidden or module.startswith(f"{forbidden}."):
                    rel = path.relative_to(REPO_ROOT)
                    failures.append(f"core imports forbidden module '{module}' in {rel}")
    return failures


def main() -> int:
    """Run all quality-gate checks and report the result."""
    checks = (
        ("secret files", check_no_secret_files),
        ("package skeleton", check_package_skeleton),
        ("core boundaries", check_core_boundaries),
    )

    all_failures: list[str] = []
    for name, check in checks:
        failures = check()
        status = "PASS" if not failures else "FAIL"
        print(f"[{status}] {name}")
        all_failures.extend(failures)

    if all_failures:
        print("\nQuality gate FAILED:")
        for failure in all_failures:
            print(f"  - {failure}")
        return 1

    print("\nQuality gate passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
