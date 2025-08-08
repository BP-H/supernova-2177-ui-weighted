"""Validator service adapters with safe fallbacks.

This module exposes lightweight wrappers around backend validator features. When
backend modules are unavailable, in-memory no-ops are provided so that calling
code can continue operating without errors.
"""
from __future__ import annotations

from typing import Any, Dict, List


def run_validations(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Run the validator cycle if the backend is available.

    Parameters
    ----------
    payload:
        Data forwarded to the backend implementation. Currently unused by the
        fallback stub.

    Returns
    -------
    dict
        A dictionary containing an ``available`` flag and the raw result from
        :func:`run_validation_cycle` when it could be executed.
    """
    try:
        from superNova_2177 import run_validation_cycle
    except Exception:
        return {"available": False, "result": {}}

    try:
        result = run_validation_cycle(**payload)
    except Exception:
        # Some implementations accept no arguments.
        result = run_validation_cycle()
    return {"available": True, "result": result}


def compute_reputations(
    validations: List[Dict[str, Any]],
    consensus: Dict[str, float],
) -> Dict[str, Any]:
    """Compute validator reputations through the backend when available.

    Parameters
    ----------
    validations:
        List of validation records.
    consensus:
        Consensus scores keyed by hypothesis identifier.

    Returns
    -------
    dict
        Result from :func:`compute_validator_reputations` with an ``available``
        flag. A stub response is returned when the backend is missing.
    """
    try:
        from validators.reputation_influence_tracker import (
            compute_validator_reputations,
        )
    except Exception:
        return {
            "available": False,
            "validator_reputations": {},
            "flags": ["backend_unavailable"],
            "stats": {"total_validators": 0, "avg_reputation": 0.0},
        }

    result = compute_validator_reputations(validations, consensus)
    result["available"] = True
    return result


def aggregate_votes(
    votes: List[Dict[str, Any]],
    method: str | None = None,
) -> Dict[str, Any]:
    """Aggregate validator votes using the backend consensus engine.

    Parameters
    ----------
    votes:
        Vote dictionaries from individual validators.
    method:
        Name of the aggregation method to use. Defaults to the backend's
        reputation-weighted method.

    Returns
    -------
    dict
        Result from :func:`aggregate_validator_votes` with an ``available``
        flag. A stub result is returned when the backend is missing.
    """
    try:
        from validators.strategies.voting_consensus_engine import (
            VotingMethod,
            aggregate_validator_votes,
        )
    except Exception:
        return {
            "available": False,
            "consensus_decision": "no_consensus",
            "consensus_confidence": 0.0,
            "voting_method": method or "unknown",
            "vote_breakdown": {},
            "flags": ["backend_unavailable"],
            "quorum_met": False,
        }

    try:
        voting_method = (
            VotingMethod(method) if method else VotingMethod.REPUTATION_WEIGHTED
        )
    except ValueError:
        voting_method = VotingMethod.REPUTATION_WEIGHTED

    result = aggregate_validator_votes(votes, method=voting_method)
    result["available"] = True
    return result
