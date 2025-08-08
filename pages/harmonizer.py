# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Interactive text harmonizer page."""

from __future__ import annotations

import streamlit as st
from frontend.theme import apply_theme
from streamlit_helpers import theme_toggle, inject_global_styles

try:  # pragma: no cover - adapter may be missing
    import harmonizer_adapter

    BACKEND_AVAILABLE = not getattr(harmonizer_adapter, "OFFLINE_MODE", False)
except Exception:  # pragma: no cover - missing backend
    harmonizer_adapter = None  # type: ignore
    BACKEND_AVAILABLE = False

apply_theme("light")
inject_global_styles()


def main() -> None:
    """Render harmonizer controls and output."""
    theme_toggle("Dark Mode", key_suffix="harmonizer")

    text = st.text_area("Input", key="harmonizer_input")
    mode = st.selectbox("Mode", ["soft", "balanced", "intense"], key="harmonizer_mode")
    intensity = st.slider("Intensity", 1, 10, 5, key="harmonizer_intensity")

    if not BACKEND_AVAILABLE:
        st.warning("Harmonizer backend unavailable.")

    if st.button("Harmonize", key="harmonize_btn", disabled=not BACKEND_AVAILABLE):
        try:
            result = harmonizer_adapter.harmonize(  # type: ignore[union-attr]
                text=text, mode=mode, intensity=intensity
            )
            output = (
                result.get("output", "") if isinstance(result, dict) else str(result)
            )
            stats = result.get("stats", {}) if isinstance(result, dict) else {}
            st.text_area("Output", output, key="harmonizer_output")
            if stats:
                st.json(stats)
        except Exception as exc:  # pragma: no cover - runtime errors
            st.error(f"Failed to harmonize: {exc}")


def render() -> None:  # For multipage loaders expecting `render`
    main()


if __name__ == "__main__":
    main()
