# services/supernova_client.py
from __future__ import annotations
import os, requests
from typing import Any, Dict, Optional

BACKEND = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
TMO = 15

def _p(u: str) -> str: return f"{BACKEND.rstrip('/')}{u}"

def health() -> bool:
    try:
        return requests.get(_p("/healthz"), timeout=5).ok
    except Exception:
        return False

def status() -> Dict[str, Any]:
    return requests.get(_p("/status"), timeout=TMO).json()

def entropy_details(token: str) -> Dict[str, Any]:
    return requests.get(_p("/system/entropy-details"), headers={"Authorization": f"Bearer {token}"}, timeout=TMO).json()

def predictions() -> Dict[str, Any]:
    return requests.get(_p("/api/system-predictions"), timeout=TMO).json()

def quantum() -> Dict[str, Any]:
    return requests.get(_p("/api/quantum-status"), timeout=TMO).json()

def network(token: str) -> Dict[str, Any]:
    return requests.get(_p("/network-analysis/"), headers={"Authorization": f"Bearer {token}"}, timeout=TMO).json()

def sim_negentropy(token: str) -> Dict[str, Any]:
    return requests.get(_p("/sim/negentropy"), headers={"Authorization": f"Bearer {token}"}, timeout=TMO).json()

def sim_entangle(token: str, target_id: int) -> Dict[str, Any]:
    return requests.get(_p(f"/sim/entangle/{target_id}"), headers={"Authorization": f"Bearer {token}"}, timeout=TMO).json()

def create_vibenode(token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return requests.post(_p("/vibenodes/"), json=payload, headers={"Authorization": f"Bearer {token}"}, timeout=TMO).json()

def remix(token: str, vibenode_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
    return requests.post(_p(f"/vibenodes/{vibenode_id}/remix"), json=payload, headers={"Authorization": f"Bearer {token}"}, timeout=TMO).json()

def like(token: str, vibenode_id: int) -> Dict[str, Any]:
    return requests.post(_p(f"/vibenodes/{vibenode_id}/like"), headers={"Authorization": f"Bearer {token}"}, timeout=TMO).json()

def vote(proposal_id: int, voter: str, choice: str, species: str="human") -> Dict[str, Any]:
    return requests.post(_p(f"/api/votes/{proposal_id}"), json={"voter": voter, "choice": choice, "species": species}, timeout=TMO).json()

def tally(proposal_id: int) -> Dict[str, Any]:
    return requests.get(_p(f"/api/votes/{proposal_id}/tally"), timeout=TMO).json()

def decide_vote(proposal_id: int, level: str="standard") -> Dict[str, Any]:
    return requests.get(_p(f"/api/votes/{proposal_id}/decide"), params={"level": level}, timeout=TMO).json()

def fork(token: str, custom_config: Dict[str, Any]) -> Dict[str, Any]:
    return requests.post(_p("/api/fork"), json=custom_config, headers={"Authorization": f"Bearer {token}"}, timeout=TMO).json()

def ai_assist(token: str, vibenode_id: int, prompt: str) -> Dict[str, Any]:
    return requests.post(_p(f"/ai-assist/{vibenode_id}"), json={"prompt": prompt}, headers={"Authorization": f"Bearer {token}"}, timeout=TMO).json()
