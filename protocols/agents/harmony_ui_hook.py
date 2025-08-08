from __future__ import annotations

"""Optional UI routes for :class:`HarmonySynthesizerAgent`.

Importing this module registers FastAPI endpoints, requiring the UI extras of
the project. It is intentionally not imported as part of the standard
``protocols`` package initialization.
"""

import base64
from typing import Any, Callable, Dict, Optional

from frontend_bridge import register_route_once
from hook_manager import HookManager
from hooks import events

from .harmony_synthesizer_agent import HarmonySynthesizerAgent

# Allow external modules/tests to provide a metrics provider
metrics_provider: Optional[Callable[[], Dict[str, float]]] = None

# Exposed hook manager for observers
ui_hook_manager = HookManager()

# Instantiate synthesizer agent
synth_agent = HarmonySynthesizerAgent(metrics_provider)


async def generate_midi_ui(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a MIDI snippet and return base64-encoded data."""
    midi = synth_agent.handle_generate(payload)
    encoded = base64.b64encode(midi).decode()
    await ui_hook_manager.trigger(events.MIDI_GENERATED, midi)
    return {"midi_base64": encoded}


# Register route with the central frontend router
register_route_once(
    "generate_midi",
    generate_midi_ui,
    "Generate a MIDI snippet",
    "protocols",
)
