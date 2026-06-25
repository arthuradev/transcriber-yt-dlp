"""PyInstaller entry point for the frozen Windows build.

PyInstaller needs a concrete script. The application's lazy imports mean the
package modules are collected via ``collect_submodules('transcriber')`` in the
spec rather than discovered statically from here.
"""

from __future__ import annotations

from transcriber.__main__ import main

if __name__ == "__main__":
    raise SystemExit(main())
