"""Output path planning policy.

Pure functions that compute where a download would be written. No filesystem
access; the current date is injected for deterministic planning.
"""

from __future__ import annotations

import re
from datetime import date

_ILLEGAL = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_WHITESPACE = re.compile(r"\s+")


def sanitize_filename(name: str, *, max_length: int = 120) -> str:
    """Make ``name`` safe to use as a Windows filename component."""
    cleaned = _ILLEGAL.sub("_", name)
    cleaned = _WHITESPACE.sub(" ", cleaned).strip().strip(".").strip()
    if not cleaned:
        return "untitled"
    return cleaned[:max_length].strip()


def plan_output_path(
    *,
    output_dir: str,
    extractor: str,
    media_id: str,
    title: str,
    ext: str,
    organize_by_site: bool,
    organize_by_date: bool,
    include_media_id: bool,
    today: date,
) -> str:
    """Compute the planned output path (forward-slash separated) for one item."""
    parts: list[str] = [output_dir.rstrip("/\\") or "."]
    if organize_by_site and extractor:
        parts.append(sanitize_filename(extractor, max_length=40))
    if organize_by_date:
        parts.append(today.isoformat())

    stem = sanitize_filename(title or media_id or "untitled")
    if include_media_id and media_id:
        stem = f"{stem} [{media_id}]"
    parts.append(f"{stem}.{ext}")
    return "/".join(parts)
