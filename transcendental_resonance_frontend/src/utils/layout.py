from __future__ import annotations

from contextlib import contextmanager
from typing import Optional, Generator, Dict, Any

try:  # pragma: no cover - allow import without NiceGUI installed
    from nicegui import ui
    from nicegui.element import Element
except Exception:  # pragma: no cover - fallback stub for testing
    import types

    class Element:  # type: ignore
        """Fallback element used when NiceGUI is unavailable."""
        pass

    class _DummyContext:
        def __enter__(self) -> Element:
            return Element()

        def __exit__(self, *_exc) -> None:
            pass

        def classes(self, *_args, **_kw) -> "_DummyContext":
            return self

        def style(self, *_args, **_kw) -> "_DummyContext":
            return self

    def _dummy_column() -> _DummyContext:
        return _DummyContext()

    ui = types.SimpleNamespace(column=_dummy_column)

from .styles import get_theme
from .api import combined_search, OFFLINE_MODE




def search_widget() -> Element:
    """Render a global search input with dropdown results."""
    search_input = ui.input('Search').classes('w-full mb-2')
    dropdown = ui.select([]).classes('w-full mb-2').style('display: none;')
    results: Dict[str, Any] = {}

    async def update_results() -> None:
        query = search_input.value or ''
        if not query.strip():
            dropdown.options = []
            dropdown.visible = False
            return
        data = await combined_search(query.strip())
        dropdown.options = [d['label'] for d in data]
        results.clear()
        for d in data:
            results[d['label']] = d
        dropdown.visible = True

    search_input.on_change(lambda e: ui.run_async(update_results()))

    def navigate(e) -> None:
        item = results.get(e.value)
        if not item:
            return
        if item['type'] == 'user':
            ui.open(f"/profile/{item['id']}")
        elif item['type'] == 'vibenode':
            ui.open('/vibenodes')
        elif item['type'] == 'event':
            ui.open('/events')

    dropdown.on_change(navigate)
    return dropdown


@contextmanager
def page_container(theme: Optional[dict] = None) -> Generator[Element, None, None]:
    """Context manager for a themed page container.

    Creates a ``ui.column`` with the standard padding and background
    gradient for the currently active theme.
    """
    theme = theme or get_theme()
    with ui.column().classes('w-full p-4').style(
        f"background: {theme['gradient']}; color: {theme['text']};"
    ) as container:
        if OFFLINE_MODE:
            ui.label("Offline Mode – using mock services.").classes(
                "text-xs opacity-75 mb-2"
            )
        yield container

