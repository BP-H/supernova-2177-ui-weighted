import os
from typing import Dict

OFFLINE_MODE = os.getenv("OFFLINE_MODE", "0") == "1"

# simple in-memory store for stubbed mode
_stub_users: list[dict] = []


def register_user(username: str, email: str, password: str) -> Dict[str, bool | str]:
    """Register a user against the backend or an in-memory stub.

    Returns a dictionary with ``available`` and ``ok`` flags.
    """
    if OFFLINE_MODE:
        if any(u["username"] == username or u["email"] == email for u in _stub_users):
            return {"available": True, "ok": False, "error": "Username or email already exists"}
        _stub_users.append({"username": username, "email": email, "password": password})
        return {"available": True, "ok": True, "message": "ok"}

    try:
        from fastapi import HTTPException  # type: ignore
        from superNova_2177 import HarmonizerCreate, SessionLocal, register_harmonizer
    except Exception as exc:  # pragma: no cover - import failure
        return {"available": False, "ok": False, "error": str(exc)}

    try:
        with SessionLocal() as db:
            user = HarmonizerCreate(username=username, email=email, password=password)
            register_harmonizer(user, db)
        return {"available": True, "ok": True, "message": "ok"}
    except HTTPException as exc:  # duplicate or other HTTP errors
        if exc.status_code == 400:
            return {"available": True, "ok": False, "error": exc.detail}
        return {"available": True, "ok": False, "error": "Registration failed"}
    except Exception as exc:  # pragma: no cover - unexpected failures
        return {"available": False, "ok": False, "error": str(exc)}


def reset_stub() -> None:
    """Clear stubbed users (testing helper)."""
    _stub_users.clear()
