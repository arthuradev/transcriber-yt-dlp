"""ASCII art loading, measurement, and rendering.

Art is stored in UTF-8 ``.txt`` files. Lines are preserved exactly (leading
spaces kept, never trimmed, never wrapped). Display width is measured in
terminal cells so Unicode art (e.g. braille blocks) is sized correctly.
"""

from __future__ import annotations

import random
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from rich.cells import cell_len
from rich.console import Console


@dataclass(frozen=True)
class AsciiArt:
    """A piece of ASCII/Unicode art and its measured dimensions."""

    name: str
    lines: tuple[str, ...]

    @property
    def width(self) -> int:
        """Maximum display width across all lines, in terminal cells."""
        return max((cell_len(line) for line in self.lines), default=0)

    @property
    def height(self) -> int:
        """Number of lines."""
        return len(self.lines)


def load_art(path: Path) -> AsciiArt:
    """Load a single art file. A trailing final newline is ignored."""
    lines = path.read_text(encoding="utf-8").split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    return AsciiArt(name=path.stem, lines=tuple(lines))


def load_art_dir(directory: Path) -> list[AsciiArt]:
    """Load every ``*.txt`` art file in ``directory`` (empty list if missing)."""
    if not directory.is_dir():
        return []
    return [load_art(path) for path in sorted(directory.glob("*.txt"))]


def locate_ascii_dir(category: str) -> Path | None:
    """Find ``assets/ascii/<category>`` from the bundle, cwd, or package tree.

    In a PyInstaller build, assets are extracted under ``sys._MEIPASS``. Returns
    ``None`` if the directory cannot be found.
    """
    candidates: list[Path] = []
    bundle_dir = getattr(sys, "_MEIPASS", None)
    if bundle_dir:
        candidates.append(Path(bundle_dir) / "assets" / "ascii" / category)
    candidates.append(Path.cwd() / "assets" / "ascii" / category)
    package_dir = Path(__file__).resolve().parent
    candidates.extend(parent / "assets" / "ascii" / category for parent in package_dir.parents)
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return None


def fits(art: AsciiArt, available_width: int, *, min_width: int = 0) -> bool:
    """Whether ``art`` can be shown given the available width and a floor."""
    if available_width < min_width:
        return False
    return art.width <= available_width


def choose_art(arts: Sequence[AsciiArt], *, rng: random.Random | None = None) -> AsciiArt | None:
    """Pick one art at random, or ``None`` if there are none."""
    if not arts:
        return None
    chooser = rng if rng is not None else random.Random()
    return chooser.choice(list(arts))


def render_art(console: Console, art: AsciiArt, *, center: bool = True) -> None:
    """Render ``art`` to ``console`` without wrapping or cropping.

    Centered horizontally when it fits and ``center`` is set; otherwise printed
    flush left. Content is printed literally (no markup/highlight) to preserve
    the raw art.
    """
    if center and art.width < console.width:
        prefix = " " * ((console.width - art.width) // 2)
        body = "\n".join(prefix + line for line in art.lines)
    else:
        body = "\n".join(art.lines)
    console.print(body, markup=False, highlight=False, soft_wrap=True)
