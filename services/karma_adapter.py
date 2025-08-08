"""Karma service adapter with optional backend integration.

This module attempts to import real implementations from ``superNova_2177``. If the
import fails, it falls back to simple in-memory stubs. All exposed functions
return ``{"available": False}`` when an error occurs.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

try:
    from superNova_2177 import (
        get_profile_karma as _get_profile_karma,
        adjust_karma as _adjust_karma,
        get_karma_leaderboard as _get_karma_leaderboard,
    )

    _STUB = False
except Exception:  # pragma: no cover - import fallback
    _STUB = True
    _karma_store: Dict[str, int] = {}

    def _get_profile_karma(user: str) -> dict:
        """Stubbed profile lookup returning stored karma."""
        return {"user": user, "karma": _karma_store.get(user, 0), "available": True}

    def _adjust_karma(user: str, delta: int) -> dict:
        """Stubbed karma adjustment stored in-memory."""
        _karma_store[user] = _karma_store.get(user, 0) + delta
        return {"user": user, "karma": _karma_store[user], "available": True}

    def _get_karma_leaderboard(limit: int = 10) -> dict:
        """Stubbed leaderboard based on the in-memory store."""
        leaderboard: List[Tuple[str, int]] = sorted(
            _karma_store.items(), key=lambda item: item[1], reverse=True
        )[:limit]
        return {"leaderboard": leaderboard, "available": True}


def get_profile_karma(user: str) -> dict:
    """Return karma details for ``user``.

    Parameters
    ----------
    user:
        Username to look up.

    Returns
    -------
    dict
        Karma information, or ``{"available": False}`` on failure.
    """

    try:
        return _get_profile_karma(user)
    except Exception:
        return {"available": False}


def adjust_karma(user: str, delta: int) -> dict:
    """Adjust ``user``'s karma by ``delta``.

    Returns updated karma details, or ``{"available": False}`` on failure.
    """

    try:
        return _adjust_karma(user, delta)
    except Exception:
        return {"available": False}


def get_karma_leaderboard(limit: int = 10) -> dict:
    """Return top ``limit`` users by karma.

    Returns a mapping containing the leaderboard, or ``{"available": False}``
    on failure.
    """

    try:
        return _get_karma_leaderboard(limit)
    except Exception:
        return {"available": False}
