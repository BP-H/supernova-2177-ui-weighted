"""Validators overview page."""
from __future__ import annotations

import streamlit as st


def main() -> None:
    """Render a placeholder validators page."""
    st.title("Validators")
    st.write("Validator metrics placeholder.")
    use_backend = st.toggle("Enable backend", key="validators_backend_toggle")
    if use_backend:
        st.info("Backend integration coming soon.")
    else:
        st.info("Backend disabled.")


if __name__ == "__main__":
    main()
