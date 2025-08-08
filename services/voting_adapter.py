"""Adapters for weighted voting interactions.

This module wraps the underlying weighted voting implementation and
provides a stable interface for the UI. It prefers the real backend
available in ``superNova_2177`` but falls back to the in-memory
``external_services.fake_api_weighted`` module when the backend is
missing.  Use :func:`register_vote`, :func:`tally_votes`,
:func:`decide_vote`, and :func:`list_votes` rather than importing
backend helpers directly.
"""

from __future__ import annotations

from typing import Any, Dict, List

# Attempt to import the real weighted voting functions; otherwise fallback
try:  # pragma: no cover - best effort import
    from superNova_2177 import (
        vote_weighted as _register_vote,
        tally_proposal_weighted as _tally_votes,
        decide_weighted_api as _decide_vote,
        list_weighted_votes as _list_votes,
    )
except Exception:  # noqa: BLE001 - fall back gracefully
    try:  # pragma: no cover
        from external_services.fake_api_weighted import (
            vote_weighted as _register_vote,
            tally_proposal_weighted as _tally_votes,
            decide_weighted_api as _decide_vote,
            list_weighted_votes as _list_votes,
        )
    except Exception:  # pragma: no cover
        # Final safety net: provide stub implementations so callers do not crash
        def _register_vote(*_: Any, **__: Any) -> Dict[str, Any]:
            return {"ok": False}

        def _tally_votes(*_: Any, **__: Any) -> Dict[str, Any]:
            return {"up": 0.0, "down": 0.0, "total": 0.0}

        def _decide_vote(*_: Any, **__: Any) -> Dict[str, Any]:
            return {
                "proposal_id": 0,
                "status": "rejected",
                "threshold": 0.6,
                "up": 0.0,
                "down": 0.0,
                "total": 0.0,
            }

        def _list_votes(*_: Any, **__: Any) -> List[Dict[str, Any]]:
            return []


def register_vote(
    proposal_id: int,
    voter: str,
    choice: str,
    species: str = "human",
) -> Dict[str, Any]:
    """Record a weighted vote via the configured backend."""

    return _register_vote(proposal_id, voter, choice, species)


def tally_votes(proposal_id: int) -> Dict[str, Any]:
    """Return the weighted tally for ``proposal_id``."""

    return _tally_votes(proposal_id)


def decide_vote(proposal_id: int, level: str = "standard") -> Dict[str, Any]:
    """Compute a decision for ``proposal_id`` at the given ``level``."""

    return _decide_vote(proposal_id, level)


def list_votes(proposal_id: int | None = None) -> List[Dict[str, Any]]:
    """List raw weighted votes, optionally filtered by ``proposal_id``."""

    return _list_votes(proposal_id)
