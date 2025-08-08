"""Karma metrics page."""
from __future__ import annotations

import streamlit as st


def main() -> None:
    """Render a simple karma page placeholder."""
    st.title("Karma")
    use_backend = st.toggle("Enable backend", key="karma_backend_toggle")
    if use_backend:
        st.info("Backend integration coming soon.")
    else:
        st.info("Backend disabled.")


if __name__ == "__main__":
    main()
