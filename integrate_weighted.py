# integrate_weighted.py
# ruff: noqa: E501
"""
One-shot safe patcher:
- Ensure weighted voting engine exists in superNova_2177.py
- Inject species selector into ui.py (sidebar)
- Append Weighted Voting panel to pages/proposals.py
- Append Weighted Decision panel to pages/decisions.py
- De-duplicate common keys in pages/agents.py (adds _v2)
Idempotent: running twice will skip already-applied blocks.
"""

from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def write(p: Path, s: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")
    print(f"[OK] updated {p.relative_to(ROOT)}")


ENGINE_BLOCK = r"""
# === WEIGHTED VOTING ENGINE (auto-added) =====================================
from dataclasses import dataclass
from typing import Literal, Dict, List

Species = Literal["human","company","ai"]
DecisionLevel = Literal["standard","important"]
THRESHOLDS: Dict[DecisionLevel, float] = {"standard": 0.60, "important": 0.90}

@dataclass
class Vote:
    proposal_id: int
    voter: str
    choice: Literal["up","down"]
    species: Species

_WEIGHTED_VOTES: List[Vote] = []

def vote_weighted(proposal_id: int, voter: str, choice: str, species: str="human"):
    c = "up" if str(choice).lower() in {"up","yes","y","approve"} else "down"
    s = str(species).lower()
    if s not in {"human","company","ai"}: s = "human"
    _WEIGHTED_VOTES.append(Vote(int(proposal_id), str(voter or "anon"), c, s))
    return {"ok": True}

def _species_shares(active: List[Species]) -> Dict[Species, float]:
    present = sorted(set(active))
    if not present: return {}
    share = 1.0 / len(present)  # ⅓ each if all present; renormalized if not
    return {s: share for s in present}

def tally_proposal_weighted(proposal_id: int):
    V = [v for v in _WEIGHTED_VOTES if v.proposal_id == int(proposal_id)]
    if not V:
        return {"up": 0.0, "down": 0.0, "total": 0.0, "per_voter_weights": {}, "counts": {}}
    shares = _species_shares([v.species for v in V])
    counts: Dict[Species, int] = {s: 0 for s in shares}
    for v in V:
        counts[v.species] = counts.get(v.species, 0) + 1
    per_voter = {s: (shares[s] / counts[s]) for s in counts if counts[s] > 0}
    up = sum(per_voter.get(v.species,0.0) for v in V if v.choice=="up")
    down = sum(per_voter.get(v.species,0.0) for v in V if v.choice=="down")
    total = up + down
    return {"up": up, "down": down, "total": total, "per_voter_weights": per_voter, "counts": counts}

def decide_weighted_api(proposal_id: int, level: str="standard"):
    t = tally_proposal_weighted(proposal_id)
    thr = THRESHOLDS["important" if level=="important" else "standard"]
    status = "accepted" if (t["total"]>0 and (t["up"]/t["total"])>=thr) else "rejected"
    t.update({"proposal_id": int(proposal_id), "status": status, "threshold": thr})
    return t
# === END WEIGHTED VOTING ENGINE ==============================================
""".strip(
    "\n"
)

SIDEBAR_SPECIES = r"""
    # --- identity (species) ---
    st.selectbox("I am a…", ["human","company","ai"], key="species")
""".strip(
    "\n"
)

PROPOSALS_PANEL = r"""
# --- WEIGHTED VOTING PANEL (auto-added) --------------------------------------
from services import voting_adapter

def _weighted_panel_for_proposal(pid: int):
    import streamlit as st
    species = st.session_state.get("species", "human")
    c1, c2 = st.columns(2)
    with c1:
        if st.button(f"👍 Vote UP (weighted) #{pid}", key=f"wup_{pid}"):
            voting_adapter.register_vote(pid, st.session_state.get('username','anon'), 'up', species)
            st.rerun()
    with c2:
        if st.button(f"👎 Vote DOWN (weighted) #{pid}", key=f"wdown_{pid}"):
            voting_adapter.register_vote(pid, st.session_state.get('username','anon'), 'down', species)
            st.rerun()
    t = voting_adapter.tally_votes(pid)
    pct = (t['up']/t['total']*100) if t['total'] else 0.0
    st.caption(f"Weighted: {t['up']:.3f} ↑ / {t['down']:.3f} ↓ — total {t['total']:.3f}  ({pct:.1f}% yes)")
# --- END WEIGHTED VOTING PANEL -----------------------------------------------
""".strip(
    "\n"
)

DECISIONS_PANEL = r"""
# --- WEIGHTED DECISION PANEL (auto-added) ------------------------------------
from services import voting_adapter

def _weighted_decide_block(pid: int):
    import streamlit as st
    level = st.selectbox("Decision level", ["standard","important"], index=0, key=f"dec_level_{pid}")
    t = voting_adapter.tally_votes(pid)
    pct = (t['up']/t['total']*100) if t['total'] else 0.0
    st.caption(f"Weighted: {t['up']:.3f} ↑ / {t['down']:.3f} ↓ — total {t['total']:.3f}  ({pct:.1f}% yes)")
    if st.button(f"Decide (weighted) #{pid}", key=f"wdec_{pid}"):
        res = voting_adapter.decide_vote(pid, level)
        st.success(f\"{res['status'].upper()} at {int(res['threshold']*100)}% threshold\")
# --- END WEIGHTED DECISION PANEL ---------------------------------------------
""".strip(
    "\n"
)


def patch_supernova_engine():
    # Try both names users used
    candidates = [ROOT / "superNova_2177.py", ROOT / "supernova_2177.py"]
    for p in candidates:
        if p.exists():
            s = read(p)
            if "def vote_weighted(" in s and "def tally_proposal_weighted(" in s:
                print("[=] engine already present in", p.name)
                return
            s = s.rstrip() + "\n\n" + ENGINE_BLOCK + "\n"
            write(p, s)
            return
    # If file missing, create superNova_2177.py with just the engine
    p = ROOT / "superNova_2177.py"
    base = "# superNova_2177 (auto-created shell)\n"
    write(p, base + "\n\n" + ENGINE_BLOCK + "\n")


def patch_ui_sidebar_species():
    p = ROOT / "ui.py"
    s = read(p)
    if not s:
        print("[!] ui.py not found, skipping sidebar species injection.")
        return
    if 'st.selectbox("I am a…"' in s or "I am a..." in s:
        print("[=] species selector already present in ui.py")
        return
    # insert after the first 'with st.sidebar:' line
    m = re.search(r"with\s+st\.sidebar\s*:\s*\n", s)
    if not m:
        print("[!] could not find 'with st.sidebar:' in ui.py; skipping.")
        return
    insert_at = m.end()
    s2 = s[:insert_at] + SIDEBAR_SPECIES + "\n" + s[insert_at:]
    write(p, s2)


def append_block_once(p: Path, marker_start: str, block_text: str):
    s = read(p)
    if not s:
        print(f"[!] {p} not found; skipping.")
        return
    if marker_start in s:
        print(f"[=] block already present in {p.name}")
        return
    s2 = s.rstrip() + "\n\n" + block_text + "\n"
    write(p, s2)


def patch_proposals_page():
    # Add the reusable panel function; your page should call _weighted_panel_for_proposal(pid)
    p = ROOT / "pages" / "proposals.py"
    append_block_once(p, "# --- WEIGHTED VOTING PANEL (auto-added)", PROPOSALS_PANEL)
    # Light-touch hint: try to auto-inject a call if a common loop is found (best-effort)
    s = read(p)
    # If there's a "for pid in" looking loop, try to add a call
    pat = r"(for\s+.+?\s+in\s+.+?:\s*\n(?:[ \t].*\n)+)"

    def add_call(m):
        blk = m.group(1)
        if "_weighted_panel_for_proposal(" in blk:
            return blk
        # append a call indented at same level
        lines = blk.splitlines(True)
        indent = re.match(r"(\s*)", lines[-1]).group(1) if lines else "    "
        lines.append(indent + "_weighted_panel_for_proposal(pid)\n")
        return "".join(lines)

    s2 = re.sub(pat, add_call, s, count=1, flags=re.DOTALL)
    if s2 != s:
        write(p, s2)
    else:
        print(
            "[~] Could not auto-inject weighted call in proposals.py; call it where you render each proposal: _weighted_panel_for_proposal(pid)"
        )


def patch_decisions_page():
    p = ROOT / "pages" / "decisions.py"
    append_block_once(p, "# --- WEIGHTED DECISION PANEL (auto-added)", DECISIONS_PANEL)
    s = read(p)
    # Try to append a call near where proposals are iterated
    pat = r"(for\s+.+?\s+in\s+.+?:\s*\n(?:[ \t].*\n)+)"

    def add_call(m):
        blk = m.group(1)
        if "_weighted_decide_block(" in blk:
            return blk
        lines = blk.splitlines(True)
        indent = re.match(r"(\s*)", lines[-1]).group(1) if lines else "    "
        lines.append(indent + "_weighted_decide_block(pid)\n")
        return "".join(lines)

    s2 = re.sub(pat, add_call, s, count=1, flags=re.DOTALL)
    if s2 != s:
        write(p, s2)
    else:
        print(
            "[~] Could not auto-inject weighted decision call; call it where you list each proposal: _weighted_decide_block(pid)"
        )


def patch_agents_keys():
    p = ROOT / "pages" / "agents.py"
    s = read(p)
    if not s:
        print("[i] pages/agents.py not found; skipping key fix.")
        return

    # add _v2 to any key="agents_*" that lacks it
    def repl(m):
        full = m.group(0)
        keyname = m.group(1)
        if keyname.endswith("_v2"):
            return full
        return full.replace(keyname, keyname + "_v2")

    s2 = re.sub(r'key\s*=\s*"((?:agents_)[a-zA-Z0-9_]+)"', repl, s)
    if s2 != s:
        write(p, s2)
    else:
        print("[=] agents.py keys look unique already; no changes.")


def main():
    patch_supernova_engine()
    patch_ui_sidebar_species()
    patch_proposals_page()
    patch_decisions_page()
    patch_agents_keys()
    print("\n[DONE] Run:  streamlit run ui.py --server.port 8888")
    print(
        "If a page still doesn’t show the weighted UI, add a call where you render each proposal:\n  _weighted_panel_for_proposal(pid)\n  _weighted_decide_block(pid)"
    )


if __name__ == "__main__":
    main()
