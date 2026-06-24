"""Tests for cleanup profiles, prompt, and chunking."""

from __future__ import annotations

from transcriber.core.cleanup import (
    CLEANUP_PROFILES,
    PROMPT_CONTRACT,
    chunk_text,
    cleanup_profiles,
    get_cleanup_profile,
    system_prompt,
)


def test_all_profiles_present() -> None:
    assert set(CLEANUP_PROFILES) == {
        "readable",
        "study_notes",
        "article",
        "subtitle_cleanup",
        "verbatim_clean",
    }
    assert len(cleanup_profiles()) == 5


def test_get_profile() -> None:
    assert get_cleanup_profile("readable") is not None
    assert get_cleanup_profile("nope") is None


def test_system_prompt_includes_contract_and_style() -> None:
    profile = get_cleanup_profile("readable")
    assert profile is not None
    prompt = system_prompt(profile)
    assert PROMPT_CONTRACT in prompt
    assert profile.instruction in prompt
    assert "Do not add information" in prompt


def test_chunk_text_empty() -> None:
    assert chunk_text("") == []
    assert chunk_text("\n\n") == []


def test_chunk_text_small_returns_single() -> None:
    assert chunk_text("hello world", 100) == ["hello world"]


def test_chunk_text_splits_on_lines() -> None:
    text = "\n".join(["line"] * 10)
    chunks = chunk_text(text, max_chars=12)
    assert len(chunks) > 1
    assert "".join(chunks).replace("\n", "") == "line" * 10


def test_chunk_text_hard_splits_long_line() -> None:
    chunks = chunk_text("a" * 25, max_chars=10)
    assert all(len(chunk) <= 10 for chunk in chunks)
    assert "".join(chunks) == "a" * 25
