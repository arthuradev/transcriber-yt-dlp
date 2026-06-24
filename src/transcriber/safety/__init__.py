"""Safety layer.

Owns risk classification, dry-run building, confirmation gating, cookie guard,
secrets guard, path guard, audit events, and rollback modeling.

Phase 7 adds ``risk`` (download risk classification). Depends only on ``core``.
"""
