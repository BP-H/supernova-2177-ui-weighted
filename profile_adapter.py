"""Profile update adapter handling backend/stub flows."""

from __future__ import annotations

import os
from typing import Dict, List

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover - requests not installed
    requests = None  # type: ignore

try:  # pragma: no cover - streamlit may be missing in tests
    import streamlit as st
except Exception:  # pragma: no cover
    st = None  # type: ignore

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def update_profile_adapter(
    bio: str,
    cultural_preferences: List[str],
    *,
    use_backend: bool | None = None,
) -> Dict[str, str | bool]:
    """Update the user's profile.

    Always returns a dictionary containing an ``available`` flag.
    """

    if not bio.strip():
        return {"available": True, "status": "error", "error": "Bio is required"}

    if use_backend is None and st is not None:
        use_backend = st.session_state.get("use_backend", False)

    if not use_backend:
        return {
            "available": True,
            "status": "stubbed",
            "bio": bio,
            "cultural_preferences": cultural_preferences,
        }

    if requests is None:
        return {
            "available": False,
            "status": "error",
            "error": "requests not installed",
        }

    payload = {"bio": bio, "cultural_preferences": cultural_preferences}
    try:
        resp = requests.put(f"{BACKEND_URL}/users/me", json=payload, timeout=5)
        resp.raise_for_status()
        return {"available": True, "status": "ok"}
    except Exception as exc:
        return {"available": False, "status": "error", "error": str(exc)}
