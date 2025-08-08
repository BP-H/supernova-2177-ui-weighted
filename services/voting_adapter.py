"""UI-friendly voting helpers."""
from superNova_2177 import register_vote, tally_votes, get_threshold, decide

def cast_vote(
    proposal_id: int, voter: str, choice: str, species: str = "human"
) -> dict:
    """Wrapper for :func:`register_vote` with a UI-oriented name."""
    return register_vote(proposal_id, voter, choice, species)

def tally(proposal_id: int) -> dict:
    """Wrapper for :func:`tally_votes` using a concise alias."""
    return tally_votes(proposal_id)

def threshold(level: str = "standard") -> float:
    """Expose :func:`get_threshold` for UI components."""
    return get_threshold(level)

def finalize(proposal_id: int, level: str = "standard") -> dict:
    """Wrapper around :func:`decide` for UI readability."""
    return decide(proposal_id, level)
