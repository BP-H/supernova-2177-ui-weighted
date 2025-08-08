"""Harmonizer + Text Harmonization adapter (unified, backend-aware).

This module exposes:
  - register(username, email, password) -> dict
  - get_influence_score(username) -> dict
  - list_harmonizers(limit=10) -> dict
  - reset_stub() -> None
  - harmonize(text, mode="balanced", intensity=0.5) -> dict

Resolution strategy (in order):
  1) Call in-process functions from superNova_2177 if present.
  2) Use HTTP endpoints on BACKEND_URL when USE_REAL_BACKEND is set.
  3) Fall back to safe in-memory stubs (for local demos/tests).
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Callable, Optional

import requests  # expected in requirements

# Env toggles
USE_REAL_BACKEND = os.getenv("USE_REAL_BACKEND", "0").lower() in {"1", "true", "yes"}
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Try to import the backend module if we're in the same process
try:  # pragma: no cover - optional import
    import superNova_2177 as sn_mod  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
    sn_mod = None  # type: ignore[assignment]


# --------------------------- in-memory stub store ------------------------------

_stub_users: List[Dict[str, Any]] = []


def reset_stub() -> None:
    """Clear stubbed users (testing helper)."""
    _stub_users.clear()


# --------------------------- helpers ------------------------------------------

def _get_attr(names: List[str]) -> Optional[Callable[..., Any]]:
    """Return the first callable attribute found on sn_mod from candidate names."""
    if not sn_mod:
        return None
    for n in names:
        fn = getattr(sn_mod, n, None)
        if callable(fn):
            return fn  # type: ignore[return-value]
    return None


# --------------------------- public API: users --------------------------------

def register(username: str, email: str, password: str) -> Dict[str, Any]:
    """Register a harmonizer via in-process backend, HTTP, or stub."""
    # 1) in-process function candidates (be flexible with names)
    fn = _get_attr(["register_harmonizer", "register_user", "register"])
    if fn and USE_REAL_BACKEND:
        try:
            return fn(username=username, email=email, password=password)  # type: ignore[misc]
        except Exception as exc:  # pragma: no cover
            return {"error": str(exc)}

    # 2) HTTP fallback when real backend is requested
    if USE_REAL_BACKEND:
        try:
            resp = requests.post(
                f"{BACKEND_URL}/users/register",
                json={"username": username, "email": email, "password": password},
                timeout=10,
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:  # pragma: no cover
            return {"error": str(exc)}

    # 3) stub mode
    if any(u["username"] == username or u["email"] == email for u in _stub_users):
        return {"error": "Username or email already exists"}
    user = {"username": username, "email": email, "influence_score": 0.0}
    _stub_users.append(user)
    return user


def get_influence_score(username: str) -> Dict[str, Any]:
    """Return a harmonizer's influence score."""
    # 1) in-process
    fn = _get_attr(["get_influence_score", "get_user_influence", "get_user"])
    if fn and USE_REAL_BACKEND:
        try:
            res = fn(username)  # type: ignore[misc]
            # Normalize to a stable shape
            if isinstance(res, dict) and "influence_score" in res:
                return {"influence_score": float(res["influence_score"])}
            # Some backends return user dicts with 'network_centrality'
            if isinstance(res, dict) and "network_centrality" in res:
                return {"influence_score": float(res["network_centrality"])}
            # Last resort: 0.0 if we can't infer
            return {"influence_score": 0.0}
        except Exception as exc:  # pragma: no cover
            return {"error": str(exc)}

    # 2) HTTP
    if USE_REAL_BACKEND:
        try:
            resp = requests.get(f"{BACKEND_URL}/users/{username}", timeout=10)
            resp.raise_for_status()
            data = resp.json()
            score = data.get("influence_score", data.get("network_centrality", 0.0))
            return {"influence_score": float(score)}
        except Exception as exc:  # pragma: no cover
            return {"error": str(exc)}

    # 3) stub
    user = next((u for u in _stub_users if u["username"] == username), None)
    if not user:
        return {"error": "Harmonizer not found"}
    return {"influence_score": float(user.get("influence_score", 0.0))}


def list_harmonizers(limit: int = 10) -> Dict[str, Any]:
    """List harmonizers with an optional limit (best effort)."""
    # 1) in-process
    fn = _get_attr(["list_harmonizers", "list_users", "search_users"])
    if fn and USE_REAL_BACKEND:
        try:
            res = fn(limit=limit) if "limit" in getattr(fn, "__code__", {}).co_varnames else fn()  # type: ignore[attr-defined]
            # Normalize
            if isinstance(res, dict) and "harmonizers" in res:
                users = list(res["harmonizers"])
            elif isinstance(res, list):
                users = res
            else:
                users = []
            return {"harmonizers": users[:limit]}
        except Exception as exc:  # pragma: no cover
            return {"error": str(exc)}

    # 2) HTTP
    if USE_REAL_BACKEND:
        try:
            resp = requests.get(f"{BACKEND_URL}/users/search", params={"q": ""}, timeout=10)
            resp.raise_for_status()
            users = resp.json()
            if isinstance(users, dict) and "harmonizers" in users:
                users = users["harmonizers"]
            if not isinstance(users, list):
                users = []
            return {"harmonizers": users[:limit]}
        except Exception as exc:  # pragma: no cover
            return {"error": str(exc)}

    # 3) stub
    return {"harmonizers": _stub_users[:limit]}


# --------------------------- public API: harmonize ----------------------------

def harmonize(text: str, mode: str = "balanced", intensity: float = 0.5) -> Dict[str, Any]:
    """Return a harmonized representation of `text` (best effort).

    Returns: {"available": bool, "result": ..., "error"?: str}
    """
    # 1) in-process
    fn = _get_attr(["harmonize", "text_harmonize", "harmonizer"])
    if fn and USE_REAL_BACKEND:
        try:
            out = fn(text, mode=mode, intensity=float(intensity))  # type: ignore[misc]
            return {"available": True, "result": out}
        except Exception as exc:  # pragma: no cover
            return {"available": False, "error": str(exc)}

    # 2) HTTP
    if USE_REAL_BACKEND:
        try:
            resp = requests.post(
                f"{BACKEND_URL}/harmonize",
                json={"text": text, "mode": mode, "intensity": float(intensity)},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            data.setdefault("available", True)
            # Ensure a stable key
            if "result" not in data and "output" in data:
                data["result"] = data["output"]
            return data
        except Exception as exc:  # pragma: no cover
            return {"available": False, "error": str(exc)}

    # 3) stub
    return {"available": False, "result": text}


__all__ = [
    "register",
    "get_influence_score",
    "list_harmonizers",
    "reset_stub",
    "harmonize",
]
