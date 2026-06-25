# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for Transcriber (portable Windows console exe).
#
# Build:  uv sync --extra build
#         uv run pyinstaller Transcriber.spec --noconfirm
#
# The package uses lazy imports, so the whole `transcriber` package is collected
# explicitly. Bundles assets/ascii. Does NOT bundle .env, config, history, logs,
# downloads, or any user data.

from PyInstaller.utils.hooks import collect_submodules

hidden_imports = (
    collect_submodules("transcriber")
    + collect_submodules("yt_dlp")
    + [
        "rich",
        "questionary",
        "pyfiglet",
        "pydantic",
        "pydantic_core",
        "yaml",
    ]
)

a = Analysis(
    ["scripts/pyi_entry.py"],
    pathex=["src"],
    binaries=[],
    datas=[("assets/ascii", "assets/ascii")],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["faster_whisper", "ctranslate2", "torch", "pyinstaller"],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="Transcriber",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
