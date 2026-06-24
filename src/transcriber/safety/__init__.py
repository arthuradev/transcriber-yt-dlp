"""Safety layer.

Owns risk classification, dry-run building, confirmation gating, cookie guard,
secrets guard, path guard, audit events, and rollback modeling.

Phase 7 adds ``risk`` (download risk classification); Phase 14 adds ``cookies``
(cookie guard), ``redaction`` (secret/URL-token redaction), and ``audit`` (audit
events).
"""
