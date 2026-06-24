"""Tests for output path planning."""

from __future__ import annotations

from datetime import date

from transcriber.core.paths import plan_output_path, sanitize_filename


def test_sanitize_replaces_illegal_chars() -> None:
    assert sanitize_filename("a/b:c*d") == "a_b_c_d"


def test_sanitize_empty_becomes_untitled() -> None:
    assert sanitize_filename("   ") == "untitled"
    assert sanitize_filename("...") == "untitled"


def test_sanitize_collapses_whitespace() -> None:
    assert sanitize_filename("a   b  c") == "a b c"


def test_plan_path_full() -> None:
    path = plan_output_path(
        output_dir="out",
        extractor="Youtube",
        media_id="abc",
        title="My Video",
        ext="mp4",
        organize_by_site=True,
        organize_by_date=True,
        include_media_id=True,
        today=date(2026, 6, 24),
    )
    assert path == "out/Youtube/2026-06-24/My Video [abc].mp4"


def test_plan_path_minimal() -> None:
    path = plan_output_path(
        output_dir="d",
        extractor="Y",
        media_id="id",
        title="T",
        ext="mp3",
        organize_by_site=False,
        organize_by_date=False,
        include_media_id=False,
        today=date(2026, 6, 24),
    )
    assert path == "d/T.mp3"
