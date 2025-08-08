# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""AI assistance for VibeNodes."""

try:
    from nicegui import ui
except Exception:  # pragma: no cover - fallback to Streamlit
    ui = None  # type: ignore
    import streamlit as st

from utils.api import api_call, TOKEN
from utils.styles import get_theme
from utils.layout import page_container
from .login import login_page


@ui.page('/ai-assist/{vibenode_id}')
async def ai_assist_page(vibenode_id: int):
    """Get AI-generated help for a specific VibeNode."""
    if not TOKEN:
        ui.open(login_page)
        return

    THEME = get_theme()
    with page_container(THEME):
        ui.label('AI Assist').classes('text-2xl font-bold mb-4').style(
            f'color: {THEME["accent"]};'
        )

        prompt = ui.textarea('Prompt for AI').classes('w-full mb-2')

        async def get_ai_response():
            data = {'prompt': prompt.value}
            resp = await api_call('POST', f'/ai-assist/{vibenode_id}', data)
            if resp:
                ui.label('AI Response:').classes('mb-2')
                ui.label(resp['response']).classes('text-sm break-words')
            else:
                ui.notify('Action failed', color='negative')

        ui.button('Get AI Help', on_click=get_ai_response).classes('w-full').style(
            f'background: {THEME["primary"]}; color: {THEME["text"]};'
        )

if ui is None:
    def ai_assist_page(*_a, **_kw):
        """Fallback when NiceGUI is unavailable."""
        st.info('AI assist requires NiceGUI.')
