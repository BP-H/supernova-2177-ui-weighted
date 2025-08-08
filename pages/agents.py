from __future__ import annotations

import json
import os
import time
import streamlit as st

from api_key_input import read_openai_key

PAGE = "agents"  # unique prefix for widget keys on this page

# Try to import the client; show a friendly hint if missing
CLIENT_OK = True
try:
    from services.supernova_client import (
        health,
        status,
        entropy_details,
        predictions,
        quantum,
        network,
        sim_negentropy,
        sim_entangle,
        create_vibenode,
        remix,
        like,
        vote,
        tally,
        decide_vote,
        fork as api_fork,
        ai_assist,
    )
except Exception as _e:
    CLIENT_OK = False


def _header():
    st.title("🤖 Agents")
    st.caption("After connecting, Agents can analyze, create, remix, react, vote, and even fork universes. "
               "All metrics here are *symbolic* — this is strictly a social media framework.")


def _api_key_form():
    with st.form(f"{PAGE}_api_form"):
        key_input = st.text_input(
            "OpenAI API key",
            value=read_openai_key(),
            type="password",
            placeholder="sk-...",
            key=f"{PAGE}_openai_api_key_v2",
        )
        saved = st.form_submit_button("Save")
    if saved:
        st.session_state["openai_api_key"] = key_input.strip()
        os.environ["OPENAI_API_KEY"] = st.session_state["openai_api_key"]
        if key_input.strip():
            st.success("Saved. Agents will use this key.")
        else:
            st.warning("No API key provided; OpenAI-powered agents are disabled.")
    st.caption(
        "Tip: you can also set this in `.streamlit/secrets.toml` as "
        '`openai_api_key = "sk-..."`'
    )


def _connection():
    st.subheader("Connection")
    if not CLIENT_OK:
        st.error("`services/supernova_client.py` not found or has import errors. "
                 "Create it (see patch) and rerun.")
        return False, ""
    ok = False
    try:
        ok = health()
    except Exception:
        ok = False
    st.info("Backend online ✅" if ok else "Backend offline ❌")
    token = st.text_input("Bearer token (JWT)", type="password", placeholder="eyJ...", key=f"{PAGE}_jwt_v2")
    return ok, token


def _analyze_section(backend_ok: bool, token: str):
    st.subheader("Analyze")
    if st.button("Analyze ecosystem", key=f"{PAGE}_analyze_btn", disabled=not backend_ok):
        try:
            s   = status()
            ent = entropy_details(token)
            pred= predictions()
            q   = quantum()
            net = network(token)
            neg = sim_negentropy(token)
            st.success("Analysis complete.")
            st.json({
                "status": s,
                "entropy": ent,
                "predictions": pred,
                "quantum": q,
                "network": net.get("metrics", {}),
                "negentropy": neg,
            })
            H = float(ent.get("current_entropy", 0.0))
            suggestions = []
            if H > 1100:
                suggestions.append("Entropy high → Mint 1–3 Originals with focused tags.")
            if net.get("metrics", {}).get("density", 0.0) < 0.02:
                suggestions.append("Graph sparse → React-blast a few posts to bind the network.")
            if pred.get("prediction"):
                suggestions.append("Validate 1 prediction via the experiments list.")
            st.write("**Suggestions**")
            for sline in suggestions or ["Looks stable. Try a creative Remix."]:
                st.write("• " + sline)
        except Exception as e:
            st.error(f"Analyze failed: {e}")


def _create_remix_react_section(backend_ok: bool, token: str):
    st.subheader("Create / Remix / React")
    c1, c2 = st.columns([2, 1])
    with c1:
        title = st.text_input("Title", value="New Dawn", key=f"{PAGE}_title_v2")
        desc = st.text_area("Description", value="A short, uplifting post about cooperative order.",
                            key=f"{PAGE}_desc_v2")
        tags_txt = st.text_input("Tags (comma)", value="harmony,order,remix", key=f"{PAGE}_tags_v2")
        tags = [t.strip() for t in tags_txt.split(",") if t.strip()]
    with c2:
        parent_id = st.number_input("Remix parent VibeNode ID (optional)", value=0, step=1, key=f"{PAGE}_parent_v2")
        react_id = st.number_input("React (👍) VibeNode ID", value=1, step=1, key=f"{PAGE}_react_id_v2")

    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        if st.button("Mint Original", key=f"{PAGE}_mint_btn", disabled=not backend_ok):
            try:
                res = create_vibenode(token, {
                    "name": title,
                    "description": desc,
                    "media_type": "text",
                    "tags": tags,
                })
                st.success(f"Minted VibeNode #{res.get('id')}")
            except Exception as e:
                st.error(f"Mint failed: {e}")
    with cc2:
        if st.button("Remix Parent", key=f"{PAGE}_remix_btn",
                     disabled=(not backend_ok) or (int(parent_id) <= 0)):
            try:
                res = remix(token, int(parent_id), {
                    "name": f"{title} (Remix)",
                    "description": desc + "\n\nRemix: clarifies structure and adds new tag taxonomy.",
                })
                st.success(f"Remixed as VibeNode #{res.get('id')}")
            except Exception as e:
                st.error(f"Remix failed: {e}")
    with cc3:
        if st.button("React (👍)", key=f"{PAGE}_react_btn", disabled=not backend_ok):
            try:
                st.json(like(token, int(react_id)))
                st.success("Reaction sent")
            except Exception as e:
                st.error(f"React failed: {e}")


def _ai_assist_section(backend_ok: bool, token: str):
    st.subheader("AI Assist (persona-linked nodes)")
    aid = st.number_input("VibeNode ID (with patron_saint_id)", value=0, step=1, key=f"{PAGE}_assist_id_v2")
    prompt = st.text_input("Prompt", value="Suggest a better title and 5 tags.", key=f"{PAGE}_assist_prompt_v2")
    if st.button("Ask Persona", key=f"{PAGE}_assist_btn", disabled=(not backend_ok) or (int(aid) <= 0)):
        try:
            st.json(ai_assist(token, int(aid), prompt))
        except Exception as e:
            st.error(f"AI Assist failed: {e}")


def _governance_section(backend_ok: bool):
    st.subheader("Governance (Weighted)")
    st.caption("Uses `/api/votes/*` routes. If you didn’t mount the router yet, these will 404.")
    pid = st.number_input("Proposal ID", value=1, step=1, key=f"{PAGE}_pid_v2")
    voter = st.text_input("Voter handle", value="agent_ops", key=f"{PAGE}_voter_v2")
    species = st.selectbox("Species", ["human", "company", "ai"], key=f"{PAGE}_species_v2")
    level = st.selectbox("Decision level", ["standard", "important"], key=f"{PAGE}_level_v2")

    gc1, gc2, gc3 = st.columns(3)
    with gc1:
        if st.button("Vote YES", key=f"{PAGE}_vote_yes", disabled=not backend_ok):
            try:
                st.json(vote(int(pid), voter, "yes", species))
            except Exception as e:
                st.error(f"Vote failed (likely router not mounted): {e}")
    with gc2:
        if st.button("Tally", key=f"{PAGE}_tally", disabled=not backend_ok):
            try:
                st.json(tally(int(pid)))
            except Exception as e:
                st.error(f"Tally failed: {e}")
    with gc3:
        if st.button("Decide", key=f"{PAGE}_decide", disabled=not backend_ok):
            try:
                st.json(decide_vote(int(pid), level))
            except Exception as e:
                st.error(f"Decide failed: {e}")


def _fork_section(backend_ok: bool, token: str):
    st.subheader("Fork Universe")
    st.caption("POST /api/fork (custom config). If not mounted yet, this will 404.")
    cfg = st.text_area("Custom config (JSON)", value='{"DAILY_DECAY":"0.985","entropy_threshold":1200}',
                       key=f"{PAGE}_fork_cfg_v2")
    if st.button("Fork", key=f"{PAGE}_fork_btn", disabled=(not backend_ok) or (not token)):
        try:
            data = json.loads(cfg) if cfg.strip() else {}
            st.json(api_fork(token, data))
        except Exception as e:
            st.error(f"Fork failed (likely router not mounted or bad JSON): {e}")


def render() -> None:
    _header()
    _api_key_form()
    backend_ok, token = _connection()
    _analyze_section(backend_ok, token)
    _create_remix_react_section(backend_ok, token)
    _ai_assist_section(backend_ok, token)
    _governance_section(backend_ok)
    _fork_section(backend_ok, token)


def main() -> None:
    render()


if __name__ == "__main__":
    main()
