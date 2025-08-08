"""Validator adapters (conflict-free unified version)

Exposes a stable, UI-friendly API with graceful fallbacks:

  - run_validations(payload) -> {"available": bool, "passed": bool, "details": Any}
  - compute_reputations(validations, consensus) -> {"available": bool, "validator_reputations": dict, "flags": list, "stats": dict}
  - aggregate_votes(votes, method=None) -> {"available": bool, "consensus_decision": str, "consensus_confidence": float, "voting_method": str, "vote_breakdown": dict, "quorum_met": bool, "flags": list}

Resolution order:
  1) In-process functions from superNova_2177 / validators.* if present (when USE_REAL_BACKEND=1).
  2) HTTP endpoints when USE_REAL_BACKEND=1.
  3) Safe stubs (local/demo).
"""
from __future__ import annotations

import os
from typing import Any, Dict, List

# Env toggles
USE_REAL_BACKEND = os.getenv("USE_REAL_BACKEND", "0").lower() in {"1", "true", "yes"}
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Optional in-process backend
try:  # pragma: no cover - optional import
    import superNova_2177 as sn_mod  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
    sn_mod = None  # type: ignore[assignment]


def _http_post(path: str, json_payload: Dict[str, Any], timeout: int = 10) -> Dict[str, Any]:
    """POST helper that degrades gracefully if requests is missing."""
    try:
        import requests  # local import to avoid hard dependency at import time
        resp = requests.post(f"{BACKEND_URL}{path}", json=json_payload, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:  # pragma: no cover
        return {"__error__": str(exc)}


def _http_get(path: str, params: Dict[str, Any] | None = None, timeout: int = 10) -> Dict[str, Any]:
    """GET helper that degrades gracefully if requests is missing."""
    try:
        import requests  # local import
        resp = requests.get(f"{BACKEND_URL}{path}", params=params or {}, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:  # pragma: no cover
        return {"__error__": str(exc)}


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def run_validations(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Run validation integrity analysis on `payload`."""
    # 1) In-process functions
    if USE_REAL_BACKEND and sn_mod:
        # Prefer a precise analyzer if present
        if hasattr(sn_mod, "analyze_validation_integrity"):
            try:
                res = getattr(sn_mod, "analyze_validation_integrity")(payload)
                passed = bool(res.get("passed") or res.get("valid"))
                return {"available": True, "passed": passed, "details": res}
            except Exception as exc:  # pragma: no cover
                return {"available": False, "passed": False, "details": str(exc)}
        # Fallback to a generic cycle if present
        if hasattr(sn_mod, "run_validation_cycle"):
            try:
                try:
                    res = getattr(sn_mod, "run_validation_cycle")(**payload)
                except TypeError:
                    res = getattr(sn_mod, "run_validation_cycle")()
                # Best-effort pass flag
                passed = bool(
                    (isinstance(res, dict) and (res.get("passed") or res.get("valid")))
                    or False
                )
                return {"available": True, "passed": passed, "details": res}
            except Exception as exc:  # pragma: no cover
                return {"available": False, "passed": False, "details": str(exc)}

    # 2) HTTP backend
    if USE_REAL_BACKEND:
        data = _http_post("/validate", payload)
        if "__error__" not in data:
            passed = bool(data.get("passed") or data.get("valid"))
            return {"available": True, "passed": passed, "details": data}
        return {"available": False, "passed": False, "details": data["__error__"]}

    # 3) Stub
    return {"available": False, "passed": False, "details": "backend disabled"}


def compute_reputations(
    validations: List[Dict[str, Any]],
    consensus: Dict[str, float],
) -> Dict[str, Any]:
    """Compute validator reputations (backend if available, else stub)."""
    # 1) In-process validators module
    try:
        if USE_REAL_BACKEND:
            from validators.reputation_influence_tracker import (  # type: ignore
                compute_validator_reputations as _core_compute,
            )
            res = _core_compute(validations, consensus)
            if isinstance(res, dict):
                res["available"] = True
                # Ensure keys exist for UI stability
                res.setdefault("validator_reputations", {})
                res.setdefault("flags", [])
                res.setdefault("stats", {"total_validators": 0, "avg_reputation": 0.0})
                return res
    except Exception as exc:  # pragma: no cover
        return {
            "available": False,
            "validator_reputations": {},
            "flags": [f"backend_error:{exc}"],
            "stats": {"total_validators": 0, "avg_reputation": 0.0},
        }

    # 2) HTTP backend (best-effort)
    if USE_REAL_BACKEND:
        data = _http_post("/validators/reputations", {"validations": validations, "consensus": consensus})
        if "__error__" not in data:
            data.setdefault("validator_reputations", {})
            data.setdefault("flags", [])
            data.setdefault("stats", {"total_validators": 0, "avg_reputation": 0.0})
            data["available"] = True
            return data
        return {
            "available": False,
            "validator_reputations": {},
            "flags": [f"http_error:{data['__error__']}"],
            "stats": {"total_validators": 0, "avg_reputation": 0.0},
        }

    # 3) Stub
    return {
        "available": False,
        "validator_reputations": {},
        "flags": ["backend_unavailable"],
        "stats": {"total_validators": 0, "avg_reputation": 0.0},
    }


def aggregate_votes(
    votes: List[Dict[str, Any]],
    method: str | None = None,
) -> Dict[str, Any]:
    """Aggregate validator votes into a consensus result."""
    # 1) In-process consensus engine
    try:
        if USE_REAL_BACKEND:
            from validators.strategies.voting_consensus_engine import (  # type: ignore
                VotingMethod,
                aggregate_validator_votes as _core_aggregate,
            )
            try:
                vm = VotingMethod(method) if method else VotingMethod.REPUTATION_WEIGHTED
            except Exception:
                vm = VotingMethod.REPUTATION_WEIGHTED
            res = _core_aggregate(votes, method=vm)
            if isinstance(res, dict):
                res["available"] = True
                res.setdefault("consensus_decision", "no_consensus")
                res.setdefault("consensus_confidence", 0.0)
                res.setdefault("voting_method", (method or "reputation_weighted"))
                res.setdefault("vote_breakdown", {})
                res.setdefault("quorum_met", False)
                res.setdefault("flags", [])
                return res
    except Exception as exc:  # pragma: no cover
        return {
            "available": False,
            "consensus_decision": "no_consensus",
            "consensus_confidence": 0.0,
            "voting_method": method or "unknown",
            "vote_breakdown": {},
            "quorum_met": False,
            "flags": [f"backend_error:{exc}"],
        }

    # 2) HTTP backend (best-effort)
    if USE_REAL_BACKEND:
        data = _http_post("/validators/aggregate", {"votes": votes, "method": method})
        if "__error__" not in data:
            data.setdefault("consensus_decision", "no_consensus")
            data.setdefault("consensus_confidence", 0.0)
            data.setdefault("voting_method", method or "unknown")
            data.setdefault("vote_breakdown", {})
            data.setdefault("quorum_met", False)
            data.setdefault("flags", [])
            data["available"] = True
            return data
        return {
            "available": False,
            "consensus_decision": "no_consensus",
            "consensus_confidence": 0.0,
            "voting_method": method or "unknown",
            "vote_breakdown": {},
            "quorum_met": False,
            "flags": [f"http_error:{data['__error__']}"],
        }

    # 3) Stub
    return {
        "available": False,
        "consensus_decision": "no_consensus",
        "consensus_confidence": 0.0,
        "voting_method": method or "unknown",
        "vote_breakdown": {},
        "quorum_met": False,
        "flags": ["backend_unavailable"],
    }


__all__ = ["run_validations", "compute_reputations", "aggregate_votes"]
