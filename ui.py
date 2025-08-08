from __future__ import annotations

import os
import importlib
import importlib.util
from pathlib import Path
from typing import Dict

import numpy as np
import streamlit as st

with st.sidebar:
    # --- identity (species) ---
    spec = st.selectbox(
        "I am a…",
        ("human", "company", "ai"),
        index={"human": 0, "company": 1, "ai": 2}.get(st.session_state.get("species", "human"), 0),
        key="species"  # <— single, canonical key
    )
    # (Optional) mirror to a simpler name if you read it elsewhere
    st.session_state["user_species"] = spec

    # --- decision kind ---
    kind = st.session_state.get("decision_kind", "standard")
    st.selectbox(
        "Decision kind",
        ("standard", "important"),
        index=0 if kind == "standard" else 1,
        key="decision_kind",
        help="standard = 60% yes · important = 90% yes",
    )


# ──────────────────────────────────────────────────────────────────────────────
# App constants
# ──────────────────────────────────────────────────────────────────────────────
APP_TITLE = "superNova_2177"
APP_BRAND = "💫 superNova_2177 💫"

# Primary logical page -> python module. (We also auto-discover ./pages/*.py.)
PRIMARY_PAGES: Dict[str, str] = {
    "Feed": "pages.feed",
    "Chat": "pages.chat",
    "Messages": "pages.messages",
    "Profile": "pages.profile",
    "Proposals": "pages.proposals",
    "Decisions": "pages.decisions",
    "Execution": "pages.execution",
    # Example to enable the 3D page:
    # "Enter Metaverse": "pages.enter_metaverse",
}

PAGES_DIR = Path(__file__).parent / "pages"


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


def _inject_css() -> None:
    st.markdown(
        """
<style>
/* Base */
.stApp { background-color:#0a0a0a !important; color:#fff !important; }
.main .block-container { padding-top:18px !important; padding-bottom:96px !important; }

/* Sidebar */
[data-testid="stSidebar"]{
  background:#18181b !important; border-right:1px solid #222 !important; color:#fff !important;
}
[data-testid="stSidebar"] .stButton>button{
  background:#1f1f23 !important; color:#fff !important; border:0 !important;
  width:100% !important; height:36px !important; border-radius:10px !important;
  text-align:left !important; padding-left:12px !important; margin:3px 0 !important;
}
[data-testid="stSidebar"] .stButton>button:hover { background:#2a2a31 !important; }
[data-testid="stSidebar"] img { border-radius:50% !important }

/* Top “tiles” */
div[data-testid="column"] .stButton>button{
  background:#1b1b1f !important; color:#fff !important; border-radius:10px !important;
  border:1px solid #2c2c32 !important;
}
div[data-testid="column"] .stButton>button:hover{ border-color:#ff1493 !important; }

/* Inputs */
[data-testid="stTextInput"]>div { background:#242428 !important; border-radius:10px !important; }
[data-testid="stTextInput"] input { background:transparent !important; color:#fff !important; }
</style>
""",
        unsafe_allow_html=True,
    )


def _brand_header() -> None:
    st.markdown(
        f"""<div style="display:flex;gap:10px;align-items:center;">
                <h1 style="margin:0;">{APP_TITLE}</h1>
            </div>""",
        unsafe_allow_html=True,
    )


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
    img = Path("assets/profile_pic.png")
    if img.exists():
        st.image(str(img), width=96)
    else:
        st.markdown("![avatar](https://placehold.co/96x96?text=👤)")
    st.subheader("taha_gungor")
    st.caption("ceo / test_tech")
    st.caption("artist / will = …")
    st.caption("New York, New York, United States")
    st.caption("test_tech")
    st.divider()
    st.metric("Profile viewers", int(np.random.randint(2100, 2450)))
    st.metric("Post impressions", int(np.random.randint(1400, 1650)))
    st.divider()


def _sidebar_nav_buttons() -> None:
    def _btn(label: str, icon: str = "", sect: str = "nav"):
        key = f"{sect}_{label.lower().replace(' ', '_')}"
        if st.button((icon + " " if icon else "") + label, key=key, use_container_width=True):
            _goto(label)

    # Workspaces
    _btn("Test Tech", "🏠", "ws")
    _btn("superNova_2177", "✨", "ws")
    _btn("GLOBALRUNWAY", "🌍", "ws")
    st.caption(" ")
    st.divider()

    # Main pages
    _btn("Feed", "📰")
    _btn("Chat", "💬")
    _btn("Messages", "📬")
    _btn("Profile", "👤")
    _btn("Proposals", "📑")
    _btn("Decisions", "✅")
    _btn("Execution", "⚙️")

    st.divider()
    st.subheader("Premium features")
    _btn("Music", "🎶", "premium")
    _btn("Agents", "🚀", "premium")
    _btn("Enter Metaverse", "🌌", "premium")
    st.caption("Mathematically sucked into a superNova_2177 void – stay tuned for 3D immersion")
    st.divider()

    _btn("Settings", "⚙️", "system")


def _backend_controls() -> None:
    use_real = st.toggle("Use real backend", value=_using_real_backend(), key="toggle_real_backend")
    url = st.text_input("Backend URL", value=_current_backend_url(), key="backend_url_input")
    st.session_state["use_real_backend"] = use_real
    st.session_state["backend_url"] = url
    _apply_backend_env(use_real, url)


def _search_box() -> None:
    st.text_input("Search posts, people…", key="search_query", label_visibility="collapsed", placeholder="🔍 Search…")


def _goto(page_label: str) -> None:
    """Set the current page and rerun using the stable API."""
    pages = st.session_state["__pages_map__"]
    if page_label not in pages and page_label.title() in pages:
        page_label = page_label.title()
    if page_label in pages:
        st.session_state["current_page"] = page_label
        st.rerun()  # stable replacement for deprecated st.experimental_rerun


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────
def main() -> None:
    # IMPORTANT: run THIS script (not Streamlit's built-in multipage runner), so
    # our router is used and the default “radio-list” nav never appears.
    st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

    _inject_css()
    _init_state()

    # Sidebar (reordered as requested: avatar -> brand -> search -> backend -> nav)
    with st.sidebar:
        _sidebar_profile()
        if st.button(APP_BRAND, key="brand_btn", use_container_width=True):
            _goto("Feed")
        _search_box()
        _backend_controls()
        _sidebar_nav_buttons()

    # Top
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
