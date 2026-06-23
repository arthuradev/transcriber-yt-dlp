"""Shared pytest fixtures."""

from __future__ import annotations

import io

import pytest
from rich.console import Console

from transcriber.ui.theme import DEFAULT_THEME


@pytest.fixture
def console_buffer() -> tuple[Console, io.StringIO]:
    """A non-terminal Rich console writing to an in-memory buffer.

    Mirrors the production console (same theme) so named styles resolve, but
    because the buffer is not a TTY ``is_terminal`` is ``False``: the startup
    animation is skipped and the shell never blocks on input.
    """
    buffer = io.StringIO()
    console = Console(file=buffer, width=100, theme=DEFAULT_THEME)
    return console, buffer
