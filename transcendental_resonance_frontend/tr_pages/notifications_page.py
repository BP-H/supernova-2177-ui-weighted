# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""User notifications page."""

try:
    from nicegui import ui
except Exception:  # pragma: no cover - fallback to Streamlit
    ui = None  # type: ignore
    import streamlit as st
from utils.api import TOKEN, api_call, listen_ws
from utils.layout import page_container
from utils.styles import get_theme

from .login_page import login_page


@ui.page("/notifications")
async def notifications_page():
    """Display user notifications."""
    if not TOKEN:
        ui.open(login_page)
        return

    THEME = get_theme()
    with page_container(THEME):
        ui.label("Notifications").classes("text-2xl font-bold mb-4").style(
            f'color: {THEME["accent"]};'
        )

        notifs_list = ui.column().classes("w-full")

        async def refresh_notifs():
            notifs = await api_call("GET", "/notifications/") or []
            notifs_list.clear()
            for n in notifs:
                with notifs_list:
                    with (
                        ui.card()
                        .classes("w-full mb-2")
                        .style("border: 1px solid #333; background: #1e1e1e;")
                    ):
                        ui.label(n["message"]).classes("text-sm")
                        if not n["is_read"]:

                            async def mark_read(n_id=n["id"]):
                                await api_call("PUT", f"/notifications/{n_id}/read")
                                await refresh_notifs()

                            ui.button("Mark Read", on_click=mark_read).style(
                                f'background: {THEME["primary"]}; color: {THEME["text"]};'
                            )

        await refresh_notifs()
        ui.timer(30, lambda: ui.run_async(refresh_notifs()))

        async def handle_event(event: dict) -> None:
            if event.get("type") == "notification":
                await refresh_notifs()

        ws_task = listen_ws(handle_event)
        ui.context.client.on_disconnect(lambda: ws_task.cancel())

if ui is None:
    def notifications_page(*_a, **_kw):
        """Fallback notifications page when NiceGUI is unavailable."""
        st.info('Notifications page requires NiceGUI.')

