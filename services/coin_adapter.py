"""RootCoin adapter with graceful fallbacks.

Resolution order:
  1) Functions from ``superNova_2177`` when available.
  2) HTTP calls when ``USE_REAL_BACKEND=1``.
  3) In-memory stubs (balances + ledger).

All functions return dictionaries with an ``available`` flag.
"""
from __future__ import annotations

import os
from collections import defaultdict
from typing import Any, Dict, List, Optional

import requests  # type: ignore

from .coin_config import DEFAULT_REWARD_SPLIT

USE_REAL_BACKEND = os.getenv("USE_REAL_BACKEND", "0").lower() in {"1", "true", "yes"}
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

try:  # pragma: no cover - optional import
    import superNova_2177 as sn_mod  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
    sn_mod = None  # type: ignore

_balances: Dict[str, float] = defaultdict(float)
_ledger: List[Dict[str, Any]] = []


def _ok(payload: Dict[str, Any]) -> Dict[str, Any]:
    payload.setdefault("available", True)
    return payload


def _na(payload: Dict[str, Any]) -> Dict[str, Any]:
    payload.setdefault("available", False)
    return payload


def _normalise_split(split: Optional[Dict[str, float]]) -> Dict[str, float]:
    data = dict(split or DEFAULT_REWARD_SPLIT)
    total = sum(data.values())
    if total <= 0:
        return DEFAULT_REWARD_SPLIT
    if total > 1.0:
        data = {k: v / total for k, v in data.items()}
    return data


def get_balance(user: str) -> Dict[str, Any]:
    """Return RootCoin balance for ``user``."""
    if sn_mod and hasattr(sn_mod, "get_balance") and USE_REAL_BACKEND:
        try:
            val = getattr(sn_mod, "get_balance")(user)
            bal = val.get("balance") if isinstance(val, dict) else float(val)
            return _ok({"balance": float(bal)})
        except Exception as exc:  # pragma: no cover
            return _na({"balance": 0.0, "error": str(exc)})

    if USE_REAL_BACKEND:
        try:
            resp = requests.get(f"{BACKEND_URL}/coin/balance/{user}", timeout=10)
            resp.raise_for_status()
            data = resp.json()
            return _ok({"balance": float(data.get("balance", 0.0))})
        except Exception as exc:  # pragma: no cover
            return _na({"balance": 0.0, "error": str(exc)})

    return _na({"balance": float(_balances[user])})


def tip(from_user: str, to_user: str, amount: float, memo: str | None = None) -> Dict[str, Any]:
    """Transfer ``amount`` from ``from_user`` to ``to_user``."""
    if sn_mod and hasattr(sn_mod, "tip") and USE_REAL_BACKEND:
        try:
            res = getattr(sn_mod, "tip")(from_user, to_user, amount, memo)
            ok = bool(res.get("ok", True)) if isinstance(res, dict) else bool(res)
            return _ok({"ok": ok})
        except Exception as exc:  # pragma: no cover
            return _na({"ok": False, "error": str(exc)})

    if USE_REAL_BACKEND:
        try:
            resp = requests.post(
                f"{BACKEND_URL}/coin/tip",
                json={
                    "from_user": from_user,
                    "to_user": to_user,
                    "amount": float(amount),
                    "memo": memo,
                },
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            return _ok({"ok": bool(data.get("ok", True))})
        except Exception as exc:  # pragma: no cover
            return _na({"ok": False, "error": str(exc)})

    _balances[from_user] -= float(amount)
    _balances[to_user] += float(amount)
    _ledger.append(
        {
            "type": "tip",
            "from": from_user,
            "to": to_user,
            "amount": float(amount),
            "memo": memo or "",
        }
    )
    return _na({"ok": True})


def reward(post_id: int, split: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Reward contributors for ``post_id`` using ``split`` ratios."""
    norm_split = _normalise_split(split)
    if sn_mod and hasattr(sn_mod, "reward") and USE_REAL_BACKEND:
        try:
            res = getattr(sn_mod, "reward")(post_id, norm_split)
            ok = bool(res.get("ok", True)) if isinstance(res, dict) else bool(res)
            return _ok({"ok": ok})
        except Exception as exc:  # pragma: no cover
            return _na({"ok": False, "error": str(exc)})

    if USE_REAL_BACKEND:
        try:
            resp = requests.post(
                f"{BACKEND_URL}/coin/reward",
                json={"post_id": post_id, "split": norm_split},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            return _ok({"ok": bool(data.get("ok", True))})
        except Exception as exc:  # pragma: no cover
            return _na({"ok": False, "error": str(exc)})

    _ledger.append({"type": "reward", "post_id": post_id, "split": norm_split})
    return _na({"ok": True})


def ledger(limit: int = 50) -> Dict[str, Any]:
    """Return recent ledger entries."""
    if sn_mod and hasattr(sn_mod, "ledger") and USE_REAL_BACKEND:
        try:
            res = getattr(sn_mod, "ledger")(limit)
            entries = res.get("entries", res) if isinstance(res, dict) else res
            return _ok({"entries": list(entries)[: int(limit)]})
        except Exception as exc:  # pragma: no cover
            return _na({"entries": [], "error": str(exc)})

    if USE_REAL_BACKEND:
        try:
            resp = requests.get(f"{BACKEND_URL}/coin/ledger", params={"limit": int(limit)}, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            entries = data.get("entries", data if isinstance(data, list) else [])
            return _ok({"entries": list(entries)[: int(limit)]})
        except Exception as exc:  # pragma: no cover
            return _na({"entries": [], "error": str(exc)})

    return _na({"entries": list(_ledger)[-int(limit):]})


__all__ = ["get_balance", "tip", "reward", "ledger"]
