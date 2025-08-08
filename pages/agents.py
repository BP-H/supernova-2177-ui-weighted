# pages/agents.py
from __future__ import annotations

import os
import streamlit as st

from api_key_input import read_openai_key

PAGE = "agents"  # prefix so all widget keys on this page are unique


def render() -> None:
    st.title("🤖 Agents")

    with st.form(f"{PAGE}_api_form"):
        key_input = st.text_input(
            "OpenAI API key",
            value=read_openai_key(),
            type="password",
            placeholder="sk-...",
            key=f"{PAGE}_openai_api_key_v2",  # unique key with suffix
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


def main() -> None:
    render()


if __name__ == "__main__":
    main()
