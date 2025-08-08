"""Harmonizer-related backend helpers.

Environment variables:
    USE_REAL_BACKEND: set to "1" to contact the live API. The default
        uses in-memory stubs suitable for local demos.
    BACKEND_URL: base URL for the backend API (default ``http://localhost:8000``).

All functions return dictionaries and attempt to fail gracefully if the
backend is unreachable or returns an error.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

import requests

USE_REAL_BACKEND = os.getenv("USE_REAL_BACKEND", "0") == "1"
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# simple in-memory store for stubbed mode
_stub_users: List[Dict[str, Any]] = []


def register(username: str, email: str, password: str) -> Dict[str, Any]:
    """Register a harmonizer via the backend or a local stub."""
    if not USE_REAL_BACKEND:
        if any(u["username"] == username or u["email"] == email for u in _stub_users):
            return {"error": "Username or email already exists"}
        user = {"username": username, "email": email, "influence_score": 0.0}
        _stub_users.append(user)
        return user
    try:
        resp = requests.post(
            f"{BACKEND_URL}/users/register",
            json={"username": username, "email": email, "password": password},
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:  # pragma: no cover - network failures
        return {"error": str(exc)}


def get_influence_score(username: str) -> Dict[str, Any]:
    """Return a harmonizer's influence score."""
    if not USE_REAL_BACKEND:
        user = next((u for u in _stub_users if u["username"] == username), None)
        if not user:
            return {"error": "Harmonizer not found"}
        return {"influence_score": user.get("influence_score", 0.0)}
    try:
        resp = requests.get(f"{BACKEND_URL}/users/{username}", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return {"influence_score": data.get("network_centrality", 0.0)}
    except Exception as exc:  # pragma: no cover - network failures
        return {"error": str(exc)}


def list_harmonizers(limit: int = 10) -> Dict[str, Any]:
    """List harmonizers with an optional limit."""
    if not USE_REAL_BACKEND:
        return {"harmonizers": _stub_users[:limit]}
    try:
        resp = requests.get(f"{BACKEND_URL}/users/search", params={"q": ""}, timeout=5)
        resp.raise_for_status()
        users = resp.json()
        return {"harmonizers": users[:limit]}
    except Exception as exc:  # pragma: no cover - network failures
        return {"error": str(exc)}


def reset_stub() -> None:
    """Clear stubbed users (testing helper)."""
    _stub_users.clear()
