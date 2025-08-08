import importlib
import os
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
os.environ["USE_REAL_BACKEND"] = "0"

from services import reactor_adapter

importlib.reload(reactor_adapter)


def test_reactions_aggregate():
    reactor_adapter.record_reaction(1, "alice", "up")
    reactor_adapter.record_reaction(1, "bob", "up")
    counts = reactor_adapter.get_reactions(1)
    assert counts["counts"]["up"] == 2
    assert not counts["available"]
