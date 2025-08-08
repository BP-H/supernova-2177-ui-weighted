# Legal & Ethical Safeguards

import sys
from pathlib import Path

import pytest
import streamlit as st

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from profile_adapter import update_profile_adapter  # noqa: E402


@pytest.mark.requires_streamlit
def test_update_profile_stub(monkeypatch):
    called = {"count": 0}

    def fake_put(*args, **kwargs):
        called["count"] += 1

        class Resp:
            def raise_for_status(self):
                pass

        return Resp()

    monkeypatch.setattr("profile_adapter.requests.put", fake_put)
    result = update_profile_adapter("hello", ["music"], use_backend=False)
    assert result["status"] == "stubbed"
    assert result["available"]
    assert called["count"] == 0


@pytest.mark.requires_streamlit
def test_update_profile_backend(monkeypatch):
    def fake_put(url, json, timeout):
        assert json == {"bio": "hello", "cultural_preferences": ["music"]}

        class Resp:
            def raise_for_status(self):
                pass

        return Resp()

    monkeypatch.setattr("profile_adapter.requests.put", fake_put)
    result = update_profile_adapter("hello", ["music"], use_backend=True)
    assert result["status"] == "ok"
    assert result["available"]


@pytest.mark.requires_streamlit
def test_update_profile_validation_error(monkeypatch):
    result = update_profile_adapter("", ["music"], use_backend=True)
    assert result["status"] == "error"
    assert result["available"]
