# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Adapter for retrieving system status metrics from the backend."""

from __future__ import annotations

import os
from typing import Any, Dict

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover - requests missing
    requests = None  # type: ignore

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
OFFLINE_MODE = os.getenv("OFFLINE_MODE", "0") == "1"


def get_status() -> Dict[str, Any]:
    """Fetch system status data from the backend API.

    Always returns a dictionary containing ``available``.
    """
    if OFFLINE_MODE or requests is None:
        return {"available": False}
    try:
        resp = requests.get(f"{BACKEND_URL}/status", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        data["available"] = True
        return data
    except Exception:
        return {"available": False}
