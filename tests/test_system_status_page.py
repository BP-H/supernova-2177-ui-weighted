# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
import sys
import types
from pathlib import Path

import pytest

pytest.importorskip("streamlit")
pytestmark = pytest.mark.requires_streamlit

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

import pages.system_status as status_page  # noqa: E402


def test_status_page_placeholders_when_disabled(monkeypatch):
    metrics = []
    dummy_st = types.SimpleNamespace(
        toggle=lambda *a, **k: False,
        metric=lambda label, value: metrics.append((label, value)),
        warning=lambda *a, **k: None,
    )
    monkeypatch.setattr(status_page, "st", dummy_st)
    status_page.main()
    assert ("Harmonizers", "N/A") in metrics
    assert ("VibeNodes", "N/A") in metrics
    assert ("Entropy", "N/A") in metrics


def test_status_page_shows_metrics(monkeypatch):
    metrics = []
    dummy_st = types.SimpleNamespace(
        toggle=lambda *a, **k: True,
        metric=lambda label, value: metrics.append((label, value)),
        warning=lambda *a, **k: None,
    )
    monkeypatch.setattr(status_page, "st", dummy_st)
    sample = {
        "available": True,
        "metrics": {
            "total_harmonizers": 3,
            "total_vibenodes": 5,
            "current_system_entropy": 0.42,
        },
    }
    monkeypatch.setattr(status_page, "get_status", lambda: sample)
    status_page.main()
    assert ("Harmonizers", 3) in metrics
    assert ("VibeNodes", 5) in metrics
    assert ("Entropy", 0.42) in metrics
