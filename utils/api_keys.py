from __future__ import annotations

"""Helper utilities for retrieving API keys.

This module centralizes access to API keys. It first checks ``st.secrets``
for a key suffixed with ``"_v2"`` and falls back to environment variables.
It never raises if ``st`` or the secret is unavailable.
"""

import os
from typing import Optional

try:  # pragma: no cover - streamlit may be unavailable during tests
    import streamlit as st  # type: ignore
except Exception:  # pragma: no cover
    st = None  # type: ignore


def get_api_key(env_key: str) -> str:
    """Retrieve an API key from ``st.secrets`` or ``os.environ``.

    Parameters
    ----------
    env_key:
        The name of the environment variable (e.g. ``"OPENAI_API_KEY"``).

    Returns
    -------
    str
        The API key if found, otherwise an empty string.
    """
    secret_key = f"{env_key}_v2"
    if st is not None:
        try:
            secret = st.secrets.get(secret_key, "")  # type: ignore[arg-type]
            if isinstance(secret, str) and secret.strip():
                return secret.strip()
        except Exception:
            pass
    return os.getenv(env_key, "").strip()


__all__ = ["get_api_key"]
