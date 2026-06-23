"""Application layer.

Use-case coordination and workflow orchestration. May depend on ``core`` and
``ports`` only. Must not import concrete external clients/adapters directly.

Phase 4 adds ``FirstRunService`` (first-run detection + setup wizard
orchestration via ports).
"""
