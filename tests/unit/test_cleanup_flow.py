"""Tests for the interactive cleanup flow."""

from __future__ import annotations

import io
from collections.abc import Sequence
from pathlib import Path

from rich.console import Console

from transcriber.application.cleanup import CleanupService
from transcriber.config.models import Language
from transcriber.core.cleanup import CleanupProfile, LLMError
from transcriber.ui.cleanup_flow import CleanupFlow
from transcriber.ui.i18n import Translator


class _Reader:
    def __init__(self, text: str = "hello") -> None:
        self._text = text

    def read_text(self, path: str) -> str:
        return self._text


class _Provider:
    def __init__(self, *, fail: bool = False) -> None:
        self._fail = fail

    def complete(self, system: str, user: str, model: str) -> str:
        if self._fail:
            raise LLMError("boom")
        return f"CLEANED {user}"


class _Prompts:
    def __init__(
        self, *, file: str = "t.txt", confirm: bool = True, profile_id: str = "readable"
    ) -> None:
        self._file = file
        self._confirm = confirm
        self._profile_id = profile_id

    def ask_file(self) -> str:
        return self._file

    def confirm(self) -> bool:
        return self._confirm

    def select_profile(self, profiles: Sequence[CleanupProfile]) -> CleanupProfile | None:
        return next((p for p in profiles if p.profile_id == self._profile_id), None)


def _flow(
    console: Console,
    *,
    output_dir: str,
    provider: _Provider | None = None,
    prompts: _Prompts | None = None,
    api_key: str | None = "KEY",
    exists: bool = True,
) -> CleanupFlow:
    return CleanupFlow(
        service=CleanupService(provider or _Provider()),
        reader=_Reader(),
        console=console,
        translator=Translator(Language.EN_US),
        output_dir=output_dir,
        model="m",
        api_key=api_key,
        prompts=prompts or _Prompts(),
        path_exists=lambda p: exists,
    )


def test_flow_missing_file(console_buffer: tuple[Console, io.StringIO], tmp_path: Path) -> None:
    console, buffer = console_buffer
    _flow(console, output_dir=str(tmp_path), exists=False).run()
    assert "File not found" in buffer.getvalue()


def test_flow_requires_confirmation(
    console_buffer: tuple[Console, io.StringIO], tmp_path: Path
) -> None:
    console, buffer = console_buffer
    _flow(console, output_dir=str(tmp_path), prompts=_Prompts(confirm=False)).run()
    assert "Cancelled" in buffer.getvalue()


def test_flow_requires_key(console_buffer: tuple[Console, io.StringIO], tmp_path: Path) -> None:
    console, buffer = console_buffer
    _flow(console, output_dir=str(tmp_path), api_key=None).run()
    assert "DEEPSEEK_API_KEY" in buffer.getvalue()


def test_flow_cleans_and_saves(console_buffer: tuple[Console, io.StringIO], tmp_path: Path) -> None:
    console, buffer = console_buffer
    _flow(console, output_dir=str(tmp_path), prompts=_Prompts(file="lecture.txt")).run()
    assert "Cleaned transcript saved" in buffer.getvalue()
    saved = tmp_path / "lecture.clean.txt"
    assert saved.is_file()
    assert "CLEANED" in saved.read_text(encoding="utf-8")


def test_flow_reports_llm_error(
    console_buffer: tuple[Console, io.StringIO], tmp_path: Path
) -> None:
    console, buffer = console_buffer
    _flow(console, output_dir=str(tmp_path), provider=_Provider(fail=True)).run()
    assert "Cleanup failed" in buffer.getvalue()
