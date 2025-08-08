# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards

import pytest
pytest.importorskip("nicegui")
pytestmark = pytest.mark.requires_nicegui

import inspect
from transcendental_resonance_frontend.tr_pages.messages_page import messages_page

def test_messages_page_is_async():
    assert inspect.iscoroutinefunction(messages_page)
