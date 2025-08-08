# voting_engine.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Literal, Tuple

from services.weights import SPECIES_WEIGHTS

Species = Literal["human", "company", "ai"]
DecisionLevel = Literal["standard", "important"]

THRESHOLDS: Dict[DecisionLevel, float] = {"standard": 0.60, "important": 0.90}

@dataclass
class Vote:
    proposal_id: int
    voter: str
    choice: Literal["up", "down"]
    species: Species

def _shares(active_species: List[Species]) -> Dict[Species, float]:
    # look up configured weights and renormalize among present species
    if not active_species:
        return {}
    present = set(active_species)
    weights = {s: SPECIES_WEIGHTS.get(s, 0.0) for s in present}
    total = sum(weights.values())
    if total <= 0:
        return {s: 0.0 for s in present}
    return {s: weights[s] / total for s in present}

def tally_weighted(votes: List[Vote], proposal_id: int) -> Tuple[float, float, float, Dict[str, float]]:
    # collect only this proposal's votes
    V = [v for v in votes if v.proposal_id == proposal_id]
    if not V:
        return 0.0, 0.0, 0.0, {}
    # species shares (⅓ each if all present; renormalized if not)
    S = _shares([v.species for v in V])
    # count voters per species
    counts: Dict[Species, int] = {s: 0 for s in S}
    for v in V:
        counts[v.species] = counts.get(v.species, 0) + 1
    # per-voter weights
    per_voter: Dict[Species, float] = {s: (S[s] / counts[s]) for s in counts if counts[s] > 0}
    up = down = 0.0
    for v in V:
        w = per_voter.get(v.species, 0.0)
        if v.choice == "up":
            up += w
        elif v.choice == "down":
            down += w
    total = up + down  # ≤ 1.0 by design (sum of species shares)
    return up, down, total, per_voter

def decide_weighted(votes: List[Vote], proposal_id: int, level: DecisionLevel = "standard") -> Dict[str, float | str]:
    up, down, total, _ = tally_weighted(votes, proposal_id)
    thr = THRESHOLDS[level]
    status = "rejected"
    if total > 0 and (up / total) >= thr:
        status = "accepted"
    return {"proposal_id": proposal_id, "status": status, "up": up, "down": down, "total": total, "threshold": thr}
