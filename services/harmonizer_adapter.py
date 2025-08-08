from __future__ import annotations

import os
from typing import Any, Dict

import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
USE_REAL_BACKEND = os.getenv("USE_REAL_BACKEND", "0") == "1"


def harmonize(
    text: str, mode: str | None = None, intensity: float | None = None
) -> Dict[str, Any]:
    """Return harmonized text via backend if available.

    Parameters
    ----------
    text: str
        Input text to transform.
    mode: str | None
        Optional mode flag passed through to backend.
    intensity: float | None
        Optional intensity value passed through to backend.
    """
    payload: Dict[str, Any] = {"text": text}
    if mode is not None:
        payload["mode"] = mode
    if intensity is not None:
        payload["intensity"] = intensity

    if USE_REAL_BACKEND:
        try:
            resp = requests.post(f"{BACKEND_URL}/harmonize", json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            data.setdefault("available", True)
            data.setdefault("output", data.get("output", text))
            return data
        except Exception:
            pass
    return {"available": False, "output": text}
