from __future__ import annotations
import os, json, requests
from typing import Any, Dict, List, Optional

DEFAULT_BACKEND = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
TMO = 20

class SupernovaClient:
    def __init__(self, base_url: str = DEFAULT_BACKEND, token: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.token = token or ""

    # ---- internals ---------------------------------------------------------
    def _h(self) -> Dict[str, str]:
        return ({"Authorization": f"Bearer {self.token}"} if self.token else {})

    def _get(self, path: str, auth: bool = False, params: Dict[str, Any] | None = None):
        try:
            r = requests.get(self.base_url + path, headers=(self._h() if auth else {}), params=params, timeout=TMO)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"error": str(e), "path": path}

    def _post(self, path: str, data: Dict[str, Any] | None = None, auth: bool = False):
        try:
            r = requests.post(self.base_url + path, json=(data or {}), headers=(self._h() if auth else {}), timeout=TMO)
            r.raise_for_status()
            return r.json() if r.headers.get("content-type","").startswith("application/json") else {"ok": True}
        except Exception as e:
            return {"error": str(e), "path": path, "data": data}

    # ---- system / analysis --------------------------------------------------
    def healthz(self): return self._get("/healthz")
    def status(self):  return self._get("/status")
    def entropy_details(self): return self._get("/system/entropy-details", auth=True)
    def system_predictions(self): return self._get("/api/system-predictions")
    def quantum_status(self): return self._get("/api/quantum-status")
    def network(self): return self._get("/network-analysis/", auth=True)
    def sim_negentropy(self): return self._get("/sim/negentropy", auth=True)
    def entangle(self, target_id: int): return self._get(f"/sim/entangle/{int(target_id)}", auth=True)

    # ---- content ------------------------------------------------------------
    def create_vibenode(self, name: str, description: str, tags: Optional[List[str]] = None,
                        media_type: str = "text", parent_vibenode_id: Optional[int] = None,
                        patron_saint_id: Optional[int] = None, media_url: Optional[str] = None):
        payload: Dict[str, Any] = {"name": name, "description": description, "media_type": media_type}
        if tags: payload["tags"] = tags
        if parent_vibenode_id: payload["parent_vibenode_id"] = parent_vibenode_id
        if patron_saint_id: payload["patron_saint_id"] = patron_saint_id
        if media_url: payload["media_url"] = media_url
        return self._post("/vibenodes/", payload, auth=True)

    def remix(self, vibenode_id: int, name: Optional[str] = None, description: Optional[str] = None):
        payload: Dict[str, Any] = {}
        if name is not None: payload["name"] = name
        if description is not None: payload["description"] = description
        return self._post(f"/vibenodes/{int(vibenode_id)}/remix", payload, auth=True)

    def like(self, vibenode_id: int):
        return self._post(f"/vibenodes/{int(vibenode_id)}/like", auth=True)

    # ---- AI assist ----------------------------------------------------------
    def ai_assist(self, vibenode_id: int, prompt: str):
        return self._post(f"/ai-assist/{int(vibenode_id)}", {"prompt": prompt}, auth=True)

    # ---- governance (no auth in stub router) --------------------------------
    def vote(self, proposal_id: int, voter: str, choice: str, species: str = "human"):
        return self._post(f"/api/votes/{int(proposal_id)}", {"voter": voter, "choice": choice, "species": species})
    def tally(self, proposal_id: int):
        return self._get(f"/api/votes/{int(proposal_id)}/tally")
    def decide(self, proposal_id: int, level: str = "standard"):
        return self._get(f"/api/votes/{int(proposal_id)}/decide", params={"level": level})
    def fork(self, custom_config: Dict[str, Any]):
        return self._post("/api/fork", custom_config, auth=True)
