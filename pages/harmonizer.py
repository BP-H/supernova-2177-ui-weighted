from __future__ import annotations

import streamlit as st

from services.harmonizer_adapter import harmonize


def main() -> None:
    """Simple interface for the text harmonizer."""
    st.markdown("### Harmonizer")

    # Respect global species selector without redefining it
    species = st.session_state.get("species", "human")
    st.caption(f"Active species: {species}")

    text = st.text_area("Text to harmonize", key="harmonizer_input")

    col1, col2 = st.columns(2)
    with col1:
        mode = st.selectbox(
            "Mode", ["standard", "gentle", "intense"], key="harmonizer_mode"
        )
    with col2:
        intensity = st.slider("Intensity", 0.0, 1.0, 0.5, key="harmonizer_intensity")

    if st.button("Harmonize", key="harmonize_btn"):
        result = harmonize(text, mode=mode, intensity=float(intensity))
        if result.get("available"):
            st.success(result.get("output", ""))
        else:
            st.warning("Harmonizer service unavailable; showing original text.")
            st.text(result.get("output", text))


if __name__ == "__main__":
    main()
