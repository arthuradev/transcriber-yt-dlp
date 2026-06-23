"""Application entry point.

Launches the TUI shell (startup banner, animation, and main menu). Menu actions
are placeholders until later phases wire the real download/transcription/cleanup
use cases.
"""

from __future__ import annotations


def main() -> int:
    """Run the application. Returns a process exit code."""
    from transcriber.application.first_run import FirstRunService
    from transcriber.storage.config_store import ConfigStore, default_config_path
    from transcriber.ui.ascii_art import choose_art, load_art_dir, locate_ascii_dir
    from transcriber.ui.first_run_prompts import QuestionaryFirstRunPrompts
    from transcriber.ui.i18n import Translator
    from transcriber.ui.shell import AppShell
    from transcriber.ui.theme import available_themes

    store = ConfigStore(default_config_path())
    first_run = FirstRunService(store)
    if first_run.is_first_run():
        config = first_run.setup(QuestionaryFirstRunPrompts(), themes=available_themes())
    else:
        config = store.load()

    translator = Translator(config.language)
    welcome_dir = locate_ascii_dir("welcome")
    welcome_art = choose_art(load_art_dir(welcome_dir)) if welcome_dir is not None else None
    return AppShell(
        theme_name=config.ui.theme,
        translator=translator,
        welcome_art=welcome_art,
    ).run()


if __name__ == "__main__":
    raise SystemExit(main())
