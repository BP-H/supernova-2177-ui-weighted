"""Universe fork federation adapter."""
from __future__ import annotations

import os
import uuid
from typing import Any, Dict

import requests  # type: ignore

USE_REAL_BACKEND = os.getenv("USE_REAL_BACKEND", "0").lower() in {"1", "true", "yes"}
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

try:  # pragma: no cover
    import superNova_2177 as sn_mod  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
    sn_mod = None  # type: ignore

_forks: list[Dict[str, Any]] = []


def _ok(payload: Dict[str, Any]) -> Dict[str, Any]:
    payload.setdefault("available", True)
    return payload


def _na(payload: Dict[str, Any]) -> Dict[str, Any]:
    payload.setdefault("available", False)
    return payload


def list_forks() -> Dict[str, Any]:
    """List known universe forks."""
    if sn_mod and hasattr(sn_mod, "list_forks") and USE_REAL_BACKEND:
        try:
            res = getattr(sn_mod, "list_forks")()
            forks = res.get("forks", res) if isinstance(res, dict) else res
            return _ok({"forks": list(forks)})
        except Exception as exc:  # pragma: no cover
            return _na({"forks": [], "error": str(exc)})

    if USE_REAL_BACKEND:
        try:
            resp = requests.get(f"{BACKEND_URL}/forks", timeout=10)
            resp.raise_for_status()
            data = resp.json()
            forks = data.get("forks", data if isinstance(data, list) else [])
            return _ok({"forks": list(forks)})
        except Exception as exc:  # pragma: no cover
            return _na({"forks": [], "error": str(exc)})

    return _na({"forks": list(_forks)})


def create_fork(creator: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new universe fork."""
    if sn_mod and hasattr(sn_mod, "create_fork") and USE_REAL_BACKEND:
        try:
            res = getattr(sn_mod, "create_fork")(creator, config)
            if isinstance(res, dict):
                return _ok({"ok": bool(res.get("ok", True)), "fork_id": res.get("fork_id")})
            return _ok({"ok": bool(res), "fork_id": None})
        except Exception as exc:  # pragma: no cover
            return _na({"ok": False, "fork_id": None, "error": str(exc)})

    if USE_REAL_BACKEND:
        try:
            resp = requests.post(
                f"{BACKEND_URL}/forks",
                json={"creator": creator, "config": config},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            return _ok({"ok": bool(data.get("ok", True)), "fork_id": data.get("fork_id")})
        except Exception as exc:  # pragma: no cover
            return _na({"ok": False, "fork_id": None, "error": str(exc)})

    fid = uuid.uuid4().hex
    _forks.append({"id": fid, "creator": creator, "config": dict(config)})
    return _na({"ok": True, "fork_id": fid})


__all__ = ["list_forks", "create_fork"]
