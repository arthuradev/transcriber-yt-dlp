"""Application entry point.

Launches the TUI shell (startup banner, animation, and main menu). Download
menu actions run the planning/dry-run flow (no execution yet); other actions are
placeholders until later phases.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rich.console import Console

    from transcriber.config.models import UserConfig
    from transcriber.ui.i18n import Translator
    from transcriber.ui.menu import MenuAction


def _build_weather_line_provider(
    config: UserConfig, translator: Translator
) -> Callable[[], str | None] | None:
    """Build a cached weather-line provider, or ``None`` when weather is off."""
    if not (config.weather.enabled and config.weather.show_on_startup):
        return None

    from transcriber.config.secrets import weather_api_key
    from transcriber.ui.weather import render_weather_line

    key = weather_api_key()
    if not key:
        return lambda: render_weather_line(None, translator)

    from transcriber.adapters.weatherapi import WeatherApiAdapter
    from transcriber.application.weather import WeatherService

    service = WeatherService(WeatherApiAdapter(key), cache_minutes=config.weather.cache_minutes)
    query = config.weather.query
    units = config.weather.units
    return lambda: render_weather_line(service.get(query, units), translator)


def _build_action_handler(
    console: Console, config: UserConfig, translator: Translator
) -> Callable[[MenuAction], bool]:
    """Build the menu-action handler routing download actions to the dry-run flow."""
    from transcriber.adapters.faster_whisper_engine import FasterWhisperEngine
    from transcriber.adapters.local_files import LocalTextFileReader
    from transcriber.adapters.yt_dlp_engine import YtDlpEngine
    from transcriber.application.batch import BatchProbeService
    from transcriber.application.executor import DownloadExecutor
    from transcriber.application.planner import DownloadPlanner
    from transcriber.application.probe import MediaProbeService
    from transcriber.application.subtitles import SubtitleService
    from transcriber.application.transcription import TranscriptionService
    from transcriber.storage.archive import FileDownloadArchive, default_archive_path
    from transcriber.ui.ascii_art import choose_art, load_art_dir, locate_ascii_dir
    from transcriber.ui.download_flow import DownloadFlow, QuestionaryDownloadFlowPrompts
    from transcriber.ui.menu import MenuAction
    from transcriber.ui.subtitle_flow import QuestionarySubtitleFlowPrompts, SubtitleFlow
    from transcriber.ui.transcribe_flow import QuestionaryTranscribeFlowPrompts, TranscribeFlow

    categories: dict[MenuAction, str] = {
        MenuAction.DOWNLOAD_VIDEO: "video",
        MenuAction.DOWNLOAD_AUDIO: "audio",
    }
    engine = YtDlpEngine()
    archive = FileDownloadArchive(default_archive_path())
    probe_service = MediaProbeService(engine)
    executor = DownloadExecutor(engine, archive=archive)
    planner = DownloadPlanner(archive=archive)
    batch_service = BatchProbeService(engine, LocalTextFileReader())
    prompts = QuestionaryDownloadFlowPrompts(translator)
    transcription_service = TranscriptionService(FasterWhisperEngine())
    transcribe_prompts = QuestionaryTranscribeFlowPrompts(translator)
    subtitle_service = SubtitleService(engine)
    subtitle_prompts = QuestionarySubtitleFlowPrompts(translator)
    success_dir = locate_ascii_dir("success")
    success_art = choose_art(load_art_dir(success_dir)) if success_dir is not None else None

    def handle(action: MenuAction) -> bool:
        if action is MenuAction.TRANSCRIBE_LOCAL:
            TranscribeFlow(
                service=transcription_service,
                console=console,
                translator=translator,
                config=config.transcription,
                output_dir=config.paths.download_dir,
                prompts=transcribe_prompts,
            ).run()
            return True

        if action is MenuAction.DOWNLOAD_TRANSCRIPT:
            SubtitleFlow(
                probe_service=probe_service,
                subtitle_service=subtitle_service,
                console=console,
                translator=translator,
                paths=config.paths,
                subtitle_format=config.subtitles.format,
                prompts=subtitle_prompts,
            ).run()
            return True

        category = categories.get(action)
        if category is None:
            return False
        DownloadFlow(
            probe_service=probe_service,
            planner=planner,
            console=console,
            translator=translator,
            paths=config.paths,
            prompts=prompts,
            executor=executor,
            batch_service=batch_service,
            success_art=success_art,
        ).run(category)
        return True

    return handle


def main() -> int:
    """Run the application. Returns a process exit code."""
    from transcriber.application.first_run import FirstRunService
    from transcriber.storage.config_store import ConfigStore, default_config_path
    from transcriber.ui.ascii_art import choose_art, load_art_dir, locate_ascii_dir
    from transcriber.ui.console import build_console
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
    console = build_console(config.ui.theme)
    welcome_dir = locate_ascii_dir("welcome")
    welcome_art = choose_art(load_art_dir(welcome_dir)) if welcome_dir is not None else None
    return AppShell(
        console=console,
        translator=translator,
        welcome_art=welcome_art,
        weather_line_provider=_build_weather_line_provider(config, translator),
        action_handler=_build_action_handler(console, config, translator),
    ).run()


if __name__ == "__main__":
    raise SystemExit(main())
