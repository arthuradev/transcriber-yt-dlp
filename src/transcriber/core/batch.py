"""Batch URL list parsing.

Pure parsing of a ``.txt`` URL list: one URL per line, blank lines and lines
starting with ``#`` ignored, surrounding whitespace stripped.
"""

from __future__ import annotations


def parse_url_list(text: str) -> list[str]:
    """Parse newline-separated URLs, skipping blanks and ``#`` comments."""
    urls: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        urls.append(line)
    return urls
