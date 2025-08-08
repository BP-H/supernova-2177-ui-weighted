"""Validation helpers for UI components.

The :func:`run_validations` function analyzes a payload using the real
validation pipeline when available.  In stub mode it reports the backend
as unavailable.
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


def run_validations(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Run validation integrity analysis on ``payload``.

    Parameters
    ----------
    payload:
        Arbitrary data structure expected by the backend validation
        pipeline.

    Returns
    -------
    Dict[str, Any]
        Dictionary containing ``available`` (bool), ``passed`` (bool), and
        ``details`` with backend response or error message.
    """

    if USE_REAL_BACKEND:
        if sn_mod and hasattr(sn_mod, "analyze_validation_integrity"):
            try:
                result = getattr(sn_mod, "analyze_validation_integrity")(payload)
                passed = bool(result.get("passed") or result.get("valid"))
                return {"available": True, "passed": passed, "details": result}
            except Exception as exc:  # pragma: no cover - backend failure
                return {"available": False, "passed": False, "details": str(exc)}
        try:  # pragma: no cover - network path not exercised in tests
            resp = requests.post(f"{BACKEND_URL}/validate", json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            passed = bool(data.get("passed") or data.get("valid"))
            return {"available": True, "passed": passed, "details": data}
        except Exception as exc:  # pragma: no cover
            return {"available": False, "passed": False, "details": str(exc)}

    # Stub fallback
    return {"available": False, "passed": False, "details": "backend disabled"}


__all__ = ["run_validations"]
