"""Text harmonization utilities.

Provides a safe wrapper around potential backend harmonization
capabilities, exposing a simple :func:`harmonize` function for the UI.
"""
from __future__ import annotations

import os
from typing import Any, Dict

import requests

USE_REAL_BACKEND = os.getenv("USE_REAL_BACKEND", "0").lower() in {"1", "true", "yes"}
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

try:  # pragma: no cover - optional import
    import superNova_2177 as sn_mod  # type: ignore
except Exception:  # pragma: no cover
    sn_mod = None


def harmonize(
    text: str, mode: str = "balanced", intensity: float = 0.5
) -> Dict[str, Any]:
    """Return a harmonized representation of ``text``.

    Parameters
    ----------
    text:
        The source content to be harmonized.
    mode:
        Backend-defined mode, defaulting to ``"balanced"``.
    intensity:
        Float value indicating the strength of harmonization.
    """

    if USE_REAL_BACKEND:
        if sn_mod and hasattr(sn_mod, "harmonize"):
            try:
                result = getattr(sn_mod, "harmonize")(
                    text, mode=mode, intensity=intensity
                )
                return {"available": True, "result": result}
            except Exception as exc:  # pragma: no cover - backend failure
                return {"available": False, "error": str(exc)}
        try:  # pragma: no cover - network path not exercised in tests
            resp = requests.post(
                f"{BACKEND_URL}/harmonize",
                json={"text": text, "mode": mode, "intensity": intensity},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            data.setdefault("available", True)
            return data
        except Exception as exc:  # pragma: no cover
            return {"available": False, "error": str(exc)}

    # Stub fallback simply echoes the text
    return {"available": False, "result": text}


__all__ = ["harmonize"]
