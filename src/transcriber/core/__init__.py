"""Core domain layer.

Pure domain concepts only. This package must not import UI, adapters, the
application layer, subprocess, or network clients, and must not perform
filesystem mutation. External systems depend inward on the core, never the
other way around.
"""
