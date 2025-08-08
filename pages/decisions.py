# pages/decisions.py
from __future__ import annotations
import json
import os
import urllib.request
import streamlit as st
from services import voting_adapter


# ----------------------- helpers -----------------------
def _use_backend() -> bool:
    return os.getenv("USE_REAL_BACKEND", "0").lower() in {"1", "true", "yes"}


def _burl() -> str:
    return os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


def _get(path: str):
    with urllib.request.urlopen(_burl() + path) as r:
        return json.loads(r.read().decode("utf-8"))


def _post(path: str, payload: dict):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        _burl() + path, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


# Fallback to fake API if real isn’t available
try:
    from external_services.fake_api import (
        list_proposals,
        tally_proposal,
        decide,
        list_decisions,
    )
except Exception:

    def list_proposals():
        return []

    def tally_proposal(pid):
        return {"up": 0, "down": 0}

    def decide(pid, threshold=0.6):
        return {"proposal_id": pid, "status": "rejected"}

    def list_decisions():
        return []


# ----------------------- main UI -----------------------
def _standard_decisions_block() -> None:
    st.subheader("Decisions")
    st.caption("Rule: accept when 👍 / (👍+👎) ≥ 60% (and at least 1 vote).")

    proposals = _get("/proposals") if _use_backend() else list_proposals()
    for p in proposals:
        pid = p["id"]
        tally = (
            _get(f"/proposals/{pid}/tally") if _use_backend() else tally_proposal(pid)
        )
        up, down = int(tally.get("up", 0)), int(tally.get("down", 0))
        total = up + down
        pct = (up / total * 100) if total else 0.0

        st.write(f"**{p['title']}** — {up} 👍 / {down} 👎  ({pct:.0f}%)")
        if st.button(f"Compute decision for #{pid}", key=f"dec_{pid}"):
            res = _post(f"/decide/{pid}", {}) if _use_backend() else decide(pid)
            st.success(f"Decision: {str(res.get('status', 'unknown')).upper()}")


# ---------------- weighted voting -----------------------


def _weighted_decisions_block() -> None:
    st.subheader("Weighted decisions (Humans / Companies / AI)")
    st.caption(
        "Important=90% threshold · Standard=60% threshold (weighted by species pool)"
    )

    proposals = _get("/proposals") if _use_backend() else list_proposals()
    for p in proposals:
        pid = p["id"]
        with st.expander(f"Proposal #{pid}: {p['title']}", expanded=False):
            t = voting_adapter.tally_votes(pid)
            total = float(t.get("total", 0.0)) or 0.0
            up = float(t.get("up", 0.0))
            down = float(t.get("down", 0.0))
            pct = (up / total * 100.0) if total else 0.0
            st.caption(
                f"Weighted tally: {up:.3f} ↑ / {down:.3f} ↓ — total {total:.3f}  "
                f"({pct:.1f}% yes)"
            )

            level = st.selectbox(
                "Decision level",
                ["standard", "important"],
                index=0,
                key=f"weighted_level_{pid}",
            )
            if st.button(f"Decide (weighted) #{pid}", key=f"wdec_{pid}"):
                res = voting_adapter.decide_vote(pid, level)
                status = str(res.get("status", "unknown")).upper()
                thr = float(res.get("threshold", 0.6))
                st.success(f"{status} at {int(thr * 100)}% threshold")


def main() -> None:
    _standard_decisions_block()
    st.divider()
    _weighted_decisions_block()

    st.divider()
    st.markdown("### Decisions log")
    out = _get("/decisions") if _use_backend() else list_decisions()
    for d in out:
        st.write(f"#{d['id']} — proposal {d['proposal_id']} → **{d['status']}**")


def render() -> None:
    main()


if __name__ == "__main__":
    main()
