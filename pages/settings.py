"""Settings page with editable profile fields."""

from __future__ import annotations

import streamlit as st

from profile_adapter import update_profile_adapter


def main() -> None:
    """Render the settings UI allowing profile edits."""
    st.markdown("### Settings")
    st.write(
        "Customize your experience here. (Placeholder – more options coming soon!)"
    )

    # Backend toggle stored in local variable
    use_backend = st.toggle("Enable backend", key="settings_use_backend")

    with st.form("profile_form"):
        bio = st.text_area("Bio", max_chars=280)
        prefs_raw = st.text_input("Cultural Preferences (comma-separated)")
        submitted = st.form_submit_button("Save Profile")

    if submitted:
        prefs = [p.strip() for p in prefs_raw.split(",") if p.strip()]
        result = update_profile_adapter(bio, prefs, use_backend=use_backend)
        if not result.get("available", True):
            st.warning("Profile service unavailable.")
        else:
            status = result.get("status")
            if status == "ok":
                st.success("Profile updated successfully")
            elif status == "stubbed":
                st.info("Profile updated (stub)")
            else:
                st.error(f"Update failed: {result.get('error', 'unknown error')}")


if __name__ == "__main__":
    main()
