import importlib
import os
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
os.environ["USE_REAL_BACKEND"] = "0"

from services import federation_adapter

importlib.reload(federation_adapter)


def test_forks_stub():
    start = len(federation_adapter.list_forks()["forks"])
    res = federation_adapter.create_fork("alice", {"HARMONY_WEIGHT": "0.9"})
    assert res["ok"]
    after = federation_adapter.list_forks()
    assert len(after["forks"]) == start + 1
    assert not after["available"]
