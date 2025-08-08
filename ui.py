# ui.py — polished shell + sidebar + router
from __future__ import annotations

import os
import importlib
import importlib.util
from pathlib import Path
from typing import Dict

import numpy as np
import streamlit as st

# ──────────────────────────────────────────────────────────────────────────────
# App constants
# ──────────────────────────────────────────────────────────────────────────────
APP_TITLE = "superNova_2177"
APP_BRAND = "💫 superNova_2177 💫"
PAGES_DIR = Path(__file__).parent / "pages"

# Primary logical page -> python module. (Also auto-discovers ./pages/*.py.)
PRIMARY_PAGES: Dict[str, str] = {
    "Feed": "pages.feed",
    "Chat": "pages.chat",
    "Messages": "pages.messages",
    "Profile": "pages.profile",
    "Proposals": "pages.proposals",
    "Decisions": "pages.decisions",
    "Execution": "pages.execution",
    "Karma": "pages.karma",
    # "Enter Metaverse": "pages.enter_metaverse",
}

# ──────────────────────────────────────────────────────────────────────────────
# Backend flags & env
# ──────────────────────────────────────────────────────────────────────────────
def _bool_env(name: str, default: bool = False) -> bool:
    val = os.environ.get(name, "")
    return default if not val else val.strip().lower() in {"1", "true", "yes", "on"}

def _apply_backend_env(use_real: bool, url: str) -> None:
    os.environ["USE_REAL_BACKEND"] = "1" if use_real else "0"
    if url:
        os.environ["BACKEND_URL"] = url

def _using_real_backend() -> bool:
    return st.session_state.get("use_real_backend", _bool_env("USE_REAL_BACKEND", False))

def _current_backend_url() -> str:
    return st.session_state.get("backend_url", os.environ.get("BACKEND_URL", "http://127.0.0.1:8000"))

# ──────────────────────────────────────────────────────────────────────────────
# Page discovery & safe import
# ──────────────────────────────────────────────────────────────────────────────
def _discover_pages() -> Dict[str, str]:
    """PRIMARY_PAGES first, then fill any gaps by scanning ./pages/*.py."""
    pages = dict(PRIMARY_PAGES)
    if PAGES_DIR.exists():
        for py in PAGES_DIR.glob("*.py"):
            slug = py.stem
            if slug.startswith("_"):
                continue
            label = slug.replace("_", " ").title()
            mod = f"pages.{slug}"
            pages.setdefault(label, mod)
    return pages

def _import_module(mod_str: str):
    """Import by module string; fallback to direct file import from ./pages."""
    try:
        return importlib.import_module(mod_str)
    except Exception:
        last = mod_str.split(".")[-1]
        candidate = PAGES_DIR / f"{last}.py"
        if candidate.exists():
            spec = importlib.util.spec_from_file_location(mod_str, candidate)
            module = importlib.util.module_from_spec(spec)  # type: ignore
            assert spec and spec.loader
            spec.loader.exec_module(module)  # type: ignore
            return module
    return None

def _call_entry(module) -> None:
    fn = getattr(module, "render", None) or getattr(module, "main", None)
    if callable(fn):
        fn()
    else:
        st.warning("This page is missing a render()/main() function.")
        st.write("Add a `render()` or `main()` to the page module to display content.")

def render_page(label: str) -> None:
    pages = st.session_state["__pages_map__"]
    mod_str = pages.get(label)
    if not mod_str:
        st.error(f"Unknown page: {label}")
        return
    module = _import_module(mod_str)
    if module is None:
        st.error(f"Could not load {mod_str} for '{label}'.")
        return
    try:
        _call_entry(module)
    except Exception as e:
        st.error(f"Error rendering {label}: {e}")
        st.exception(e)

# ──────────────────────────────────────────────────────────────────────────────
# Polished UI pieces
# ──────────────────────────────────────────────────────────────────────────────
def _init_state() -> None:
    st.session_state.setdefault("theme", "dark")
    st.session_state.setdefault("current_page", "Feed")
    st.session_state.setdefault("use_real_backend", _bool_env("USE_REAL_BACKEND", False))
    st.session_state.setdefault("backend_url", os.environ.get("BACKEND_URL", "http://127.0.0.1:8000"))
    st.session_state.setdefault("__pages_map__", _discover_pages())
    st.session_state.setdefault("search_query", "")
    st.session_state.setdefault("decision_kind", "standard")
    st.session_state.setdefault("species", st.session_state.get("species", "human"))

def _inject_css() -> None:
    st.markdown(
        """
<style>
:root{
  --bg:#0a0b10; --panel:#0f1117; --panel-2:#10131a; --card:#11131d;
  --stroke:#1c2130; --muted:#a1a7b3; --text:#e9ecf1; --brand:#9b8cff;
  --ring:rgba(155,140,255,.35);
}
.stApp { background: var(--bg) !important; color: var(--text) !important; }
.main .block-container { padding-top:18px !important; padding-bottom:96px !important; }

/* Sidebar container */
[data-testid="stSidebar"]{
  background: radial-gradient(90% 70% at 0% 0%, rgba(155,140,255,.08), transparent 60%),
              linear-gradient(180deg, var(--panel), var(--panel-2));
  border-right:1px solid var(--stroke) !important; color:#fff !important;
}

/* Sidebar profile card */
.sn-card{
  border:1px solid var(--stroke); background:var(--card);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.04), 0 10px 30px rgba(0,0,0,.25);
  border-radius:16px; padding:12px; margin-bottom:10px;
}
.sn-pill{
  display:inline-flex; align-items:center; gap:.45rem; padding:.25rem .6rem;
  border-radius:999px; border:1px solid var(--stroke); color:#c7d2fe;
  background:#0f1320; font-size:.8rem;
}
.sn-section{ font-size:.8rem; color:var(--muted); margin:6px 0 2px; }

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton>button{
  background:#131724 !important; color:#e5e7eb !important; border:1px solid var(--stroke) !important;
  width:100% !important; height:38px !important; border-radius:12px !important;
  text-align:left !important; padding-left:12px !important; margin:4px 0 !important; font-weight:600;
}
[data-testid="stSidebar"] .stButton>button:hover {
  background:#151a2a !important; border-color:#2e374d !important;
  box-shadow:0 0 0 2px var(--ring) inset !important;
}
[data-testid="stSidebar"] img { border-radius:12px !important }

/* Brand header & top tiles */
.sn-brand { display:flex; gap:10px; align-items:center; }
.sn-brand h1 { margin:0; letter-spacing:.3px }
div[data-testid="column"] .stButton>button{
  background:#12182a !important; color:#fff !important; border-radius:12px !important;
  border:1px solid var(--stroke) !important;
}
div[data-testid="column"] .stButton>button:hover{
  border-color:#394156 !important; box-shadow:0 0 0 2px var(--ring) inset !important;
}

/* Inputs */
[data-testid="stTextInput"]>div { background:#161a28 !important; border-radius:12px !important; border:1px solid var(--stroke) !important; }
[data-testid="stTextInput"] input { background:transparent !important; color:#fff !important; }

/* Small divider bar used in feed header area (visual rhythm) */
.sn-sweep { height:10px; border-radius:999px; background:linear-gradient(90deg, rgba(155,140,255,.16), rgba(155,140,255,0) 70%); border:1px solid var(--stroke); }
</style>
""",
        unsafe_allow_html=True,
    )

def _goto(page_label: str) -> None:
    """Set the current page and rerun using the stable API."""
    pages = st.session_state["__pages_map__"]
    if page_label not in pages and page_label.title() in pages:
        page_label = page_label.title()
    if page_label in pages:
        st.session_state["current_page"] = page_label
        st.rerun()

def _nav_tile(icon: str, label: str) -> None:
    key = f"top_{label.lower().replace(' ', '_')}"
    if st.button(f"{icon} {label}", key=key, use_container_width=True):
        _goto(label)

def _top_shortcuts() -> None:
    cols = st.columns([1, 1, 1, 1, 6])
    tiles = [("🗳️", "Voting"), ("📄", "Proposals"), ("✅", "Decisions"), ("⚙️", "Execution")]
    for (icon, label), col in zip(tiles, cols):
        with col:
            _nav_tile(icon, label)

def _sidebar_profile() -> None:
    with st.container(border=True):
        st.markdown('<div class="sn-card">', unsafe_allow_html=True)
        st.image("https://placehold.co/320x160/11131d/FFFFFF?text=superNova_2177", use_container_width=True)
        st.markdown("**taha_gungor**")
        st.caption("ceo / test_tech")
        st.caption("artist / will = …")
        st.caption("New York, New York, United States")
        st.caption("test_tech")
        st.markdown('</div>', unsafe_allow_html=True)

        colA, colB = st.columns(2)
        with colA:
            st.metric("Profile viewers", int(np.random.randint(2100, 2450)))
        with colB:
            st.metric("Post impressions", int(np.random.randint(1400, 1650)))

def _sidebar_identity_controls() -> None:
    st.markdown("#### superNova_2177 🪐")
    # --- identity (species)
    spec = st.selectbox(
        "I am a…",
        ("human", "company", "ai"),
        index={"human": 0, "company": 1, "ai": 2}.get(st.session_state.get("species", "human"), 0),
        key="species",
        help="Used by weighted voting & agents. Purely symbolic.",
    )
    st.session_state["user_species"] = spec

    # --- decision kind
    kind = st.session_state.get("decision_kind", "standard")
    st.selectbox(
        "Decision kind",
        ("standard", "important"),
        index=0 if kind == "standard" else 1,
        key="decision_kind",
        help="standard = 60% yes · important = 90% yes",
    )

def _backend_controls() -> None:
    st.markdown("<div class='sn-section'>Backend</div>", unsafe_allow_html=True)
    use_real = st.toggle("Use real backend", value=_using_real_backend(), key="toggle_real_backend")
    url = st.text_input("Backend URL", value=_current_backend_url(), key="backend_url_input", placeholder="http://127.0.0.1:8000")
    st.session_state["use_real_backend"] = use_real
    st.session_state["backend_url"] = url
    _apply_backend_env(use_real, url)

def _search_box() -> None:
    st.text_input("Search posts, people…", key="search_query", label_visibility="collapsed", placeholder="🔍 Search…")

def _sidebar_nav_buttons() -> None:
    def _btn(label: str, icon: str = "", sect: str = "nav"):
        key = f"{sect}_{label.lower().replace(' ', '_')}"
        if st.button((icon + " " if icon else "") + label, key=key, use_container_width=True):
            _goto(label)

    st.markdown("<div class='sn-section'>Workspaces</div>", unsafe_allow_html=True)
    _btn("Test Tech", "🏠", "ws")
    _btn("superNova_2177", "✨", "ws")
    _btn("GLOBALRUNWAY", "🌍", "ws")
    st.divider()

    st.markdown("<div class='sn-section'>Navigate</div>", unsafe_allow_html=True)
    _btn("Feed", "📰")
    _btn("Chat", "💬")
    _btn("Messages", "📬")
    _btn("Profile", "👤")
    _btn("Proposals", "📑")
    _btn("Decisions", "✅")
    _btn("Execution", "⚙️")

    pages_map = st.session_state.get("__pages_map__", {})
    for label, icon in [("Coin", "🪙"), ("Forks", "🍴"), ("Remixes", "🎛️")]:
        if label in pages_map:
            _btn(label, icon)

    st.divider()
    st.subheader("Premium")
    _btn("Music", "🎶", "premium")
    _btn("Agents", "🚀", "premium")
    _btn("Enter Metaverse", "🌌", "premium")
    st.caption("Mathematically sucked into a superNova_2177 void – stay tuned for 3D immersion")
    st.divider()
    _btn("Settings", "⚙️", "system")

def _brand_header() -> None:
    st.markdown(
        f"""<div class="sn-brand"><h1>{APP_TITLE}</h1></div>""",
        unsafe_allow_html=True,
    )
    st.markdown('<div class="sn-sweep"></div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────
def main() -> None:
    # Run THIS file as your app entrypoint so we control nav/routing.
    st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

    _inject_css()
    _init_state()

    # Sidebar: profile → identity → search → backend → nav
    with st.sidebar:
        _sidebar_profile()
        if st.button(APP_BRAND, key="brand_btn", use_container_width=True):
            _goto("Feed")
        _sidebar_identity_controls()
        _search_box()
        _backend_controls()
        _sidebar_nav_buttons()

    # Top brand & quick actions
    _brand_header()
    _top_shortcuts()

    # Search mode (placeholder)
    query = st.session_state.get("search_query", "").strip()
    if query:
        st.subheader(f'Searching for: "{query}"')
        st.info("Search results placeholder – wire this up to your backend when ready.")
        st.write("• Users:")
        for i in range(3):
            st.write(f"  - user_{i}_{query}")
        st.write("• Posts:")
        for i in range(3):
            st.write(f"  - post_{i}_{query}")
        return

    # Page render
    current = st.session_state.get("current_page", "Feed")
    pages = st.session_state["__pages_map__"]
    if current not in pages:
        current = "Feed"
        st.session_state["current_page"] = current
    render_page(current)

if __name__ == "__main__":
    main()
