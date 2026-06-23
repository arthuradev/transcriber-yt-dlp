"""Application entry point.

Phase 1 ships only the project skeleton. No functional behavior is wired yet;
this entry point exists so the package is runnable and importable.
"""

from __future__ import annotations

from transcriber import __version__


def main() -> int:
    """Run the application.

    Returns a process exit code. Phase 1 is a non-functional skeleton.
    """
    print(f"Transcriber v{__version__} - skeleton (Phase 1). No operations are wired yet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
