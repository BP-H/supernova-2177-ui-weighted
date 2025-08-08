# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""System status metrics page."""

from __future__ import annotations

import streamlit as st

from system_status_adapter import get_status


def main() -> None:
    """Render system status metrics using Streamlit widgets."""
    use_backend = st.toggle("Enable backend", value=True, key="sys_status_toggle")
    data = get_status() if use_backend else {"available": False}
    if not data.get("available") or "metrics" not in data:
        st.warning("Backend disabled or unavailable.")
        st.metric("Harmonizers", "N/A")
        st.metric("VibeNodes", "N/A")
        st.metric("Entropy", "N/A")
    else:
        metrics = data.get("metrics", {})
        st.metric("Harmonizers", metrics.get("total_harmonizers", 0))
        st.metric("VibeNodes", metrics.get("total_vibenodes", 0))
        st.metric("Entropy", metrics.get("current_system_entropy", 0))


def render() -> None:
    main()


async def status_page() -> None:
    """NiceGUI-compatible async wrapper."""
    main()


if __name__ == "__main__":
    main()
