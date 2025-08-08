from __future__ import annotations
from typing import Dict, List, Literal
try:
    from fastapi import APIRouter, Body
except Exception:  # super defensive fallback if FastAPI isn't present yet
    class APIRouter:
        def __init__(self): ...
        def post(self, *a, **k): return lambda f: f
        def get(self, *a, **k): return lambda f: f
    def Body(*a, **k): return None

try:
    from services.weights import SPECIES_WEIGHTS  # optional nicer weights
except Exception:
    SPECIES_WEIGHTS = {"human": 1.0, "company": 1.0, "ai": 1.0}

Species = Literal["human","company","ai"]
router = APIRouter()

class _Vote:
    def __init__(self, pid: int, voter: str, choice: str, species: Species):
        self.pid = pid
        self.voter = voter
        self.choice = "up" if choice.lower() in {"up","yes","y","approve"} else "down"
        self.species = species

_VOTES: List[_Vote] = []
THRESHOLDS = {"standard": 0.60, "important": 0.90}

def _shares(active: List[Species]) -> Dict[Species, float]:
    present = sorted(set(active))
    if not present: return {}
    w = {s: float(SPECIES_WEIGHTS.get(s, 0.0)) for s in present}
    total = sum(w.values()) or 1.0
    return {s: w[s] / total for s in present}

@router.post("/api/votes/{proposal_id}", tags=["Governance"])
def register_vote(proposal_id: int,
                  voter: str = Body(...),
                  choice: str = Body(...),
                  species: str = Body("human")):
    s = species if species in {"human","company","ai"} else "human"
    _VOTES.append(_Vote(int(proposal_id), str(voter), str(choice), s))
    return {"ok": True}

@router.get("/api/votes/{proposal_id}/tally", tags=["Governance"])
def tally_votes(proposal_id: int):
    V = [v for v in _VOTES if v.pid == int(proposal_id)]
    if not V: return {"up": 0.0, "down": 0.0, "total": 0.0, "per_voter_weights": {}, "counts": {}}
    shares = _shares([v.species for v in V])
    counts = {s: 0 for s in shares}
    for v in V: counts[v.species] = counts.get(v.species, 0) + 1
    per_voter = {s: (shares[s] / counts[s]) for s in counts if counts[s] > 0}
    up = sum(per_voter.get(v.species,0.0) for v in V if v.choice=="up")
    down = sum(per_voter.get(v.species,0.0) for v in V if v.choice=="down")
    total = up + down
    return {"up": up, "down": down, "total": total, "per_voter_weights": per_voter, "counts": counts}

@router.get("/api/votes/{proposal_id}/decide", tags=["Governance"])
def decide_vote(proposal_id: int, level: str="standard"):
    t = tally_votes(proposal_id)
    thr = THRESHOLDS["important" if level=="important" else "standard"]
    status = "accepted" if (t["total"]>0 and (t["up"]/t["total"])>=thr) else "rejected"
