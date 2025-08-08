# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards

try:
    from nicegui import ui
except Exception:  # pragma: no cover - fallback to Streamlit
    ui = None  # type: ignore
    import streamlit as st
from utils.api import TOKEN, api_call
from utils.layout import page_container
from utils.features import skeleton_loader
from components.media_renderer import render_media_block
from utils.styles import get_theme

from .login_page import login_page


@ui.page("/explore")
async def explore_page() -> None:
    """Display trending VibeNodes with infinite scroll."""
    if not TOKEN:
        ui.open(login_page)
        return

    THEME = get_theme()
    with page_container(THEME):
        ui.label("Explore").classes("text-2xl font-bold mb-4").style(
            f'color: {THEME["accent"]};'
        )

        posts_container = ui.column().classes("w-full")

        limit = 10
        offset = 0
        loading = {"value": False}

        async def load_more() -> None:
            nonlocal offset
            params = {"offset": offset, "limit": limit}
            placeholders = []
            with posts_container:
                for _ in range(limit):
                    placeholders.append(skeleton_loader().classes("w-full h-32 mb-2"))
            posts = None
            try:
                posts = await api_call("GET", "/vibenodes/trending", params)
            except Exception:
                posts = None
            for p in placeholders:
                p.delete()
            if posts is None:
                ui.notify('Failed to load posts', color='negative')
                return
            if not posts:
                return
            offset += len(posts)
            for p in posts:
                with posts_container:
                    with (
                        ui.card()
                        .classes("w-full mb-2")
                        .style("border: 1px solid #333; background: #1e1e1e;")
                    ):
                        ui.label(p.get("name", "")).classes("text-lg")
                        ui.label(p.get("description", "")).classes("text-sm")
                        render_media_block(p.get("media_url"), p.get("media_type", ""))
                        ui.label(f"Likes: {p.get('likes_count', 0)}").classes("text-sm")

        await load_more()

        async def check_scroll() -> None:
            if loading["value"]:
                return
            at_bottom = await ui.run_javascript(
                "window.innerHeight + window.scrollY >= document.body.offsetHeight - 2",
                respond=True,
            )
            if at_bottom:
                loading["value"] = True
                await load_more()
                loading["value"] = False

        ui.timer(1.0, lambda: ui.run_async(check_scroll()))

if ui is None:
    def explore_page(*_a, **_kw):
        """Fallback explore page when NiceGUI is unavailable."""
        st.info('Explore page requires NiceGUI.')

