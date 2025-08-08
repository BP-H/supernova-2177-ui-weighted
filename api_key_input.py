# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Reusable helpers for API key input in the Streamlit UI."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Optional

try:
    import streamlit as st
except Exception:  # pragma: no cover - streamlit not available
    st = None  # type: ignore

from causal_graph import InfluenceGraph

# Mapping of display name -> (model identifier, session_state key)
PROVIDERS = {
    "Dummy": ("dummy", None),
    "GPT-4o (OpenAI)": ("gpt-4o", "OPENAI_API_KEY"),
    "Claude-3 (Anthropic)": ("claude-3", "ANTHROPIC_API_KEY"),
    "Gemini (Google)": ("gemini", "GOOGLE_API_KEY"),
    "Mixtral (Groq)": ("mixtral", "GROQ_API_KEY"),
}


def read_openai_key() -> str:
    """Return the OpenAI API key from session, secrets, or environment."""

    key = ""
    if st is not None:
        session_val = st.session_state.get("OPENAI_API_KEY") or st.session_state.get(
            "openai_api_key"
        )
        if isinstance(session_val, str) and session_val.strip():
            key = session_val.strip()
        else:
            try:
                secret_val = st.secrets.get("OPENAI_API_KEY") or st.secrets.get(
                    "openai_api_key"
                )
                if isinstance(secret_val, str) and secret_val.strip():
                    key = secret_val.strip()
            except Exception:
                pass
    if not key:
        key = os.environ.get("OPENAI_API_KEY", "").strip()
    return key


def render_api_key_ui(
    default: str = "Dummy",
    *,
    key_prefix: str = "main",
) -> dict[str, str | None | bool]:
    """Render model selection and API key fields with unique widget keys.

    Parameters
    ----------
    default : str
        The provider name to pre-select in the dropdown.
    key_prefix : str
        Prefix used to ensure widget keys are unique when this
        component is rendered multiple times on a page.

    Returns
    -------
    dict[str, str | None | bool]
        Dictionary containing ``model``, ``api_key`` and a ``disabled`` flag.
    """
    if st is None:
        return {"model": "dummy", "api_key": None, "disabled": False}


    names = list(PROVIDERS.keys())
    if default in names:
        index = names.index(default)
    else:
        index = 0
    prefix = f"{key_prefix}_" if key_prefix else ""

    choice = st.selectbox("LLM Model", names, index=index, key=f"{prefix}model")
    model, key_name = PROVIDERS[choice]
    key_val = ""
    disabled = False
    actual_key: str | None = None
    if key_name is not None:
        default_val = read_openai_key() if key_name == "OPENAI_API_KEY" else os.getenv(key_name, "")
        key_val = st.text_input(
            f"{choice} API Key",
            type="password",
            value=st.session_state.get(key_name, default_val),
            key=f"{prefix}{model}_api_key_v2",
        )
        actual_key = (key_val or st.session_state.get(key_name) or default_val).strip()
        if key_val:
            st.session_state[key_name] = key_val.strip()
        if not actual_key:
            st.warning(f"{choice} API key missing; related actions disabled.")
            disabled = True
    st.session_state["selected_model"] = model
    return {"model": model, "api_key": actual_key, "disabled": disabled}


def record_simulation_event(
    session: dict,
    source: str,
    target: str,
    edge_type: str,
    timestamp: Optional[str] = None,
) -> InfluenceGraph:
    """Store an interaction and return the updated graph."""
    graph: InfluenceGraph = session.setdefault("simulation_graph", InfluenceGraph())
    events = session.setdefault("simulation_events", [])

    try:
        ts = datetime.fromisoformat(timestamp) if timestamp else datetime.utcnow()
    except Exception:
        ts = datetime.utcnow()

    graph.add_interaction(source, target, edge_type=edge_type, timestamp=ts)
    events.append({"source": source, "target": target, "edge_type": edge_type, "timestamp": ts})
    return graph


def render_simulation_stubs() -> None:
    """Interactive form to capture simple simulation events."""
    if st is None:
        return

    st.session_state.setdefault("simulation_graph", InfluenceGraph())
    st.session_state.setdefault("simulation_events", [])

    with st.expander("Simulation Event Input", expanded=False):
        with st.form("sim_event_form"):
            source = st.text_input("Source Node ID")
            target = st.text_input("Target Node ID")
            edge_type = st.text_input("Edge Type", value="follow")
            ts_str = st.text_input("Timestamp (ISO)", value=datetime.utcnow().isoformat())
            submitted = st.form_submit_button("Add Event")
        if submitted:
            record_simulation_event(st.session_state, source, target, edge_type, ts_str)
            st.success("Event recorded")

        graph: InfluenceGraph = st.session_state["simulation_graph"]
        if graph.graph.number_of_edges() > 0:
            try:
                import networkx as nx  # type: ignore
                import matplotlib.pyplot as plt  # type: ignore

                fig, ax = plt.subplots()
                pos = nx.spring_layout(graph.graph)
                nx.draw_networkx(graph.graph, pos=pos, ax=ax)
                st.pyplot(fig)
            except Exception:
                st.toast("Install networkx and matplotlib for graph display")

        trace_id = st.text_input("Trace Node", key="trace_node")
        if trace_id:
            st.write("Ancestors", graph.trace_to_ancestors(trace_id, max_depth=3))
            st.write("Descendants", graph.trace_to_descendants(trace_id, max_depth=3))

