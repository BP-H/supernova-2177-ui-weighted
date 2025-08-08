# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Interactive music generation page."""

try:
    from nicegui import ui
except Exception:  # pragma: no cover - fallback to Streamlit
    ui = None  # type: ignore
    import streamlit as st

from utils.api import api_call, TOKEN
from utils.styles import get_theme
from utils.layout import page_container
from .login_page import login_page


@ui.page('/music')
async def music_page():
    """Generate music based on harmony settings."""
    if not TOKEN:
        ui.open(login_page)
        return

    THEME = get_theme()
    with page_container(THEME):
        ui.label('Music Generator').classes('text-2xl font-bold mb-4').style(
            f'color: {THEME["accent"]};'
        )

        harmony_slider = ui.slider(min=0, max=100, value=50).classes('w-full')
        harmony_label = ui.label(f'Harmony: {harmony_slider.value}').classes('mb-4')
        harmony_slider.on(
            'update:model-value',
            lambda e: harmony_label.set_text(f'Harmony: {e.value}')
        )

        length_input = ui.number('Length (bars)', value=8).classes('w-full mb-4')

        download_link = ui.link('Download MIDI', '#').props('download').classes('hidden')

        async def generate():
            data = {
                'harmony': harmony_slider.value,
                'length': length_input.value,
            }
            resp = await api_call('POST', '/generate-music', data)
            if resp and 'url' in resp:
                download_link.href = resp['url']
                download_link.classes(remove='hidden')
                ui.notify('Music generated!', color='positive')
            else:
                ui.notify('Music generation failed', color='negative')

        ui.button('Generate Music', on_click=generate).classes('w-full mb-4').style(
            f'background: {THEME["primary"]}; color: {THEME["text"]};'
        )
        download_link

if ui is None:
    def music_page(*_a, **_kw):
        """Fallback music page when NiceGUI is unavailable."""
        st.info('Music page requires NiceGUI.')

