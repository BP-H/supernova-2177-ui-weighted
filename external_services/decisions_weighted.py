# pages/decisions_weighted.py
from __future__ import annotations
import streamlit as st
from external_services.fake_api_weighted import (
    tally_proposal_weighted,
    decide_weighted_api,
    get_threshold,
)

def _list_proposals():
    try:
        from external_services.fake_api import list_proposals
        return list_proposals()
    except Exception:
        return []

def render():
    st.title("✅ Decisions (Weighted)")

    kind = st.session_state.get("decision_kind", "standard")
    thr = get_threshold(kind)
    st.caption(
        f"{kind.title()} decisions require {int(thr*100)}% yes (weighted)"
    )
    props = _list_proposals()

    if props:
        for p in props:
            pid = int(p.get("id"))
            title = p.get("title", f"Proposal {pid}")
            st.subheader(f"#{pid} — {title}")

            tally = tally_proposal_weighted(pid)
            up, down, total = tally["up"], tally["down"], tally["total"]
            pct = (up / total * 100) if total > 0 else 0.0
            st.markdown(f"**Weighted tally:** {up:.3f} ↑ / {down:.3f} ↓ — total {total:.3f}  (**{pct:.1f}% yes**)")

            if st.button(f"Decide (weighted) #{pid}", key=f"wdec_{pid}"):
                res = decide_weighted_api(pid, kind)
                st.success(
                    f"Decision: **{res.get('status','?').upper()}** ({kind}) — threshold: {int(res['threshold']*100)}%"
                )
            st.divider()
    else:
        st.info("No proposals listed by backend. Enter a Proposal ID to test.")
        pid = st.number_input("Proposal ID", min_value=1, value=1, step=1)
        tally = tally_proposal_weighted(pid)
        up, down, total = tally["up"], tally["down"], tally["total"]
        pct = (up / total * 100) if total > 0 else 0.0
        st.markdown(f"**Weighted tally:** {up:.3f} ↑ / {down:.3f} ↓ — total {total:.3f}  (**{pct:.1f}% yes**)")
        if st.button("Decide (weighted)"):
            res = decide_weighted_api(pid, kind)
            st.success(
                f"Decision: **{res.get('status','?').upper()}** ({kind}) — threshold: {int(res['threshold']*100)}%"
            )

def main():
    render()

if __name__ == "__main__":
    main()
