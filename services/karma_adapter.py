"""Karma utilities for UI components.

This module wraps backend karma operations while providing safe
fallbacks when the backend or underlying functions are unavailable.
"""
from __future__ import annotations

import os
from typing import Any, Dict

import requests

USE_REAL_BACKEND = os.getenv("USE_REAL_BACKEND", "0").lower() in {"1", "true", "yes"}
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

try:  # pragma: no cover - optional import
    import superNova_2177 as sn_mod  # type: ignore
except Exception:  # pragma: no cover - import may fail
    sn_mod = None

_stub_karma: Dict[str, float] = {}


def get_profile_karma(user: str) -> Dict[str, Any]:
    """Return karma information for ``user``.

    The function attempts to call a real backend implementation when
    ``USE_REAL_BACKEND`` is enabled.  If the backend is unavailable or the
    implementation is missing, a stub response is returned with
    ``available`` set to ``False``.
    """

    if USE_REAL_BACKEND:
        if sn_mod and hasattr(sn_mod, "get_profile_karma"):
            try:
                karma = getattr(sn_mod, "get_profile_karma")(user)
                return {"available": True, "karma": karma}
            except Exception as exc:  # pragma: no cover - backend failure
                return {"available": False, "error": str(exc)}
        try:  # pragma: no cover - network path not exercised in tests
            resp = requests.get(f"{BACKEND_URL}/karma/{user}", timeout=5)
            resp.raise_for_status()
            data = resp.json()
            data.setdefault("available", True)
            return data
        except Exception as exc:  # pragma: no cover - network errors
            return {"available": False, "error": str(exc)}

    # Fallback stub mode
    return {"available": False, "karma": _stub_karma.get(user, 0.0)}


def adjust_karma(user: str, delta: float) -> Dict[str, Any]:
    """Adjust ``user``'s karma by ``delta``.

    Returns a dict containing ``available`` and the updated ``karma``.
    ``available`` is ``False`` when operating in stub mode or upon backend
    errors.
    """

    if USE_REAL_BACKEND:
        if sn_mod and hasattr(sn_mod, "adjust_karma"):
            try:
                karma = getattr(sn_mod, "adjust_karma")(user, delta)
                return {"available": True, "karma": karma}
            except Exception as exc:  # pragma: no cover - backend failure
                return {"available": False, "error": str(exc)}
        try:  # pragma: no cover - network path not exercised in tests
            resp = requests.post(
                f"{BACKEND_URL}/karma/{user}/adjust",
                json={"delta": delta},
                timeout=5,
            )
            resp.raise_for_status()
            data = resp.json()
            data.setdefault("available", True)
            return data
        except Exception as exc:  # pragma: no cover
            return {"available": False, "error": str(exc)}

    # Stub fallback
    new_val = _stub_karma.get(user, 0.0) + float(delta)
    _stub_karma[user] = new_val
    return {"available": False, "karma": new_val}


__all__ = ["get_profile_karma", "adjust_karma"]
