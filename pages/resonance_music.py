# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Resonance music player and summary viewer."""

from __future__ import annotations

import asyncio
import base64
import os
from typing import Optional
from pathlib import Path

import requests
import streamlit as st
from frontend.theme import apply_theme

from streamlit_helpers import (
    alert,
    centered_container,
    safe_container,
    header,
    theme_toggle,
    inject_global_styles,
)
from streamlit_autorefresh import st_autorefresh
from status_indicator import (
    render_status_icon,
    check_backend,
)
from utils.api import (
    get_resonance_summary,
    dispatch_route,
)
from .widget_keys import (
    page_key,
    RESONANCE_MUSIC_PAGE,
)

# Dedicated keys for this page to avoid collisions across Streamlit pages.
# The `_v2` suffix is added via ``page_key`` to signal the new naming scheme.
STATUS_PING_KEY = page_key(RESONANCE_MUSIC_PAGE, "status_ping")
AMBIENT_LOOP_TOGGLE_KEY = page_key(RESONANCE_MUSIC_PAGE, "ambient_loop_toggle")
PROFILE_SELECT_KEY = page_key(RESONANCE_MUSIC_PAGE, "profile_select")
GENERATE_MUSIC_BTN_KEY = page_key(RESONANCE_MUSIC_PAGE, "generate_music_btn")
FETCH_SUMMARY_BTN_KEY = page_key(RESONANCE_MUSIC_PAGE, "fetch_summary_btn")
SUMMARY_AUDIO_PLAYER_KEY = page_key(
    RESONANCE_MUSIC_PAGE,
    "summary_audio_player",
)

# Initialize theme & global styles once
apply_theme("light")
inject_global_styles()

# BACKEND_URL is defined in utils.api, but we keep it here for direct requests
# if needed.
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
AMBIENT_URL = os.getenv(
    "AMBIENT_MP3_URL",
    "https://raw.githubusercontent.com/anars/blank-audio/master/10-minutes-of-silence.mp3",
)
DEFAULT_AMBIENT_URL = (
    "https://raw.githubusercontent.com/anars/blank-audio/master/"
    "10-seconds-of-silence.mp3"
)


def _load_ambient_audio() -> Optional[bytes]:
    """Return ambient MP3 bytes from local file or remote URL."""
    local = Path("ambient_loop.mp3")
    if local.exists():
        try:
            return local.read_bytes()
        except Exception:
            pass
    try:
        resp = requests.get(DEFAULT_AMBIENT_URL, timeout=5)
        if resp.ok:
            return resp.content
    except Exception:
        pass
    return None


def _run_async(coro):
    """Execute ``coro`` regardless of event loop state."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    else:
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
        return loop.run_until_complete(coro)


def main(main_container=None, status_container=None) -> None:
    """Render music generation and summary widgets."""
    if main_container is None:
        main_container = st
    if status_container is None:
        status_container = st
    theme_toggle("Dark Mode", key_suffix="music")

    # Auto-refresh for backend health check (global, outside main_container)
    st_autorefresh(interval=30000, key=STATUS_PING_KEY)

    # Render global backend status indicator in the provided container
    status_ctx = safe_container(status_container)
    with status_ctx:
        render_status_icon(endpoint="/healthz")

    # Display alert if backend is not reachable (check once per rerun)
    backend_ok = check_backend(endpoint="/healthz")
    if not backend_ok:
        alert(
            (
                "Backend service unreachable. Please ensure it is running "
                f"at {BACKEND_URL}."
            ),
            "error",
        )

    render_resonance_music_page(main_container=main_container, backend_ok=backend_ok)


def render_resonance_music_page(
    main_container=None, backend_ok: Optional[bool] = None
) -> None:
    """
    Render the Resonance Music page with backend MIDI generation and metrics summary.
    Handles dynamic selection of profile/track and safely wraps container logic.
    """
    container_ctx = safe_container(main_container)

    with container_ctx:
        header("Resonance Music")
        centered_container()

        if backend_ok is None:
            backend_ok = check_backend(endpoint="/healthz")

        st.session_state.setdefault("ambient_enabled", True)
        play_music = st.toggle(
            "🎵 Ambient Loop",
            value=st.session_state["ambient_enabled"],
            key=AMBIENT_LOOP_TOGGLE_KEY,
        )
        st.session_state["ambient_enabled"] = play_music
        if play_music:
            audio_bytes = _load_ambient_audio()
            if audio_bytes:
                encoded = base64.b64encode(audio_bytes).decode()
                st.markdown(
                    (
                        "<audio id='ambient-audio' autoplay loop style='display:none'>"
                        f"<source src='data:audio/mp3;base64,{encoded}' "
                        "type='audio/mp3'></audio>"
                    ),
                    unsafe_allow_html=True,
                )
            else:
                st.error("Failed to load ambient music. Please try again later.")
        else:
            st.markdown(
                (
                    "<script>"
                    "var a=document.getElementById('ambient-audio');"
                    "if(a){a.pause();a.remove();}"
                    "</script>"
                ),
                unsafe_allow_html=True,
            )

        profile_options = ["default", "high_harmony", "high_entropy"]
        track_options = ["Solar Echoes", "Quantum Drift", "Ether Pulse"]
        combined_options = list(set(profile_options + track_options))

        choice = st.selectbox(
            "Select a track or resonance profile",
            combined_options,
            index=0,
            placeholder="tracks or resonance profiles",
            key=PROFILE_SELECT_KEY,
        )

        midi_placeholder = st.empty()

        # --- Generate Music Section ---
        if st.button("Generate music", key=GENERATE_MUSIC_BTN_KEY):
            if not backend_ok:
                alert(
                    (
                        "Cannot generate music: Backend service unreachable "
                        f"at {BACKEND_URL}."
                    ),
                    "error",
                )
                return

            with st.spinner("Generating..."):
                try:
                    result = _run_async(
                        dispatch_route("generate_midi", {"profile": choice})
                    )
                    midi_b64 = (
                        result.get("midi_base64") if isinstance(result, dict) else None
                    )

                    if midi_b64:
                        midi_bytes = base64.b64decode(midi_b64)
                        midi_placeholder.audio(midi_bytes, format="audio/midi")
                        st.toast("Music generated!")
                    else:
                        alert("No MIDI data returned from generation.", "warning")
                except Exception as exc:
                    alert(
                        "Music generation failed: "
                        f"{exc}. Ensure backend is running and "
                        "'generate_midi' route is available.",
                        "error",
                    )

        # --- Fetch Resonance Summary Section ---
        if st.button("Fetch resonance summary", key=FETCH_SUMMARY_BTN_KEY):
            if not backend_ok:
                alert(
                    (
                        "Cannot fetch summary: Backend service unreachable "
                        f"at {BACKEND_URL}."
                    ),
                    "error",
                )
                return

            with st.spinner("Fetching summary..."):
                try:
                    data = _run_async(get_resonance_summary(choice))
                except Exception as exc:
                    alert(
                        "Failed to load summary: "
                        f"{exc}. Ensure backend is running and "
                        "'resonance-summary' route is available.",
                        "error",
                    )
                else:
                    if data:
                        metrics = data.get("metrics", {})
                        midi_bytes_count = data.get("midi_bytes", 0)

                        header("Metrics")
                        if metrics:
                            st.table(
                                {
                                    "metric": list(metrics.keys()),
                                    "value": list(metrics.values()),
                                }
                            )
                        else:
                            st.toast("No metrics available for this profile.")

                        st.write(
                            f"Associated MIDI bytes (count/size): {midi_bytes_count}"
                        )

                        summary_midi_b64 = data.get("midi_base64")
                        if summary_midi_b64:
                            summary_midi_bytes = base64.b64decode(summary_midi_b64)
                            st.audio(
                                summary_midi_bytes,
                                format="audio/midi",
                                key=SUMMARY_AUDIO_PLAYER_KEY,
                            )
                            st.toast("Playing associated MIDI from summary.")

                        st.toast("Summary loaded!")
                    else:
                        alert("No summary data returned for this profile.", "warning")


def render() -> None:
    """Wrapper to keep page loading consistent."""
    main()


if __name__ == "__main__":
    main()
