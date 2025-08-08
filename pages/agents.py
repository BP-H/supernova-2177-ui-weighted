# pages/agents.py
from __future__ import annotations
import os
import streamlit as st

from utils.api_keys import get_api_key

PAGE = "agents"  # prefix so all widget keys on this page are unique


def _default_openai_key() -> str:
    """Prefer session -> secrets/env via helper; never crash if missing."""
    val = st.session_state.get("openai_api_key_v2")
    if isinstance(val, str) and val.strip():
        return val.strip()
    return get_api_key("OPENAI_API_KEY")


def render() -> None:
    st.title("🤖 Agents")

    with st.form(f"{PAGE}_api_form"):
        key_input = st.text_input(
            "OpenAI API key",
            value=_default_openai_key(),
            type="password",
            placeholder="sk-...",
            key=f"{PAGE}_openai_api_key_v2",  # ensure unique key
        )
        saved = st.form_submit_button("Save")

    if saved:
        st.session_state["openai_api_key_v2"] = key_input.strip()
        os.environ["OPENAI_API_KEY"] = st.session_state["openai_api_key_v2"]
        st.success("Saved. Agents will use this key.")

    st.caption(
        "Tip: you can also set this in `.streamlit/secrets.toml` as "
        '`openai_api_key = "sk-..."`'
    )


def main() -> None:
    render()


if __name__ == "__main__":
    main()
