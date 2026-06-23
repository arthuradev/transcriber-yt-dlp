"""Application entry point.

Launches the TUI shell (startup banner, animation, and main menu). Menu actions
are placeholders until later phases wire the real download/transcription/cleanup
use cases.
"""

from __future__ import annotations


def main() -> int:
    """Run the application. Returns a process exit code."""
    from transcriber.ui.ascii_art import choose_art, load_art_dir, locate_ascii_dir
    from transcriber.ui.shell import AppShell

    welcome_dir = locate_ascii_dir("welcome")
    welcome_art = choose_art(load_art_dir(welcome_dir)) if welcome_dir is not None else None
    return AppShell(welcome_art=welcome_art).run()


if __name__ == "__main__":
    raise SystemExit(main())
