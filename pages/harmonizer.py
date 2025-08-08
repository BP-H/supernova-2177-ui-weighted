"""Harmonizer management page."""
from __future__ import annotations

import streamlit as st


def main() -> None:
    """Render a placeholder harmonizer page."""
    st.title("Harmonizer")
    st.write("Manage harmonizers here. (Placeholder)")
    use_backend = st.toggle("Enable backend", key="harmonizer_backend_toggle")
    if use_backend:
        st.info("Backend integration coming soon.")
    else:
        st.info("Backend disabled.")


if __name__ == "__main__":
    main()
