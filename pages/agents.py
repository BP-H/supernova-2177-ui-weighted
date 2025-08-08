# inside pages/agents.py render()

import json, time
import streamlit as st
from api_key_input import read_openai_key
from services.supernova_client import (
    health, status, entropy_details, predictions, quantum, network,
    sim_negentropy, sim_entangle, create_vibenode, remix, like, vote, tally,
    decide_vote, fork, ai_assist
)

st.subheader("Connection")
backend_ok = health()
st.info("Backend online ✅" if backend_ok else "Backend offline ❌")
disabled = not backend_ok

st.subheader("Analyze")
token = st.text_input("Bearer token (JWT)", type="password", placeholder="eyJ...", key="agents_jwt_v2")
if st.button("Analyze ecosystem", disabled=disabled):
    try:
        s   = status()
        ent = entropy_details(token)
        pred= predictions()
        q   = quantum()
        net = network(token)
        neg = sim_negentropy(token)
        st.success("Analysis complete.")
        st.json({"status": s, "entropy": ent, "predictions": pred, "quantum": q, "network": net["metrics"], "negentropy": neg})
        # Tiny suggestion heuristic:
        H = ent.get("current_entropy", 0.0)
        sug = []
        if H > 1100: sug.append("Entropy high → Mint 1–3 Originals with focused tags.")
        if net.get("metrics", {}).get("density", 0) < 0.02: sug.append("Graph sparse → React-blast top posts to bind the network.")
        if q.get("decoherence_rate", 0) > 0.5: sug.append("Toggle fuzzy mode off or create soothing music via Resonance.")
        if pred.get("prediction"): sug.append("Validate 1 prediction via experiments.")
        st.write("**Suggestions**")
        for sline in sug or ["Looks stable. Remix something fun."]:
            st.write("• " + sline)
    except Exception as e:
        st.error(f"Analyze failed: {e}")

st.subheader("Create / Remix")
title = st.text_input("Title", value="New Dawn")
desc = st.text_area("Description", value="A short, uplifting post about cooperative order.")
tags = st.text_input("Tags (comma)", value="harmony,order,remix").split(",")
parent_id = st.number_input("Remix parent VibeNode ID (optional)", value=0, step=1)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Mint Original", disabled=disabled):
        try:
            res = create_vibenode(token, {"name": title, "description": desc, "media_type": "text", "tags": [t.strip() for t in tags if t.strip()]})
            st.success(f"Minted VibeNode #{res['id']}")
        except Exception as e:
            st.error(f"Mint failed: {e}")
with col2:
    if st.button("Remix Parent", disabled=disabled or parent_id<=0):
        try:
            res = remix(token, int(parent_id), {"name": f"{title} (Remix)", "description": desc + "\n\nRemix: introduces clearer structure and new tag taxonomy."})
            st.success(f"Remixed as VibeNode #{res['id']}")
        except Exception as e:
            st.error(f"Remix failed: {e}")
with col3:
    top_like_id = st.number_input("React-blast a VibeNode ID", value=1, step=1, key="react_id_v2")
    if st.button("React (👍)", disabled=disabled):
        try:
            st.write(like(token, int(top_like_id)))
            st.success("Reaction sent")
        except Exception as e:
            st.error(f"React failed: {e}")

st.subheader("AI Assist (persona-linked nodes)")
assist_id = st.number_input("VibeNode ID (with patron_saint_id)", value=0, step=1, key="assist_id_v2")
assist_prompt = st.text_input("Prompt", value="Suggest a better title and 5 tags.")
if st.button("Ask Persona", disabled=disabled or assist_id<=0):
    try:
        st.json(ai_assist(token, int(assist_id), assist_prompt))
    except Exception as e:
        st.error(f"AI Assist failed: {e}")

st.subheader("Governance (Weighted)")
pid = st.number_input("Proposal ID", value=1, step=1, key="pid_v2")
voter = st.text_input("Voter handle", value="agent_ops")
species = st.selectbox("Species", ["human","company","ai"])
lv = st.selectbox("Decision level", ["standard","important"])
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Vote YES", disabled=disabled): st.json(vote(int(pid), voter, "yes", species))
with c2:
    if st.button("Tally", disabled=disabled): st.json(tally(int(pid)))
with c3:
    if st.button("Decide", disabled=disabled): st.json(decide_vote(int(pid), lv))

st.subheader("Fork Universe")
cfg = st.text_area("Custom config (JSON)", value='{"DAILY_DECAY":"0.985","entropy_threshold":1200}')
if st.button("Fork", disabled=disabled or not token):
    try:
        st.json(fork(token, json.loads(cfg)))
    except Exception as e:
        st.error(f"Fork failed: {e}")
