"""Application entry point.

Launches the TUI shell (startup banner, animation, and main menu). Menu actions
are placeholders until later phases wire the real download/transcription/cleanup
use cases.
"""

from __future__ import annotations


def main() -> int:
    """Run the application. Returns a process exit code."""
    from transcriber.ui.shell import AppShell

    return AppShell().run()


if __name__ == "__main__":
    raise SystemExit(main())
