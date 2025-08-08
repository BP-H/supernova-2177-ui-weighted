# pages/proposals_weighted.py
from __future__ import annotations

import streamlit as st
from external_services.fake_api_weighted import (
    list_weighted_votes,
    tally_proposal_weighted,
    vote_weighted,
)


# try to read proposals from your existing fake_api; fall back to manual ID entry
def _list_proposals():
    try:
        from external_services.fake_api import (
            list_proposals,
        )  # your existing helper if present

        return (
            list_proposals()
        )  # expected: list[{"id": int, "title": str, ...}] or similar
    except Exception:
        return []


def render():
    st.title("📑 Proposals (Weighted)")
    props = _list_proposals()

    # pick proposal
    if props:
        labels = [
            f'#{p.get("id", i)} — {p.get("title","(no title)")}'
            for i, p in enumerate(props)
        ]
        idx = st.selectbox(
            "Choose a proposal",
            range(len(props)),
            format_func=lambda i: labels[i],
        )
        pid = int(props[idx].get("id", idx + 1))
        title = props[idx].get("title", f"Proposal {pid}")
    else:
        st.info("No proposals listed by backend. Enter an ID to test.")
        pid = st.number_input("Proposal ID", min_value=1, value=1, step=1)
        title = f"Proposal {pid}"

    st.subheader(title)

    # species / choice from global sidebar
    species = st.session_state["species"]
    c1, c2 = st.columns(2)
    with c1:
        if st.button("👍 Vote UP", use_container_width=True):
            vote_weighted(pid, st.session_state.get("username", "anon"), "up", species)
            st.rerun()
    with c2:
        if st.button("👎 Vote DOWN", use_container_width=True):
            vote_weighted(
                pid, st.session_state.get("username", "anon"), "down", species
            )
            st.rerun()

    # live tally
    tally = tally_proposal_weighted(pid)
    up, down, total = tally["up"], tally["down"], tally["total"]
    pct = (up / total * 100) if total > 0 else 0.0
    st.markdown(
        f"**Weighted tally:** {up:.3f} ↑ / {down:.3f} ↓ — total {total:.3f}  "
        f"(**{pct:.1f}% yes**)",
    )

    with st.expander("Breakdown"):
        st.write("Per-voter weights:", tally.get("per_voter_weights", {}))
        st.write("Counts by species:", tally.get("counts", {}))
        st.write("Raw votes:", list_weighted_votes(pid))


# Streamlit entry
def main():
    render()


if __name__ == "__main__":
    main()
