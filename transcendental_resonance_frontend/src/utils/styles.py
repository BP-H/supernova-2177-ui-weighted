"""Styling utilities for the Transcendental Resonance frontend."""

from typing import Dict, Optional
from frontend.theme import set_theme as _st_set_theme

try:
    from nicegui import ui  # type: ignore
except Exception:  # pragma: no cover - nicegui optional
    class _UIStub:
        def run_javascript(self, *args, **kwargs):
            return None

        def add_head_html(self, *args, **kwargs):
            return None

    ui = _UIStub()  # type: ignore

# Theme palettes. The default "dark" theme matches the original neon aesthetic.
THEMES: Dict[str, Dict[str, str]] = {
    "dark": {
        "primary": "#0d47a1",
        "accent": "#00e676",
        "background": "#121212",
        "text": "#ffffff",
        "gradient": "linear-gradient(135deg, #0d47a1 0%, #121212 100%)",
    },
    "light": {
        "primary": "#1976d2",
        "accent": "#ff4081",
        "background": "#ffffff",
        "text": "#000000",
        "gradient": "linear-gradient(135deg, #ffffff 0%, #f3f3f3 100%)",
    },
    "modern": {
        "primary": "#6200EE",
        "accent": "#03DAC5",
        "background": "#f5f5f5",
        "text": "#333333",
        "gradient": "linear-gradient(135deg, #6200EE 0%, #03DAC5 100%)",
    },
    "cyberpunk": {
        "primary": "#FF0080",
        "accent": "#00F0FF",
        "background": "#050014",
        "text": "#F8F8F2",
        "gradient": "linear-gradient(135deg, #FF0080 0%, #00F0FF 100%)",
    },
    "codex": {
        "primary": "#19C37D",
        "accent": "#19C37D",
        "background": "#202123",
        "text": "#ECECF1",
        "gradient": "linear-gradient(135deg, #202123 0%, #343541 100%)",
    },
    "high_contrast": {
        "primary": "#000000",
        "accent": "#FFFF00",
        "background": "#000000",
        "text": "#FFFFFF",
        "gradient": "linear-gradient(135deg, #000000 0%, #222222 100%)",
    },
}

# Currently active theme name and accent color. They can be changed at runtime
# and are persisted in the browser ``localStorage``.
ACTIVE_THEME_NAME: str = "dark"
ACTIVE_ACCENT: str = THEMES[ACTIVE_THEME_NAME]["accent"]


def apply_global_styles() -> None:
    """Inject global CSS styles based on stored theme and accent settings."""
    global ACTIVE_THEME_NAME, ACTIVE_ACCENT

    try:
        stored_theme: Optional[str] = ui.run_javascript(
            "localStorage.getItem('theme')",
            respond=True,
        )
        if isinstance(stored_theme, str) and stored_theme in THEMES:
            ACTIVE_THEME_NAME = stored_theme
        stored_accent: Optional[str] = ui.run_javascript(
            "localStorage.getItem('accent')",
            respond=True,
        )
        if isinstance(stored_accent, str) and stored_accent:
            ACTIVE_ACCENT = stored_accent
    except Exception:
        # Accessing localStorage may fail during testing
        pass

    theme = THEMES[ACTIVE_THEME_NAME].copy()
    theme["accent"] = ACTIVE_ACCENT

    font_family = "'Inter', sans-serif"
    font_link = "<link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap\" rel=\"stylesheet\">"
    if ACTIVE_THEME_NAME == "cyberpunk":
        font_family = "'Orbitron', sans-serif"
        font_link = (
            "<link href=\"https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap\" rel=\"stylesheet\">"
        )
    elif ACTIVE_THEME_NAME == "codex":
        font_family = "'Iosevka', monospace"
        font_link = (
            "<link href=\"https://fonts.googleapis.com/css2?family=Iosevka:wght@400;700&display=swap\" rel=\"stylesheet\">"
        )

    ui.add_head_html(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        {font_link}
        <style id="global-theme">
            body {{ font-family: {font_family}; background: {theme['background']}; color: {theme['text']}; }}
            .q-btn:hover {{ border: 1px solid {theme['accent']}; }}
            .futuristic-gradient {{ background: {theme['gradient']}; }}
            .glow-card {{ border: 1px solid {theme["accent"]}; box-shadow: 0 0 6px {theme["accent"]}; }}
        </style>
        """
    )


def set_theme(name: str) -> None:
    """Switch the active theme and reapply global styles.

    This wrapper updates local theme tracking and delegates to
    :func:`frontend.theme.set_theme` for CSS injection.
    """
    global ACTIVE_THEME_NAME, ACTIVE_ACCENT
    ACTIVE_THEME_NAME = name if name in THEMES else "dark"
    ACTIVE_ACCENT = THEMES[ACTIVE_THEME_NAME]["accent"]
    ui.run_javascript(f"localStorage.setItem('theme', '{ACTIVE_THEME_NAME}')")
    ui.run_javascript(f"localStorage.setItem('accent', '{ACTIVE_ACCENT}')")
    apply_global_styles()
    _st_set_theme(ACTIVE_THEME_NAME)


def get_theme() -> Dict[str, str]:
    """Return the currently active theme dictionary."""
    theme = THEMES[ACTIVE_THEME_NAME].copy()
    theme["accent"] = ACTIVE_ACCENT
    return theme


def get_theme_name() -> str:
    """Return the name of the currently active theme."""
    return ACTIVE_THEME_NAME


def set_accent(color: str) -> None:
    """Update only the accent color and store the preference."""
    global ACTIVE_ACCENT
    ACTIVE_ACCENT = color
    ui.run_javascript(f"localStorage.setItem('accent', '{color}')")
    apply_global_styles()


_previous_theme = ACTIVE_THEME_NAME

def toggle_high_contrast(enabled: bool) -> None:
    """Enable or disable high contrast mode."""
    global _previous_theme
    if enabled:
        _previous_theme = ACTIVE_THEME_NAME
        set_theme("high_contrast")
    else:
        set_theme(_previous_theme)
