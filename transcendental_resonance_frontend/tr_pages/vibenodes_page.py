# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""VibeNodes creation and listing."""

try:
    from nicegui import ui
except Exception:  # pragma: no cover - fallback to Streamlit
    ui = None  # type: ignore
    import streamlit as st

try:  # optional import when NiceGUI is available
    import streamlit as st  # type: ignore
except Exception:  # pragma: no cover - streamlit optional
    st = None  # type: ignore

import asyncio
import contextlib

from components.emoji_toolbar import emoji_toolbar
from components.media_renderer import render_media_block

from utils.api import TOKEN, api_call, listen_ws
from utils.features import skeleton_loader
from utils.layout import page_container
from utils.safe_markdown import safe_markdown
from utils.styles import get_theme

from .login_page import login_page


@ui.page("/vibenodes")
async def vibenodes_page():
    """Create and display VibeNodes."""
    if not TOKEN:
        ui.open(login_page)
        return

    THEME = get_theme()
    with page_container(THEME):
        ui.label("VibeNodes").classes("text-2xl font-bold mb-4").style(
            f'color: {THEME["accent"]};'
        )


        ui.label("Trending").classes("text-xl font-bold mb-2")
        trending_list = ui.column().classes("w-full mb-4")

        # fmt: off
        search_query = ui.input('Search').classes('w-full mb-2')
        # fmt: on
        # fmt: off
        sort_select = ui.select(['name', 'date', 'trending'], value='name').classes('w-full mb-4')
        # fmt: on

        name = ui.input("Name").classes("w-full mb-2")
        description = ui.textarea("Description").classes("w-full mb-2")
        media_type = ui.select(
            ["text", "image", "video", "audio", "music", "mixed"],
            value="text",
        ).classes("w-full mb-2")
        tags = ui.input("Tags (comma-separated)").classes("w-full mb-2")
        parent_id = ui.input("Parent VibeNode ID (optional)").classes("w-full mb-2")

        uploaded_media = {"url": None, "type": None}
        progress_container = ui.column().classes("w-full")

        async def handle_upload(event):
            with progress_container:
                progress = ui.linear_progress(value=0).classes('w-full mb-2')


            async def spin():
                while progress.value < 0.95:
                    await asyncio.sleep(0.1)
                    progress.value += 0.05

            spinner = ui.background_tasks.create(spin(), name='upload-progress')
            try:
                files = {
                    'file': (event.name, event.content.read(), 'multipart/form-data')
                }
                resp = await api_call('POST', '/upload/', files=files)
            finally:
                spinner.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await spinner
                progress.value = 1.0

            if resp:
                uploaded_media['url'] = resp.get('media_url')
                uploaded_media['type'] = resp.get('media_type')
                ui.notify('Media uploaded', color='positive')
                if uploaded_media['type'] and uploaded_media['type'].startswith('image'):
                    ui.image(uploaded_media['url']).classes('w-full mb-2')




        ui.upload(
            multiple=True,
            auto_upload=True,
            on_upload=lambda e: ui.run_async(handle_upload(e)),
        ).props("label=Drop files here").classes(
            "w-full mb-2 border-2 border-dashed rounded-lg p-4"
        )

        async def create_vibenode():
            data = {
                "name": name.value,
                "description": description.value,
                "media_type": uploaded_media.get("type") or media_type.value,
                "tags": (
                    [t.strip() for t in tags.value.split(",")] if tags.value else None
                ),
                "parent_vibenode_id": int(parent_id.value) if parent_id.value else None,
            }
            if uploaded_media.get("url"):
                data["media_url"] = uploaded_media["url"]
            resp = await api_call("POST", "/vibenodes/", data)
            if resp:
                ui.notify("VibeNode created!", color="positive")
                await refresh_vibenodes()
                await refresh_trending()

        ui.button("Create VibeNode", on_click=create_vibenode).classes(
            "w-full mb-4"
        ).style(f'background: {THEME["primary"]}; color: {THEME["text"]};')

        vibenodes_list = ui.column().classes("w-full")

        async def refresh_trending():
            params = {"sort": "trending", "limit": 5}
            trending_list.clear()
            with trending_list:
                for _ in range(3):
                    skeleton_loader().classes("w-full h-20 mb-2")
            trending = await api_call("GET", "/vibenodes/", params) or []
            trending_list.clear()
            for vn in trending:
                with trending_list:
                    with (
                        ui.card()
                        .classes("w-full mb-2")
                        .style("border: 1px solid #333; background: #1e1e1e;")
                    ):
                        ui.label(vn["name"]).classes("text-lg")
                        ui.label(vn["description"]).classes("text-sm")
                        if vn.get("media_url"):
                            mtype = vn.get("media_type", "")
                            if mtype.startswith("image"):
                                ui.image(vn["media_url"]).classes("w-full")
                            elif mtype.startswith("video"):
                                ui.video(vn["media_url"]).classes("w-full")
                            elif mtype.startswith("audio") or mtype.startswith("music"):
                                ui.audio(vn["media_url"]).classes("w-full")
                        ui.label(f"Likes: {vn.get('likes_count', 0)}").classes(
                            "text-sm"
                        )

                        async def like_fn(vn_id=vn["id"]):
                            await api_call("POST", f"/vibenodes/{vn_id}/like")
                            await refresh_trending()
                            await refresh_vibenodes()

                        ui.button("Like/Unlike", on_click=like_fn).style(
                            f'background: {THEME["accent"]}; color: {THEME["background"]};'
                        )

                        async def remix_fn(vn_data=vn):
                            name.value = vn_data["name"]
                            description.value = vn_data["description"]
                            parent_id.value = str(vn_data["id"])
                            ui.notify("Loaded remix draft", color="info")

                        ui.button("Remix", on_click=remix_fn).style(
                            f'background: {THEME["primary"]}; color: {THEME["text"]};'
                        )

                        if st is not None and st.session_state.get("beta_mode"):
                            async def ai_remix(vn_id=vn["id"]):
                                resp = await api_call("POST", f"/vibenodes/{vn_id}/remix")
                                if resp:
                                    dlg = ui.dialog()
                                    with dlg:
                                        with ui.card().classes("w-full p-4"):
                                            ui.label(resp.get("name", "AI Remix")).classes("text-lg")
                                            if resp.get("media_url"):
                                                render_media_block(resp.get("media_url"), resp.get("media_type", ""))
                                            ui.markdown(safe_markdown(resp.get("description", ""))).classes("text-sm")
                                            ui.button("Close", on_click=dlg.close).classes("w-full")
                                    dlg.open()

                            ui.button(
                                "AI Remix",
                                on_click=lambda vn_id=vn["id"]: ui.run_async(ai_remix(vn_id)),
                            ).style(
                                f'background: {THEME["accent"]}; color: {THEME["background"]};'
                            )

                        if st is not None and st.session_state.get("beta_mode"):
                            async def ai_remix(vn_id=vn["id"]):
                                resp = await api_call("POST", f"/vibenodes/{vn_id}/remix")
                                if resp:
                                    dlg = ui.dialog()
                                    with dlg:
                                        with ui.card().classes("w-full p-4"):
                                            ui.label(resp.get("name", "AI Remix")).classes("text-lg")
                                            if resp.get("media_url"):
                                                render_media_block(resp.get("media_url"), resp.get("media_type", ""))
                                            ui.markdown(safe_markdown(resp.get("description", ""))).classes("text-sm")
                                            ui.button("Close", on_click=dlg.close).classes("w-full")
                                    dlg.open()

                            ui.button("AI Remix", on_click=lambda vn_id=vn["id"]: ui.run_async(ai_remix(vn_id))).style(
                                f'background: {THEME["accent"]}; color: {THEME["background"]};'
                            )

        async def refresh_vibenodes():
            params = {}
            if search_query.value:
                params["search"] = search_query.value
            if sort_select.value:
                params["sort"] = sort_select.value
            vibenodes_list.clear()
            with vibenodes_list:
                for _ in range(3):
                    skeleton_loader().classes("w-full h-32 mb-2")
            vibenodes = await api_call("GET", "/vibenodes/", params) or []
            if search_query.value:
                vibenodes = [
                    vn
                    for vn in vibenodes
                    if search_query.value.lower() in vn["name"].lower()
                ]
            if sort_select.value:
                if sort_select.value == "name":
                    vibenodes.sort(key=lambda x: x.get("name", ""))
                elif sort_select.value == "date":
                    vibenodes.sort(key=lambda x: x.get("created_at", ""))
                elif sort_select.value == "trending":
                    pass
            vibenodes_list.clear()
            for vn in vibenodes:
                with vibenodes_list:
                    with (
                        ui.card()
                        .classes("w-full mb-2")
                        .style("border: 1px solid #333; background: #1e1e1e;")
                    ):
                        ui.label(vn["name"]).classes("text-lg")
                        ui.label(vn["description"]).classes("text-sm")
                        if vn.get("media_url"):
                            render_media_block(
                                vn["media_url"], vn.get("media_type", "")
                            )
                        ui.label(f"Likes: {vn.get('likes_count', 0)}").classes(
                            "text-sm"
                        )

                        async def like_fn(vn_id=vn["id"]):
                            await api_call("POST", f"/vibenodes/{vn_id}/like")
                            await refresh_vibenodes()

                        ui.button("Like/Unlike", on_click=like_fn).style(
                            f'background: {THEME["accent"]}; color: {THEME["background"]};'
                        )

                        async def remix_fn(vn_data=vn):
                            name.value = vn_data["name"]
                            description.value = vn_data["description"]
                            parent_id.value = str(vn_data["id"])
                            ui.notify("Loaded remix draft", color="info")

                        ui.button("Remix", on_click=remix_fn).style(
                            f'background: {THEME["primary"]}; color: {THEME["text"]};'
                        )

                        # --- Comments Section ---
                        comments = (
                            await api_call("GET", f'/vibenodes/{vn["id"]}/comments')
                            or []
                        )
                        with ui.expansion("Comments", value=False).classes(
                            "w-full mt-2"
                        ):
                            for c in comments:
                                ui.markdown(
                                    safe_markdown(c.get("content", ""))
                                ).classes("text-sm")
                            comment_input = ui.textarea("Add a comment").classes(
                                "w-full mb-2"
                            )
                            emoji_toolbar(comment_input)
                            suggestions_box = (
                                ui.column()
                                .classes("w-full shadow rounded hidden")
                                .style(
                                    "background:#1e1e1e; position: absolute; z-index: 50;"
                                )
                            )

                            async def update_suggestions() -> None:
                                import re

                                text = comment_input.value
                                match = re.search(r"@(\w+)$", text)
                                if match:
                                    query = match.group(1)
                                    users = (
                                        await api_call(
                                            "GET", "/users/search", {"q": query}
                                        )
                                        or []
                                    )
                                    suggestions_box.clear()
                                    for u in users:

                                        def insert(username=u["username"]):
                                            comment_input.value = re.sub(
                                                r"@\w+$",
                                                f"@{username} ",
                                                comment_input.value,
                                            )
                                            suggestions_box.classes("hidden")

                                        ui.button(u["username"], on_click=insert).props(
                                            "flat"
                                        ).classes("w-full text-left")
                                    suggestions_box.classes(remove="hidden")
                                else:
                                    suggestions_box.classes("hidden")

                            comment_input.on(
                                "keyup", lambda e: ui.run_async(update_suggestions())
                            )

                            async def post_comment(vn_id=vn["id"], ci=comment_input):
                                import re

                                content = ci.value.strip()
                                if not content:
                                    ui.notify(
                                        "Comment cannot be empty", color="warning"
                                    )
                                    return
                                names = re.findall(r"@(\w+)", content)
                                mentioned_ids: list[int] = []
                                for name in names:
                                    user = await api_call("GET", f"/users/{name}")
                                    if user and "id" in user:
                                        mentioned_ids.append(user["id"])
                                await api_call(
                                    "POST",
                                    f"/vibenodes/{vn_id}/comments",
                                    {"content": content, "mentions": mentioned_ids},
                                )
                                ci.value = ""
                                await refresh_vibenodes()

                            ui.button("Post", on_click=post_comment).classes(
                                "w-full"
                            ).style(
                                f'background: {THEME["accent"]}; color: {THEME["background"]};'
                            )

        await refresh_trending()
        await refresh_vibenodes()

        async def handle_event(event: dict) -> None:
            if event.get("type") == "vibenode_updated":
                await refresh_vibenodes()

        async def start_ws() -> None:
            try:
                ws_task = listen_ws(handle_event)
                ui.context.client.on_disconnect(lambda: ws_task.cancel())
                await ws_task
            except Exception:
                ui.notify("Realtime updates unavailable", color="warning")

        ui.run_async(start_ws())

if ui is None:
    def vibenodes_page(*_a, **_kw):
        """Fallback vibenodes page when NiceGUI is unavailable."""
        st.info('VibeNodes page requires NiceGUI.')


