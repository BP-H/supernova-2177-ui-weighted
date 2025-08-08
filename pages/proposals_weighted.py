# pages/proposals_weighted.py
from __future__ import annotations

import streamlit as st
from external_services.fake_api_weighted import (
    list_weighted_votes,
    tally_proposal_weighted,
    vote_weighted,
)


# ---- proposal list (best-effort) --------------------------------------------
def _list_proposals():
    """Try to pull proposals from your existing fake_api; fallback to none."""
    try:
        from external_services.fake_api import list_proposals  # optional, may not exist

        return list_proposals()  # expected: [{"id": int, "title": str, ...}, ...]
    except Exception:
        return []


def render():
    st.title("📑 Proposals (Weighted)")

    # Pick proposal
    proposals = _list_proposals()
    if proposals:
        labels = [
            f'#{p.get("id", i)} — {p.get("title","(no title)")}'
            for i, p in enumerate(proposals)
        ]
        idx = st.selectbox(
            "Choose a proposal",
            options=range(len(proposals)),
            format_func=lambda i: labels[i],
            key="weighted_pick_proposal",
        )
        pid = int(proposals[idx].get("id", idx + 1))
        title = proposals[idx].get("title", f"Proposal {pid}")
    else:
        st.info("No proposals from backend. Enter an ID to test the weighted engine.")
        pid = st.number_input(
            "Proposal ID", min_value=1, value=1, step=1, key="weighted_pid_input"
        )
        title = f"Proposal {pid}"

    st.subheader(title)

    # Use species chosen in the global sidebar
    species = st.session_state["species"]

    col_up, col_down = st.columns(2)

    with col_up:
        if st.button("👍 Vote UP", use_container_width=True, key=f"vote_up_{pid}"):
            vote_weighted(
                pid,
                st.session_state.get("username", "anon"),
                "up",
                species,
            )
            st.rerun()

    with col_down:
        if st.button("👎 Vote DOWN", use_container_width=True, key=f"vote_down_{pid}"):
            vote_weighted(
                pid,
                st.session_state.get("username", "anon"),
                "down",
                species,
            )
            st.rerun()

    # Live weighted tally
    tally = tally_proposal_weighted(pid)
    up, down, total = tally["up"], tally["down"], tally["total"]
    pct_yes = (up / total * 100.0) if total > 0 else 0.0
    st.markdown(
        f"**Weighted tally:** {up:.3f} ↑ / {down:.3f} ↓ — total {total:.3f}  "
        f"(**{pct_yes:.1f}% yes**)",
    )

    with st.expander("Breakdown"):
        st.write("Per-voter weights:", tally.get("per_voter_weights", {}))
        st.write("Counts by species:", tally.get("counts", {}))
        st.write("Raw weighted votes:", list_weighted_votes(pid))


def main():
    render()


if __name__ == "__main__":
    main()
