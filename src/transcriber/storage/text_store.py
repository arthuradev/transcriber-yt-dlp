"""Persist plain text (e.g. cleaned transcripts) to disk."""

from __future__ import annotations

from pathlib import Path


def save_text(text: str, *, output_dir: str, stem: str, ext: str) -> Path:
    """Write ``text`` to ``output_dir/stem<ext>`` and return the path."""
    path = Path(output_dir) / f"{stem}{ext}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path
