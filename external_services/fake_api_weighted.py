# external_services/fake_api_weighted.py
# In-memory weighted voting API (humans / companies / ai), built to sit
# alongside your existing external_services.fake_api without breaking it.

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Literal, Tuple, Any

try:
    # Requires voting_engine.py (dataclass Vote + tally/decide)
from voting_engine import Vote, tally_weighted, decide_weighted, THRESHOLDS
except Exception as e:  # graceful fallback so imports never crash the app
    Vote = None  # type: ignore
    tally_weighted = decide_weighted = None  # type: ignore

# ---- in-memory store for weighted votes -------------------------------------

# Each item: {"proposal_id": int, "voter": str, "choice": "up"/"down", "species": "human"/"company"/"ai"}
_WEIGHTED_VOTES: List[Dict[str, Any]] = []

_SPECIES = {"human", "company", "ai"}

def _norm_species(s: str) -> str:
    s = (s or "").strip().lower()
    if s in _SPECIES:
        return s
    # common aliases
    if s in {"humans"}: return "human"
    if s in {"companies", "org", "organization", "corp"}: return "company"
    if s in {"agent", "agents", "machine", "robot", "model"}: return "ai"
    return "human"

def _norm_choice(c: str) -> str:
    c = (c or "").strip().lower()
    if c in {"up", "yes", "y", "approve", "accept"}: return "up"
    if c in {"down", "no", "n", "reject"}: return "down"
    return "down"

# ---- public API --------------------------------------------------------------

def vote_weighted(proposal_id: int, voter: str, choice: str, species: str = "human") -> Dict[str, Any]:
    """Record a weighted vote for proposal_id."""
    entry = {
        "proposal_id": int(proposal_id),
        "voter": str(voter or "anon"),
        "choice": _norm_choice(choice),
        "species": _norm_species(species),
    }
    _WEIGHTED_VOTES.append(entry)
    return {"ok": True, "stored": entry}

def list_weighted_votes(proposal_id: int | None = None) -> List[Dict[str, Any]]:
    if proposal_id is None:
        return list(_WEIGHTED_VOTES)
    pid = int(proposal_id)
    return [v for v in _WEIGHTED_VOTES if v["proposal_id"] == pid]

def clear_weighted_votes(proposal_id: int | None = None) -> Dict[str, Any]:
    global _WEIGHTED_VOTES
    if proposal_id is None:
        _WEIGHTED_VOTES = []
        return {"ok": True, "cleared": "all"}
    pid = int(proposal_id)
    kept = [v for v in _WEIGHTED_VOTES if v["proposal_id"] != pid]
    removed = len(_WEIGHTED_VOTES) - len(kept)
    _WEIGHTED_VOTES = kept
    return {"ok": True, "removed": removed, "proposal_id": pid}

def tally_proposal_weighted(proposal_id: int) -> Dict[str, Any]:
    """Return weighted up/down/total and a breakdown (per-voter weights & counts)."""
    if Vote is None or tally_weighted is None:
        return {"up": 0.0, "down": 0.0, "total": 0.0, "per_voter_weights": {}, "counts": {}}
    pid = int(proposal_id)
    votes = [Vote(**v) for v in _WEIGHTED_VOTES if v["proposal_id"] == pid]
    up, down, total, per_voter = tally_weighted(votes, pid)
    # also return species vote counts
    counts: Dict[str, int] = {}
    for v in votes:
        counts[v.species] = counts.get(v.species, 0) + 1
    return {"up": up, "down": down, "total": total, "per_voter_weights": per_voter, "counts": counts}

def decide_weighted_api(proposal_id: int, level: str = "standard") -> Dict[str, Any]:
    """Return {'status': 'accepted'|'rejected', 'threshold': float, ...}"""
    if Vote is None or decide_weighted is None:
        return {"proposal_id": int(proposal_id), "status": "rejected", "threshold": 0.6, "up": 0.0, "down": 0.0, "total": 0.0}
    pid = int(proposal_id)
    votes = [Vote(**v) for v in _WEIGHTED_VOTES if v["proposal_id"] == pid]
    lvl = level if level in {"standard", "important"} else "standard"
    return decide_weighted(votes, pid, lvl)  # type: ignore

def get_threshold(level: str) -> float:
    """Return the decision threshold for the given level."""
    lvl = level if level in {"standard", "important"} else "standard"
    return THRESHOLDS[lvl]
