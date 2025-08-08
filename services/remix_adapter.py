"""Remix creation adapter with graceful fallbacks."""
from __future__ import annotations

import os
from typing import Any, Dict

import requests  # type: ignore

USE_REAL_BACKEND = os.getenv("USE_REAL_BACKEND", "0").lower() in {"1", "true", "yes"}
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

try:  # pragma: no cover
    import superNova_2177 as sn_mod  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
    sn_mod = None  # type: ignore

_next_id = 1


def _ok(payload: Dict[str, Any]) -> Dict[str, Any]:
    payload.setdefault("available", True)
    return payload


def _na(payload: Dict[str, Any]) -> Dict[str, Any]:
    payload.setdefault("available", False)
    return payload


def create_remix(src_post_id: int, remixer: str, note: str) -> Dict[str, Any]:
    """Create a remix of ``src_post_id``."""
    global _next_id
    if sn_mod and hasattr(sn_mod, "create_remix") and USE_REAL_BACKEND:
        try:
            res = getattr(sn_mod, "create_remix")(src_post_id, remixer, note)
            if isinstance(res, dict):
                return _ok({"ok": bool(res.get("ok", True)), "new_post_id": res.get("new_post_id")})
            return _ok({"ok": bool(res), "new_post_id": _next_id})
        except Exception as exc:  # pragma: no cover
            return _na({"ok": False, "new_post_id": -1, "error": str(exc)})

    if USE_REAL_BACKEND:
        try:
            resp = requests.post(
                f"{BACKEND_URL}/remix",
                json={"src_post_id": src_post_id, "remixer": remixer, "note": note},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            return _ok({"ok": bool(data.get("ok", True)), "new_post_id": data.get("new_post_id", -1)})
        except Exception as exc:  # pragma: no cover
            return _na({"ok": False, "new_post_id": -1, "error": str(exc)})

    new_id = _next_id
    _next_id += 1
    return _na({"ok": True, "new_post_id": new_id})


__all__ = ["create_remix"]
