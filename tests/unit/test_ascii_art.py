"""Tests for the ASCII art loader and renderer."""

from __future__ import annotations

import io
import random
import sys
from pathlib import Path

import pytest
from rich.console import Console

from transcriber.ui.ascii_art import (
    AsciiArt,
    choose_art,
    fits,
    load_art,
    load_art_dir,
    locate_ascii_dir,
    render_art,
)


def _art(lines: list[str]) -> AsciiArt:
    return AsciiArt(name="t", lines=tuple(lines))


def test_width_is_max_cell_width() -> None:
    art = _art(["abc", "ab", ""])
    assert art.width == 3
    assert art.height == 3


def test_load_art_drops_trailing_newline(tmp_path: Path) -> None:
    file = tmp_path / "hello.txt"
    file.write_text("line1\nline2\n", encoding="utf-8")
    art = load_art(file)
    assert art.name == "hello"
    assert art.lines == ("line1", "line2")


def test_load_art_dir_missing_returns_empty(tmp_path: Path) -> None:
    assert load_art_dir(tmp_path / "nope") == []


def test_fits_respects_width_and_minimum() -> None:
    art = _art(["####"])  # width 4
    assert fits(art, 10)
    assert not fits(art, 3)
    assert not fits(art, 10, min_width=20)


def test_choose_art_returns_none_when_empty() -> None:
    assert choose_art([]) is None


def test_choose_art_is_deterministic_with_seeded_rng() -> None:
    arts = [_art(["a"]), _art(["b"]), _art(["c"])]
    chosen = choose_art(arts, rng=random.Random(0))
    assert chosen in arts


def test_render_art_preserves_lines(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer
    render_art(console, _art(["XX", "YY"]), center=False)
    output = buffer.getvalue()
    assert "XX" in output
    assert "YY" in output


def test_render_art_centers_when_it_fits(console_buffer: tuple[Console, io.StringIO]) -> None:
    console, buffer = console_buffer  # width 100
    render_art(console, _art(["ABCD"]), center=True)
    first_line = buffer.getvalue().splitlines()[0]
    assert first_line.startswith(" ")
    assert first_line.rstrip() == " " * ((100 - 4) // 2) + "ABCD"


def test_bundled_welcome_art_loads() -> None:
    directory = locate_ascii_dir("welcome")
    assert directory is not None
    arts = load_art_dir(directory)
    assert arts
    assert all(art.width > 0 for art in arts)


def test_locate_ascii_dir_uses_meipass(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    bundle = tmp_path / "bundle"
    (bundle / "assets" / "ascii" / "welcome").mkdir(parents=True)
    monkeypatch.setattr(sys, "_MEIPASS", str(bundle), raising=False)
    found = locate_ascii_dir("welcome")
    assert found == bundle / "assets" / "ascii" / "welcome"
