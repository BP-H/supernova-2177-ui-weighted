"""Reaction tracking adapter with layered fallbacks."""
from __future__ import annotations

import os
from collections import defaultdict
from typing import Any, Dict

import requests  # type: ignore

USE_REAL_BACKEND = os.getenv("USE_REAL_BACKEND", "0").lower() in {"1", "true", "yes"}
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

try:  # pragma: no cover
    import superNova_2177 as sn_mod  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
    sn_mod = None  # type: ignore

_reactions: Dict[int, Dict[str, int]] = defaultdict(lambda: defaultdict(int))


def _ok(payload: Dict[str, Any]) -> Dict[str, Any]:
    payload.setdefault("available", True)
    return payload


def _na(payload: Dict[str, Any]) -> Dict[str, Any]:
    payload.setdefault("available", False)
    return payload


def record_reaction(post_id: int, user: str, kind: str) -> Dict[str, Any]:
    """Record a reaction ``kind`` by ``user`` on ``post_id``."""
    if sn_mod and hasattr(sn_mod, "record_reaction") and USE_REAL_BACKEND:
        try:
            res = getattr(sn_mod, "record_reaction")(post_id, user, kind)
            ok = bool(res.get("ok", True)) if isinstance(res, dict) else bool(res)
            return _ok({"ok": ok})
        except Exception as exc:  # pragma: no cover
            return _na({"ok": False, "error": str(exc)})

    if USE_REAL_BACKEND:
        try:
            resp = requests.post(
                f"{BACKEND_URL}/reactor/react",
                json={"post_id": post_id, "user": user, "kind": kind},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            return _ok({"ok": bool(data.get("ok", True))})
        except Exception as exc:  # pragma: no cover
            return _na({"ok": False, "error": str(exc)})

    _reactions[post_id][kind] += 1
    return _na({"ok": True})


def get_reactions(post_id: int) -> Dict[str, Any]:
    """Return reaction counts for ``post_id``."""
    if sn_mod and hasattr(sn_mod, "get_reactions") and USE_REAL_BACKEND:
        try:
            res = getattr(sn_mod, "get_reactions")(post_id)
            counts = res.get("counts", res) if isinstance(res, dict) else res
            return _ok({"counts": dict(counts)})
        except Exception as exc:  # pragma: no cover
            return _na({"counts": {}, "error": str(exc)})

    if USE_REAL_BACKEND:
        try:
            resp = requests.get(f"{BACKEND_URL}/reactor/{post_id}", timeout=10)
            resp.raise_for_status()
            data = resp.json()
            counts = data.get("counts", data if isinstance(data, dict) else {})
            return _ok({"counts": dict(counts)})
        except Exception as exc:  # pragma: no cover
            return _na({"counts": {}, "error": str(exc)})

    return _na({"counts": dict(_reactions.get(post_id, {}))})


__all__ = ["record_reaction", "get_reactions"]
