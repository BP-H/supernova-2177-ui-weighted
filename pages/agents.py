from __future__ import annotations
import os, json
import streamlit as st
from api_key_input import read_openai_key
from services.supernova_client import SupernovaClient

PAGE = "agents"  # unique widget prefix

def _header():
    st.title("🤖 Agents")
    st.caption("Connect to your superNova_2177 backend, then analyze, create, remix, react, ask AI, vote, and fork. All metrics are symbolic.")

def _api_key_box():
    with st.form(f"{PAGE}_api_form"):
        key_input = st.text_input("OpenAI API key", value=read_openai_key(), type="password", placeholder="sk-...", key=f"{PAGE}_openai_api_key_v2")
        saved = st.form_submit_button("Save")
    if saved:
        st.session_state["openai_api_key"] = key_input.strip()
        os.environ["OPENAI_API_KEY"] = st.session_state["openai_api_key"]
        st.success("Saved." if key_input.strip() else "Cleared. OpenAI-powered helpers disabled.")
    st.caption('Tip: you can also set `.streamlit/secrets.toml` → openai_api_key = "sk-..."')

def _connect_box():
    st.subheader("Connection")
    backend = st.text_input("Backend URL", value=st.session_state.get("backend_url", "http://127.0.0.1:8000"), key=f"{PAGE}_backend_url")
    st.session_state["backend_url"] = backend.strip()
    token = st.text_input("Bearer token (JWT)", type="password", placeholder="eyJ...", key=f"{PAGE}_jwt")
    client = SupernovaClient(backend, token)
    c1, c2 = st.columns(2)
    if c1.button("Ping /healthz", key=f"{PAGE}_ping"):
        st.json(client.healthz())
    if c2.button("System /status", key=f"{PAGE}_status"):
        st.json(client.status())
    return client

def _analyze_box(client: SupernovaClient):
    st.subheader("Analyze")
    c1, c2, c3 = st.columns(3)
    if c1.button("System predictions", key=f"{PAGE}_pred"):
        st.json(client.system_predictions())
    if c2.button("Quantum status", key=f"{PAGE}_q"):
        st.json(client.quantum_status())
    if c3.button("Entropy details (auth)", key=f"{PAGE}_ent"):
        st.json(client.entropy_details())

def _content_box(client: SupernovaClient):
    st.subheader("Create / Remix / React")
    with st.form(f"{PAGE}_create_form", clear_on_submit=True):
        name = st.text_input("Title", value="New Dawn", key=f"{PAGE}_name")
        desc = st.text_area("Description", value="A short post about cooperative order.", key=f"{PAGE}_desc")
        tags_txt = st.text_input("Tags (comma)", value="harmony,order,remix", key=f"{PAGE}_tags")
        submitted = st.form_submit_button("Mint Original")
        if submitted:
            tags = [t.strip() for t in tags_txt.split(",") if t.strip()]
            st.json(client.create_vibenode(name, desc, tags))
    c1, c2 = st.columns(2)
    with c1:
        pid = st.number_input("Remix parent VibeNode ID", value=0, min_value=0, step=1, key=f"{PAGE}_parent")
        if st.button("Remix parent", key=f"{PAGE}_remix") and pid > 0:
            st.json(client.remix(int(pid), name=f"{pid} remix", description="Adds structure and new tags."))
    with c2:
        like_id = st.number_input("React (👍) VibeNode ID", value=1, min_value=1, step=1, key=f"{PAGE}_like_id")
        if st.button("React 👍", key=f"{PAGE}_react"):
            st.json(client.like(int(like_id)))

def _ai_assist_box(client: SupernovaClient):
    st.subheader("AI Assist (persona-linked nodes)")
    aid = st.number_input("VibeNode ID", value=0, min_value=0, step=1, key=f"{PAGE}_assist_id")
    prompt = st.text_input("Prompt", value="Suggest a better title and 5 tags.", key=f"{PAGE}_assist_prompt")
    if st.button("Ask Persona", key=f"{PAGE}_assist_btn") and int(aid) > 0:
        st.json(client.ai_assist(int(aid), prompt))

def _governance_box(client: SupernovaClient):
    st.subheader("Governance (Weighted)")
    st.caption("If the router isn't mounted yet, these will 404.")
    pid = st.number_input("Proposal ID", value=1, min_value=1, step=1, key=f"{PAGE}_pid")
    voter = st.text_input("Voter handle", value="agent_ops", key=f"{PAGE}_voter")
    species = st.selectbox("Species", ["human","company","ai"], key=f"{PAGE}_species")
    lvl = st.selectbox("Decision level", ["standard","important"], key=f"{PAGE}_level")
    g1, g2, g3 = st.columns(3)
    if g1.button("Vote YES", key=f"{PAGE}_vote_yes"):
        st.json(client.vote(int(pid), voter, "yes", species))
    if g2.button("Tally", key=f"{PAGE}_tally"):
        st.json(client.tally(int(pid)))
    if g3.button("Decide", key=f"{PAGE}_decide"):
        st.json(client.decide(int(pid), lvl))

def _fork_box(client: SupernovaClient):
    st.subheader("Fork Universe")
    cfg = st.text_area("Custom config (JSON)", value='{"DAILY_DECAY":"0.985","entropy_threshold":1200}', key=f"{PAGE}_fork_cfg")
    if st.button("Fork", key=f"{PAGE}_fork_btn"):
        try:
            st.json(client.fork(json.loads(cfg) if cfg.strip() else {}))
        except Exception as e:
            st.error(f"Bad JSON: {e}")

def render() -> None:
    _header()
    _api_key_box()
    client = _connect_box()
    _analyze_box(client)
    _content_box(client)
    _ai_assist_box(client)
    _governance_box(client)
    _fork_box(client)

def main() -> None:
    render()

if __name__ == "__main__":
    main()
