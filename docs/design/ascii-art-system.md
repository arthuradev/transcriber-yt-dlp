# ASCII Art System

## Purpose
ASCII art is used as a delightful visual reward after successful operations and optionally on welcome.

## Asset rules
- Store art in UTF-8 `.txt` files.
- Preserve leading spaces.
- Do not wrap.
- Do not trim lines when rendering.
- Measure terminal width before rendering.
- Center only if safe.
- Fallback to compact success message when too narrow.

## Directories
```text
assets/ascii/welcome/
assets/ascii/success/
assets/ascii/custom/
```

## Config
See `configs/ascii.example.yaml`.

## Initial assets
The project may include the four user-provided ASCII art files under welcome/success. If future copyright/license concerns arise, remove them and keep the renderer/custom folder system.
