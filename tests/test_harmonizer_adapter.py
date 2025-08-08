from pathlib import Path
import sys
import importlib

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))


def test_stub_harmonizer_functions(monkeypatch):
    monkeypatch.setenv("USE_REAL_BACKEND", "0")
    from services import harmonizer_adapter

    importlib.reload(harmonizer_adapter)
    harmonizer_adapter.reset_stub()

    user = harmonizer_adapter.register("alice", "a@example.com", "pw")
    assert user["username"] == "alice"

    dup = harmonizer_adapter.register("alice", "b@example.com", "pw")
    assert "error" in dup

    score = harmonizer_adapter.get_influence_score("alice")
    assert score["influence_score"] == 0.0

    listing = harmonizer_adapter.list_harmonizers()
    assert any(u["username"] == "alice" for u in listing["harmonizers"])
