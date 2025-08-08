"""Central helpers for Streamlit widget keys.

Ensures uniqueness across pages by applying a common naming scheme.
"""

from __future__ import annotations

# Suffix applied to all widget keys to signal the v2 naming scheme.
_KEY_SUFFIX = "_v2"


def page_key(page: str, name: str) -> str:
    """Return a namespaced widget key for ``name`` on ``page``.

    Examples
    --------
    >>> page_key("resonance_music", "status_ping")
    'resonance_music_status_ping_v2'
    """

    return f"{page}_{name}{_KEY_SUFFIX}"


# Page identifiers used throughout the repo. Documenting them here helps
# maintainers keep track of the keys reserved by each page.
RESONANCE_MUSIC_PAGE = "resonance_music"
VIDEO_CHAT_PAGE = "video_chat"
