"""User profile view and editing."""

# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards

try:
    from nicegui import ui
except Exception:  # pragma: no cover - fallback to Streamlit
    ui = None  # type: ignore
    import streamlit as st
from utils.api import (
    TOKEN,
    api_call,
    clear_token,
    get_followers,
    get_following,
    get_user,
    toggle_follow,
    get_user_recommendations,
)
from utils.layout import page_container
from utils.styles import (THEMES, get_theme, get_theme_name, set_accent,
                          set_theme)

from .events_page import events_page
from .groups_page import groups_page
from .login_page import login_page
from .messages_page import messages_page
from .notifications_page import notifications_page
from .proposals_page import proposals_page
from .vibenodes_page import vibenodes_page
from .recommendations_page import recommendations_page


@ui.page("/profile")
@ui.page("/profile/{username}")
async def profile_page(username: str | None = None):
    """Display and edit the user's profile."""
    if not TOKEN:
        ui.open(login_page)
        return

    my_data = await api_call("GET", "/users/me")
    if not my_data:
        clear_token()
        ui.open(login_page)
        return

    target_username = username or my_data["username"]
    if target_username == my_data["username"]:
        user_data = my_data
        score_data = await api_call("GET", "/users/me/influence-score") or {}
    else:
        user_data = await get_user(target_username)
        if not user_data:
            ui.notify("User not found", color="negative")
            return
        score_data = {}

    followers = await get_followers(target_username)
    following = await get_following(target_username)

    # always fetch avatar_url from /users/<username>
    avatar_resp = await api_call("GET", f"/users/{target_username}") or {}
    avatar_url = avatar_resp.get("avatar_url")

    THEME = get_theme()
    with page_container(THEME):
        avatar_img = (
            ui.image(avatar_url)
            .classes("w-32 h-32 rounded-full mb-2")
            if avatar_url
            else ui.icon("person").classes("text-8xl mb-2")
        )

        ui.label(f'Welcome, {user_data["username"]}').classes(
            "text-2xl font-bold mb-4"
        ).style(f'color: {THEME["accent"]};')

        ui.label(f'Harmony Score: {user_data["harmony_score"]}').classes("mb-2")
        ui.label(f'Creative Spark: {user_data["creative_spark"]}').classes("mb-2")
        ui.label(
            f'Influence Score: {score_data.get("influence_score", "N/A")}'
        ).classes("mb-2")
        ui.label(f'Species: {user_data["species"]}').classes("mb-2")
        followers_label = ui.label(f'Followers: {followers.get("count", 0)}').classes(
            "mb-2"
        )
        ui.label(f'Following: {following.get("count", 0)}').classes("mb-4")

        if target_username == my_data["username"]:
            bio = ui.input("Bio", value=user_data.get("bio", "")).classes("w-full mb-2")

            async def update_bio():
                resp = await api_call("PUT", "/users/me", {"bio": bio.value})
                if resp:
                    ui.notify("Bio updated", color="positive")

            ui.button("Update Bio", on_click=update_bio).classes("mb-4").style(
                f'background: {THEME["primary"]}; color: {THEME["text"]};'
            )

            async def handle_avatar_upload(content, name):
                nonlocal avatar_url
                files = {"file": (name, content.read(), "multipart/form-data")}
                resp = await api_call("POST", "/upload/avatar", files=files)
                if resp and resp.get("avatar_url"):
                    avatar_img.source = resp["avatar_url"]
                    avatar_url = resp["avatar_url"]
                    await api_call("PUT", "/users/me", {"avatar_url": resp["avatar_url"]})
                    ui.notify("Avatar updated", color="positive")

            ui.upload(
                on_upload=lambda e: ui.run_async(handle_avatar_upload(e.content, e.name))
            ).classes("w-full mb-4")
        else:
            ui.label(user_data.get("bio", "")).classes("mb-4")
            is_following = my_data["username"] in followers.get("followers", [])

            async def toggle() -> None:
                await toggle_follow(target_username)
                new_data = await get_followers(target_username)
                followers_label.text = f"Followers: {new_data.get('count', 0)}"
                button.text = (
                    "Unfollow"
                    if my_data["username"] in new_data.get("followers", [])
                    else "Follow"
                )

            button = (
                ui.button(
                    "Unfollow" if is_following else "Follow",
                    on_click=lambda: ui.run_async(toggle()),
                )
                .classes("mb-4")
                .style(f'background: {THEME["primary"]}; color: {THEME["text"]};')
            )

        ui.button("VibeNodes", on_click=lambda: ui.open(vibenodes_page)).classes(
            "w-full mb-2"
        ).style(f'background: {THEME["accent"]}; color: {THEME["background"]};')
        from .explore_page import explore_page  # lazy import

        ui.button("Explore", on_click=lambda: ui.open(explore_page)).classes(
            "w-full mb-2"
        ).style(f'background: {THEME["accent"]}; color: {THEME["background"]};')
        ui.button("Groups", on_click=lambda: ui.open(groups_page)).classes(
            "w-full mb-2"
        ).style(f'background: {THEME["accent"]}; color: {THEME["background"]};')
        ui.button("Events", on_click=lambda: ui.open(events_page)).classes(
            "w-full mb-2"
        ).style(f'background: {THEME["accent"]}; color: {THEME["background"]};')
        ui.button("Proposals", on_click=lambda: ui.open(proposals_page)).classes(
            "w-full mb-2"
        ).style(f'background: {THEME["accent"]}; color: {THEME["background"]};')
        ui.button(
            "Notifications", on_click=lambda: ui.open(notifications_page)
        ).classes("w-full mb-2").style(
            f'background: {THEME["accent"]}; color: {THEME["background"]};'
        )
        ui.button("Messages", on_click=lambda: ui.open(messages_page)).classes(
            "w-full mb-2"
        ).style(f'background: {THEME["accent"]}; color: {THEME["background"]};')
        ui.button("Discover", on_click=lambda: ui.open(recommendations_page)).classes(
            "w-full mb-2"
        ).style(f'background: {THEME["accent"]}; color: {THEME["background"]};')
        from .system_insights_page import system_insights_page  # lazy import

        ui.button(
            "System Insights", on_click=lambda: ui.open(system_insights_page)
        ).classes("w-full mb-2").style(
            f'background: {THEME["accent"]}; color: {THEME["background"]};'
        )
        ui.button(
            "Logout",
            on_click=lambda: (clear_token(), ui.open(login_page)),
        ).classes("w-full").style(f'background: red; color: {THEME["text"]};')

        with ui.row().classes("w-full mt-4"):
            ui.select(
                list(THEMES.keys()),
                value=get_theme_name(),
                on_change=lambda e: set_theme(e.value),
            ).classes("mr-2")
            ui.color_input(
                "Accent",
                value=THEME["accent"],
                on_change=lambda e: set_accent(e.value),
            )

        ui.label("You may like").classes("text-xl font-bold mt-4").style(
            f'color: {THEME["accent"]};'
        )
        suggestions = ui.column().classes("w-full")

        async def load_suggestions() -> None:
            recs = await get_user_recommendations()
            for u in recs:
                with suggestions:
                    with ui.card().classes('w-full mb-2').style(
                        'border: 1px solid #333; background: #1e1e1e;'
                    ):
                        ui.label(u.get('username', 'Unknown')).classes('text-lg')
                        bio = u.get('bio')
                        if bio:
                            ui.label(bio).classes('text-sm')

        await load_suggestions()

if ui is None:
    def profile_page(*_a, **_kw):
        """Fallback profile page when NiceGUI is unavailable."""
        st.info('Profile page requires NiceGUI.')

