# pages/karma.py
# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration • Legal & Ethical Safeguards
from __future__ import annotations

import streamlit as st
from services import karma_adapter as K  # correct import

def _leaderboard_rows(obj):
    # adapter returns {"leaderboard": List[Tuple[user, karma]], "available": True}
    if isinstance(obj, dict):
        rows = obj.get("leaderboard", [])
    else:
        rows = obj or []
    return [{"user": u, "karma": k} for (u, k) in rows]

def render() -> None:
    st.title("⭐ Karma")

    user = st.session_state.get("username", "anon")
    species = st.session_state.get("species", "human")  # not used by adapter now, but kept for future

    data = K.get_profile_karma(user)
    if not data.get("available", True):
        st.warning("Karma backend unavailable — using in-memory stub.")
    karma = int(data.get("karma", 0))
    st.metric("Current karma", karma)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("➕  +1", use_container_width=True, key="karma_plus_btn"):
            K.adjust_karma(user, 1)
            st.rerun()
    with c2:
        if st.button("➖  -1", use_container_width=True, key="karma_minus_btn"):
            K.adjust_karma(user, -1)
            st.rerun()

    st.subheader("Leaderboard")
    lb = K.get_karma_leaderboard(limit=20)
    st.table(_leaderboard_rows(lb))

def main() -> None:
    render()

if __name__ == "__main__":  # pragma: no cover
    main()
