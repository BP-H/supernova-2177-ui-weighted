import importlib
import os
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
os.environ["USE_REAL_BACKEND"] = "0"

from services import coin_adapter

importlib.reload(coin_adapter)


def test_tip_and_ledger():
    coin_adapter.tip("alice", "bob", 2.0, None)
    a = coin_adapter.get_balance("alice")
    b = coin_adapter.get_balance("bob")
    assert a["balance"] == -2.0
    assert b["balance"] == 2.0
    assert not a["available"]
    ledger = coin_adapter.ledger()
    assert ledger["entries"][-1]["type"] == "tip"
    assert not ledger["available"]


def test_reward_no_crash():
    res = coin_adapter.reward(1, {"creator": 1.0})
    assert res["ok"]
    assert not res["available"]
