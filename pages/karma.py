# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Karma page showing user karma and leaderboard."""

from __future__ import annotations

import streamlit as st
from streamlit_helpers import shared_header, shared_footer


def _load_karma(username: str, species: str):
    """Load karma data via ``karma_adapter``.

    Returns a tuple ``(karma, adjustments, leaderboard, adapter)``. Any
    failures are surfaced to the user via ``st.error`` and ``None`` values are
    returned to indicate the page should bail out.
    """

    try:
        with st.spinner("Fetching karma…"):
            import karma_adapter  # type: ignore

            karma = karma_adapter.get_karma(username, species)
            adjustments = karma_adapter.list_adjustments(username)
            leaderboard = karma_adapter.get_leaderboard()
        return karma, adjustments, leaderboard, karma_adapter
    except Exception as exc:  # pragma: no cover - network/adapter errors
        st.error(f"Unable to load karma data: {exc}")
        return None, None, None, None


def render() -> None:
    shared_header("Karma")

    username = st.session_state.get("username", "anon")
    species = st.session_state.get("species", "human")

    karma, adjustments, leaderboard, adapter = _load_karma(username, species)
    if karma is None or adapter is None:
        return

    st.metric("Current Karma", karma)

    plus_col, minus_col = st.columns(2)
    with plus_col:
        if st.button("+1", key="karma_plus_btn", use_container_width=True):
            try:
                with st.spinner("Updating…"):
                    adapter.adjust_karma(username, 1, species)
                st.rerun()
            except Exception as exc:  # pragma: no cover - network/adapter errors
                st.error(f"Failed to increase karma: {exc}")
    with minus_col:
        if st.button("-1", key="karma_minus_btn", use_container_width=True):
            try:
                with st.spinner("Updating…"):
                    adapter.adjust_karma(username, -1, species)
                st.rerun()
            except Exception as exc:  # pragma: no cover - network/adapter errors
                st.error(f"Failed to decrease karma: {exc}")

    st.subheader("Recent Adjustments")
    st.table(adjustments or [])

    st.subheader("Leaderboard")
    st.table(leaderboard or [])

    shared_footer()


def main() -> None:
    render()


if __name__ == "__main__":  # pragma: no cover
    main()
