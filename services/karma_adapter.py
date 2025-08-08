"""Karma adapter (unified + conflict-free)

Exposes a stable UI-friendly API with graceful fallbacks:

  - get_profile_karma(user) -> {"available": bool, "user": str, "karma": float, "error"?: str}
  - adjust_karma(user, delta) -> {"available": bool, "user": str, "karma": float, "error"?: str}
  - get_karma_leaderboard(limit=10) -> {"available": bool, "leaderboard": list[tuple[str, float]], "error"?: str}

Resolution order:
  1) In-process functions from superNova_2177 if present.
  2) HTTP endpoints when USE_REAL_BACKEND is set.
  3) In-memory stubs (local/demo).
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Tuple

import requests  # ensure in requirements

# Env toggles
USE_REAL_BACKEND = os.getenv("USE_REAL_BACKEND", "0").lower() in {"1", "true", "yes"}
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Try to import the backend module if we're in the same process
try:  # pragma: no cover - optional import
    import superNova_2177 as sn_mod  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
    sn_mod = None  # type: ignore[assignment]

# --------------------------- in-memory stub store ------------------------------

_karma_store: Dict[str, float] = {}


# --------------------------- helpers ------------------------------------------

def _ok(payload: Dict[str, Any]) -> Dict[str, Any]:
    payload.setdefault("available", True)
    return payload


def _err(user: str | None, msg: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {"available": False, "error": msg}
    if user is not None:
        out["user"] = user
        out["karma"] = float(_karma_store.get(user, 0.0))
    return out


# --------------------------- public API ---------------------------------------

def get_profile_karma(user: str) -> Dict[str, Any]:
    """Return karma info for `user` with a consistent shape."""
    # 1) in-process superNova_2177
    if sn_mod and hasattr(sn_mod, "get_profile_karma") and USE_REAL_BACKEND:
        try:
            val = getattr(sn_mod, "get_profile_karma")(user)
            # Normalize possible shapes
            if isinstance(val, dict):
                karma = val.get("karma", val.get("score", val.get("value", 0)))
            else:
                karma = val
            return _ok({"user": user, "karma": float(karma)})
        except Exception as exc:  # pragma: no cover
            return _err(user, str(exc))

    # 2) HTTP backend
    if USE_REAL_BACKEND:
        try:
            resp = requests.get(f"{BACKEND_URL}/karma/{user}", timeout=10)
            resp.raise_for_status()
            data = resp.json()
            karma = data.get("karma", data.get("score", 0.0))
            return _ok({"user": user, "karma": float(karma)})
        except Exception as exc:  # pragma: no cover
            return _err(user, str(exc))

    # 3) stub
    return {"available": False, "user": user, "karma": float(_karma_store.get(user, 0.0))}


def adjust_karma(user: str, delta: float) -> Dict[str, Any]:
    """Adjust `user`'s karma by `delta` and return updated value."""
    # 1) in-process superNova_2177
    if sn_mod and hasattr(sn_mod, "adjust_karma") and USE_REAL_BACKEND:
        try:
            val = getattr(sn_mod, "adjust_karma")(user, delta)
            # Normalize
            if isinstance(val, dict):
                karma = val.get("karma", val.get("score", 0.0))
            else:
                karma = val
            return _ok({"user": user, "karma": float(karma)})
        except Exception as exc:  # pragma: no cover
            return _err(user, str(exc))

    # 2) HTTP backend
    if USE_REAL_BACKEND:
        try:
            resp = requests.post(
                f"{BACKEND_URL}/karma/{user}/adjust",
                json={"delta": float(delta)},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            karma = data.get("karma", data.get("score", 0.0))
            return _ok({"user": user, "karma": float(karma)})
        except Exception as exc:  # pragma: no cover
            return _err(user, str(exc))

    # 3) stub
    new_val = float(_karma_store.get(user, 0.0)) + float(delta)
    _karma_store[user] = new_val
    # Mark as unavailable so callers know it's a demo value
    return {"available": False, "user": user, "karma": new_val}


def get_karma_leaderboard(limit: int = 10) -> Dict[str, Any]:
    """Return top `limit` users by karma with a consistent shape."""
    # 1) in-process superNova_2177
    if sn_mod and hasattr(sn_mod, "get_karma_leaderboard") and USE_REAL_BACKEND:
        try:
            res = getattr(sn_mod, "get_karma_leaderboard")(limit)
            # Normalize shapes: dict with "leaderboard" OR raw list
            if isinstance(res, dict):
                lb = res.get("leaderboard", res.get("items", []))
            else:
                lb = res
            # Ensure list of (user, karma) tuples
            leaderboard: List[Tuple[str, float]] = []
            for item in (lb or []):
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    leaderboard.append((str(item[0]), float(item[1])))
                elif isinstance(item, dict):
                    leaderboard.append((str(item.get("user") or item.get("username")), float(item.get("karma", 0.0))))
            return _ok({"leaderboard": leaderboard[: max(1, int(limit))]})
        except Exception as exc:  # pragma: no cover
            return {"available": False, "leaderboard": [], "error": str(exc)}

    # 2) HTTP backend
    if USE_REAL_BACKEND:
        try:
            resp = requests.get(f"{BACKEND_URL}/karma/leaderboard", params={"limit": int(limit)}, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            lb = data.get("leaderboard", data if isinstance(data, list) else [])
            leaderboard: List[Tuple[str, float]] = []
            for item in (lb or []):
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    leaderboard.append((str(item[0]), float(item[1])))
                elif isinstance(item, dict):
                    leaderboard.append((str(item.get("user") or item.get("username")), float(item.get("karma", 0.0))))
            return _ok({"leaderboard": leaderboard[: max(1, int(limit))]})
        except Exception as exc:  # pragma: no cover
            return {"available": False, "leaderboard": [], "error": str(exc)}

    # 3) stub
    leaderboard_stub: List[Tuple[str, float]] = sorted(
        _karma_store.items(), key=lambda kv: kv[1], reverse=True
    )[: max(1, int(limit))]
    return {"available": False, "leaderboard": leaderboard_stub}


__all__ = ["get_profile_karma", "adjust_karma", "get_karma_leaderboard"]
