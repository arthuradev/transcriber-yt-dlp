"""UI layer.

Presentation and user interaction only (Rich, Questionary, Pyfiglet). Must not
contain business rules, safety decisions, or direct side effects on external
systems.

Phase 2 provides the TUI shell: console/theme, startup banner, animation, and
the main-menu loop. Phase 3 adds the dark theme registry, the ASCII art renderer
with terminal-width fit checks, and the clean-screen success flow. Menu actions
remain placeholders until later phases.
"""
