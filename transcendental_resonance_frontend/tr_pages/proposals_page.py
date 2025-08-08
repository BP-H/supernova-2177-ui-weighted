# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Governance proposals page."""

try:
    from nicegui import ui
except Exception:  # pragma: no cover - fallback to Streamlit
    ui = None  # type: ignore
    import streamlit as st

from utils.api import api_call, TOKEN
from utils.styles import get_theme
from utils.layout import page_container
from utils.features import skeleton_loader
from .login_page import login_page


@ui.page('/proposals')
async def proposals_page():
    """Create and vote on proposals."""
    if not TOKEN:
        ui.open(login_page)
        return

    THEME = get_theme()
    with page_container(THEME):
        ui.label('Proposals').classes('text-2xl font-bold mb-4').style(
            f'color: {THEME["accent"]};'
        )

        p_title = ui.input('Title').classes('w-full mb-2')
        p_desc = ui.textarea('Description').classes('w-full mb-2')
        p_type = ui.select(['general', 'system_parameter_change'], value='general').classes('w-full mb-2')
        p_group_id = ui.input('Group ID (optional)').classes('w-full mb-2')

        async def create_proposal():
            data = {
                'title': p_title.value,
                'description': p_desc.value,
                'proposal_type': p_type.value,
                'group_id': int(p_group_id.value) if p_group_id.value else None,
            }
            resp = await api_call('POST', '/proposals/', data)
            if resp:
                ui.notify('Proposal created!', color='positive')
                await refresh_proposals()
            else:
                ui.notify('Action failed', color='negative')

        ui.button('Create Proposal', on_click=create_proposal).classes('w-full mb-4').style(
            f'background: {THEME["primary"]}; color: {THEME["text"]};'
        )

        proposals_list = ui.column().classes('w-full')

        async def refresh_proposals():
            proposals_list.clear()
            with proposals_list:
                for _ in range(3):
                    skeleton_loader().classes('w-full h-20 mb-2')
            proposals = await api_call('GET', '/proposals/') or []
            proposals_list.clear()
            for p in proposals:
                with proposals_list:
                    with ui.card().classes('w-full mb-2').style('border: 1px solid #333; background: #1e1e1e;'):
                        ui.label(p['title']).classes('text-lg')
                        ui.label(p['description']).classes('text-sm')
                        ui.label(f"Status: {p['status']}").classes('text-sm')
                        if p['status'] == 'open':
                            async def vote_yes(p_id=p['id']):
                                await api_call('POST', f'/proposals/{p_id}/vote', {'vote': 'yes'})
                                await refresh_proposals()
                            async def vote_no(p_id=p['id']):
                                await api_call('POST', f'/proposals/{p_id}/vote', {'vote': 'no'})
                                await refresh_proposals()
                            ui.row().classes('justify-between')
                            ui.button('Yes', on_click=vote_yes).style('background: green; color: white;')
                            ui.button('No', on_click=vote_no).style('background: red; color: white;')

        await refresh_proposals()

if ui is None:
    def proposals_page(*_a, **_kw):
        """Fallback proposals page when NiceGUI is unavailable."""
        st.info('Proposals page requires NiceGUI.')

