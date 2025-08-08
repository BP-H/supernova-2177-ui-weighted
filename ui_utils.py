# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Utility functions for streamlit UIs."""

from pathlib import Path
import streamlit as st
from streamlit_helpers import inject_global_styles
from modern_ui_components import render_modern_header, render_modern_sidebar


def summarize_text(text: str, max_len: int = 150) -> str:
    """Basic text summarizer placeholder."""
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def parse_summary(text: str) -> str:
    """Extract the summary section from an RFC markdown text."""
    if "## Summary" not in text:
        return ""
    part = text.split("## Summary", 1)[1]
    lines = []
    for line in part.splitlines()[1:]:
        if line.startswith("##"):
            break
        if line.strip():
            lines.append(line.strip())
    return " ".join(lines)


@st.cache_data
def load_rfc_entries(rfc_dir: Path):
    """Return list and index of RFC entries from a directory."""
    rfc_paths = sorted(rfc_dir.rglob("rfc-*.md"))
    rfc_entries = []
    rfc_index = {}
    for path in rfc_paths:
        text = path.read_text()
        summary = parse_summary(text)
        entry = {
            "id": path.stem,
            "summary": summary,
            "text": text,
            "path": path,
        }
        rfc_entries.append(entry)
        rfc_index[path.stem.lower()] = entry
    return rfc_entries, rfc_index


def render_main_ui() -> None:
    """Render a minimal placeholder for the Streamlit dashboard."""
    inject_global_styles()
    st.title("superNova_2177")
    st.write("UI initialization complete.")


def render_modern_layout() -> None:
    """Demo layout showcasing the modern styles."""
    inject_global_styles()

    pages = {"Home": "home", "Feed": "feed", "Profile": "profile"}
    choice = render_modern_sidebar(
        pages,
        icons={"Home": "🏠", "Feed": "📰", "Profile": "👤"},
        session_key="demo_nav",
    )

    render_modern_header("NovaNet 🚀")

    with st.container():
        st.markdown(
            "<div class='custom-container'>Welcome to the next-gen network.</div>",
            unsafe_allow_html=True,
        )
        st.button("Primary Action", key="primary_btn")


__all__ = [
    "summarize_text",
    "parse_summary",
    "load_rfc_entries",
    "render_main_ui",
    "render_modern_layout",
    "render_modern_sidebar",
    "render_modern_header",
]
