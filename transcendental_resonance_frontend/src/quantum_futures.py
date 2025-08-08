# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
"""Quantum futures generation utilities.

This module provides placeholders for speculative timeline modeling using
quantum-inspired heuristics. Functions here generate whimsical possible
futures for VibeNodes and include stubs for upcoming vision and video hooks.
"""

from __future__ import annotations

import random
from typing import Any, Dict, List

import streamlit as st

from external_services.llm_client import LLMClient, get_speculative_futures
from external_services.vision_client import VisionClient, analyze_timeline

# Satirical disclaimer appended to all speculative output
DISCLAIMER = "This is a satirical simulation, not advice or prediction."

# Sarcastic quantum emoji glossary
EMOJI_GLOSSARY: Dict[str, str] = {
    "\U0001F468\u200d\U0001F4BB": "time ripple",
    "\U0001F300": "quantum swirl",
    "\U0001F308": "hopeful decoherence",
}


def _entropy_tag() -> float:
    """Return a random entropy tag used for demo purposes."""
    return random.random()  # nosec B311


@st.cache_data(show_spinner=False)
async def generate_speculative_futures(
    node: Dict[str, Any], num_variants: int = 3
) -> List[Dict[str, str]]:
    """Generate playful speculative futures for a VibeNode using ``llm_client``."""

    description = node.get("description", "")
    texts = await get_speculative_futures(description)
    futures: List[Dict[str, str]] = []
    for text in texts[: max(1, num_variants)]:
        emoji = random.choice(list(EMOJI_GLOSSARY.keys()))  # nosec B311
        futures.append({"text": f"{text} {emoji}", "entropy": f"{_entropy_tag():.2f}"})
    return futures


@st.cache_data(show_spinner=False)
async def generate_speculative_payload(description: str) -> List[Dict[str, str]]:
    """Return text, video, and vision analysis pairs with a disclaimer."""

    llm = LLMClient()
    texts = (await llm.get_speculative_futures(description)).get("futures", [])
    results: List[Dict[str, str]] = []
    vision = VisionClient()
    for text in texts:
        offline = llm.offline or vision.offline
        if offline:
            video_url = "https://example.com/placeholder"
        else:
            video_url = f"https://example.com/fake_video_for_{text[:10]}"
        vision_notes = (await vision.analyze_timeline(video_url)).get("events", [])
        results.append(
            {
                "text": text,
                "video_url": video_url,
                "vision_notes": vision_notes,
                "disclaimer": DISCLAIMER,
            }
        )
    return results


def quantum_video_stub(*_args, **_kwargs) -> None:
    """Placeholder for future WebGL/AI-video integration."""
    return None


async def analyze_video_timeline(video_url: str) -> List[str]:
    """Delegate to :func:`analyze_timeline` for vision analysis."""
    return await analyze_timeline(video_url)


__all__ = [
    "DISCLAIMER",
    "EMOJI_GLOSSARY",
    "generate_speculative_futures",
    "quantum_video_stub",
    "analyze_video_timeline",
]
