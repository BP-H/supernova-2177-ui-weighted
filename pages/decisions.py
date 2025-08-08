# pages/decisions.py
from __future__ import annotations
import json
import os
import urllib.request
import streamlit as st


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
    def list_proposals(): return []
    def tally_proposal(pid): return {"up": 0, "down": 0}
    def decide(pid, threshold=0.6): return {"proposal_id": pid, "status": "rejected"}
    def list_decisions(): return []


# ----------------------- main UI -----------------------
def _standard_decisions_block() -> None:
    st.subheader("Decisions")
    st.caption("Rule: accept when 👍 / (👍+👎) ≥ 60% (and at least 1 vote).")

    proposals = _get("/proposals") if _use_backend() else list_proposals()
    for p in proposals:
        pid = p["id"]
        tally = _get(f"/proposals/{pid}/tally") if _use_backend() else tally_proposal(pid)
        up, down = int(tally.get("up", 0)), int(tally.get("down", 0))
        total = up + down
        pct = (up / total * 100) if total else 0.0

        st.write(f"**{p['title']}** — {up} 👍 / {down} 👎  ({pct:.0f}%)")
        if st.button(f"Compute decision for #{pid}", key=f"dec_{pid}"):
            res = _post(f"/decide/{pid}", {}) if _use_backend() else decide(pid)
            st.success(f"Decision: {str(res.get('status', 'unknown')).upper()}")


# ---------------- weighted (superNova_2177) -------------
# Try both casings so we don't break either file name.
try:
    from superNova_2177 import tally_proposal_weighted, decide_weighted_api, get_threshold
except Exception:
    try:
        from supernova_2177 import tally_proposal_weighted, decide_weighted_api, get_threshold  # type: ignore
    except Exception:
        # very safe stubs so the page keeps working if the module is missing
        def tally_proposal_weighted(pid: int):
            return {"up": 0.0, "down": 0.0, "total": 0.0}
        def decide_weighted_api(pid: int, level: str):
            return {"status": "rejected", "threshold": 0.6}
        def get_threshold(level: str) -> float:
            return 0.9 if level == "important" else 0.6


def _weighted_decisions_block() -> None:
    st.subheader("Weighted decisions (Humans / Companies / AI)")
    kind = st.session_state.get("decision_kind", "standard")
    thr = get_threshold(kind)
    st.caption(
        f"{kind.title()} decisions require {int(thr * 100)}% threshold (weighted by species pool)"
    )

    proposals = _get("/proposals") if _use_backend() else list_proposals()
    for p in proposals:
        pid = p["id"]
        with st.expander(f"Proposal #{pid}: {p['title']}", expanded=False):
            t = tally_proposal_weighted(pid)
            total = float(t.get("total", 0.0)) or 0.0
            up = float(t.get("up", 0.0))
            down = float(t.get("down", 0.0))
            pct = (up / total * 100.0) if total else 0.0
            st.caption(
                f"Weighted tally: {up:.3f} ↑ / {down:.3f} ↓ — total {total:.3f}  ({pct:.1f}% yes)"
            )

            if st.button(f"Decide (weighted) #{pid}", key=f"wdec_{pid}"):
                res = decide_weighted_api(pid, kind)
                status = str(res.get("status", "unknown")).upper()
                st.success(
                    f"{status} ({kind}) at {int(res.get('threshold', thr) * 100)}% threshold"
                )


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
