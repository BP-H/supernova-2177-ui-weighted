import os
import json
import urllib.request
import streamlit as st
from typing import Dict, Any
from services import voting_adapter


def _use_backend() -> bool:
    return os.getenv("USE_REAL_BACKEND", "0").lower() in {"1", "true", "yes"}


def _burl() -> str:
    return os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


def _get(path: str):
    with urllib.request.urlopen(_burl() + path) as r:
        return json.loads(r.read().decode("utf-8"))


def _post(path: str, payload: Dict[str, Any]):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        _burl() + path, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


# local fallback
try:
    from external_services.fake_api import (
        list_proposals,
        create_proposal,
        vote,
        tally_proposal,
    )
except Exception:

    def list_proposals():
        return []

    def create_proposal(author, title, body):
        return {}

    def vote(pid, voter, choice):
        return {"ok": False}

    def tally_proposal(pid):
        return {"up": 0, "down": 0}


def main():
    st.subheader("Proposals")
    with st.form("new_proposal"):
        title = st.text_input("Title")
        body = st.text_area("Description", height=120)
        submitted = st.form_submit_button("Create")
    if submitted and title.strip():
        if _use_backend():
            _post("/proposals", {"title": title, "body": body, "author": "guest"})
        else:
            create_proposal("guest", title, body)
        st.success("Created")
        st.rerun()

    # list
    items = _get("/proposals") if _use_backend() else list_proposals()
    for p in items:
        with st.container():
            st.markdown(f"### {p['title']}")
            st.write(p.get("body", ""))
            pid = p["id"]
            col1, col2, col3 = st.columns(3)
            if col1.button(f"👍 Upvote #{pid}", key=f"u_{pid}"):
                (
                    _post(
                        "/votes", {"proposal_id": pid, "voter": "guest", "choice": "up"}
                    )
                    if _use_backend()
                    else vote(pid, "guest", "up")
                )
                st.rerun()
            if col2.button(f"👎 Downvote #{pid}", key=f"d_{pid}"):
                (
                    _post(
                        "/votes",
                        {"proposal_id": pid, "voter": "guest", "choice": "down"},
                    )
                    if _use_backend()
                    else vote(pid, "guest", "down")
                )
                st.rerun()
            tally = (
                _get(f"/proposals/{pid}/tally")
                if _use_backend()
                else tally_proposal(pid)
            )
            col3.metric("Votes", f"{tally.get('up',0)} 👍 / {tally.get('down',0)} 👎")


def render():
    main()


# --- WEIGHTED VOTING PANEL (auto-added) --------------------------------------


def _weighted_panel_for_proposal(pid: int):
    import streamlit as st

    species = st.session_state.get("species", "human")
    c1, c2 = st.columns(2)
    with c1:
        if st.button(f"👍 Vote UP (weighted) #{pid}", key=f"wup_{pid}"):
            voting_adapter.register_vote(
                pid, st.session_state.get("username", "anon"), "up", species
            )
            st.rerun()
    with c2:
        if st.button(f"👎 Vote DOWN (weighted) #{pid}", key=f"wdown_{pid}"):
            voting_adapter.register_vote(
                pid, st.session_state.get("username", "anon"), "down", species
            )
            st.rerun()
    t = voting_adapter.tally_votes(pid)
    pct = (t["up"] / t["total"] * 100) if t["total"] else 0.0
    st.caption(
        f"Weighted: {t['up']:.3f} ↑ / {t['down']:.3f} ↓ — total {t['total']:.3f}  "
        f"({pct:.1f}% yes)"
    )


# --- END WEIGHTED VOTING PANEL -----------------------------------------------
