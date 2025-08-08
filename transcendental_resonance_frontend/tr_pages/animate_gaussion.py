"""
)
with centered_container():
header("Diagnostics")
col1, col2 = st.columns(2)
with col1:
    st.info("📁 Expected Pages Directory")
    st.code(str(PAGES_DIR))
with col2:
    st.info("🔍 Directory Status")
    if PAGES_DIR.exists():
        st.success("Directory exists")
    else:
        st.error("Directory missing")
header("🎮 Available Features")
if st.button("Run Validation Analysis"):
    run_analysis([], layout="force")
if st.button("Show Boot Diagnostics"):
    boot_diagnostic_ui()
st.markdown(
"""
<style>
.landing-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}
.landing-overlay-content {
    background: rgba(30, 30, 30, 0.85);
    backdrop-filter: blur(6px);
    padding: 2rem 3rem;
    border-radius: 12px;
    text-align: center;
}
</style>
""",
unsafe_allow_html=True,
)
overlay = st.container()
with overlay:
st.markdown(
    "<div class='landing-overlay'><div class='landing-overlay-content'>",
    unsafe_allow_html=True,
)
st.markdown("### Quick Actions", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if st.button("Create Proposal", key="landing_create_proposal"):
        load_page_with_fallback(
            "Voting",
            [
                f"transcendental_resonance_frontend.tr_pages.{PAGES.get('Voting', 'voting')}",
                f"pages.{PAGES.get('Voting', 'voting')}",
            ],
        )
with col2:
    if st.button("Run Validation", key="landing_run_validation"):
        run_analysis([], layout="force")
st.markdown("</div></div>", unsafe_allow_html=True)

def load_page_with_fallback(choice: str, module_paths: list[str] | None = None) -> None:
choice = normalize_choice(choice)
if module_paths is None:
module = PAGES.get(choice)
if not module and choice.lower() in PAGES.values():
    module = choice.lower()
if not module:
    st.error(f"Unknown page: {choice}")
    if "_render_fallback" in globals():
        _render_fallback(choice)
    return
module_paths = [
    f"transcendental_resonance_frontend.tr_pages.{module}",
    f"pages.{module}",
]
PAGES_DIR = get_pages_dir()
if not PAGES_DIR.exists():
st.error(f"Pages directory not found: {PAGES_DIR}")
if "_render_fallback" in globals():
    _render_fallback(choice)
return
last_exc: Exception | None = None
attempted_paths = set()
for module_path in module_paths:
if module_path in attempted_paths:
    continue
attempted_paths.add(module_path)
filename = module_path.rsplit(".", 1)[-1] + ".py"
candidate_files = [
    ROOT_DIR / "pages" / filename,
    PAGES_DIR / filename,
]
for page_file in candidate_files:
    if page_file.exists():
        rel_path = f"pages/{page_file.stem}"
        try:
            st.switch_page(rel_path)
            _fallback_rendered.clear()
            return
        except StreamlitAPIException as exc:
            st.toast(f"Switch failed for {choice}: {exc}", icon="⚠️")
            logger.debug("File exists but switch failed: %s", page_file)
            break
        except Exception as exc:
            logging.error(
                "switch_page failed for %s: %s", rel_path, exc, exc_info=True
            )
            logger.debug("File exists but switch failed: %s", page_file)
            last_exc = exc
            break
try:
    page_mod = importlib.import_module(module_path)
    for method_name in ("render", "main"):
        if hasattr(page_mod, method_name):
            getattr(page_mod, method_name)()
            _fallback_rendered.clear()
            return
except ImportError:
    continue
except Exception as exc:
    last_exc = exc
    logging.error("Error executing %s: %s", module_path, exc, exc_info=True)
    break
st.toast("Unable to load page. Showing preview.", icon="⚠️")
if choice == "Validation":
st.error("Validation page failed to load")
if "_render_fallback" in globals():
_render_fallback(choice)
if last_exc:
with st.expander("Show error details"):
    st.exception(last_exc)
return

def _render_fallback(choice: str) -> None:
normalized = normalize_choice(choice)
slug = PAGES.get(normalized, str(normalized)).lower()
if "PYTEST_CURRENT_TEST" in os.environ:
fallback_pages = {
    "validation": render_modern_validation_page,
    "voting": render_modern_voting_page,
    "agents": render_modern_agents_page,
    "resonance music": render_modern_music_page,
    "chat": render_modern_chat_page,
    "social": render_modern_social_page,
    "profile": render_modern_profile_page,
}
fallback_fn = fallback_pages.get(slug)
if fallback_fn and slug not in _fallback_rendered:
    _fallback_rendered.add(slug)
    show_preview_badge("🚧 Preview Mode")
    fallback_fn()
return
if slug in _fallback_rendered:
return
_fallback_rendered.add(slug)
if not UI_DEBUG:
fallback_pages = {
    "validation": render_modern_validation_page,
    "voting": render_modern_voting_page,
    "agents": render_modern_agents_page,
    "resonance music": render_modern_music_page,
    "chat": render_modern_chat_page,
    "social": render_modern_social_page,
    "profile": render_modern_profile_page,
}
fallback_fn = fallback_pages.get(slug)
if fallback_fn:
    show_preview_badge("🚧 Preview Mode")
    fallback_fn()
return
OFFLINE_MODE = os.getenv("OFFLINE_MODE", "0") == "1"
page_candidates = [
ROOT_DIR / "pages" / f"{slug}.py",
get_pages_dir() / f"{slug}.py",
Path.cwd() / "pages" / f"{slug}.py",
]
loaded = False
if hasattr(st, "experimental_page"):
for page_file in page_candidates:
    if not page_file.exists():
        continue
    logger.debug("Attempting to load %s from %s", slug, page_file)
    try:
        spec = importlib.util.spec_from_file_location(
            f"_page_{slug}", page_file
        )
        if not spec or not spec.loader:
            continue
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        for fn in ("render", "main"):
            if hasattr(mod, fn):
                try:
                    getattr(mod, fn)()
                    loaded = True
                    break
                except Exception as exc:
                    logger.error(
                        "Error running %s.%s: %s",
                        slug, fn, exc, exc_info=True,
                    )
        if loaded:
            break
    except Exception as exc:
        logger.error(
            "Error loading page candidate %s: %s",
            page_file, exc, exc_info=True,
        )
if loaded:
return
fallback_pages = {
"validation": render_modern_validation_page,
"voting": render_modern_voting_page,
"agents": render_modern_agents_page,
"resonance music": render_modern_music_page,
"chat": render_modern_chat_page,
"social": render_modern_social_page,
"profile": render_modern_profile_page,
}
fallback_fn = fallback_pages.get(slug)
if fallback_fn:
logger.debug("Rendering fallback for %s", slug)
if OFFLINE_MODE:
    st.toast("Offline mode: using mock services", icon="⚠️")
show_preview_badge("🚧 Preview Mode")
fallback_fn()
else:
st.toast(f"No fallback available for page: {choice}", icon="⚠️")

def render_modern_validation_page():
render_title_bar("✅", "Validation Console")
st.markdown("**Timeline**")
st.markdown("- Task queued\n- Running analysis\n- Completed")
progress = st.progress(0)
for i in range(5):
time.sleep(0.1)
progress.progress((i + 1) / 5)
st.success("Status: OK")

def render_modern_voting_page():
render_title_bar("🗳️", "Voting Dashboard")
votes = {"Proposal A": 3, "Proposal B": 5}
total = sum(votes.values()) or 1
for label, count in votes.items():
st.write(f"{label}: {count} votes")
st.progress(count / total)

def render_modern_agents_page():
render_title_bar("🤖", "AI Agents")
agents = ["Guardian", "Oracle", "Resonance"]
cols = st.columns(len(agents))
for col, name in zip(cols, agents):
with col:
    st.image(
        "https://via.placeholder.com/80",
        width=80,
        use_container_width=True,
        caption=f"{name} avatar",
    )
    st.write(name)
    st.line_chart([1, 3, 2, 4])

def render_modern_music_page():
render_title_bar("🎵", "Resonance Music")
st.line_chart([0, 1, 0, -1, 0])
st.caption("Harmonic signature: A# minor")

def render_modern_social_page():
render_title_bar("👥", "Social Network")
posts = [
{"image": "https://placekitten.com/400/300", "text": "Cute kitten", "likes": 5},
{"image": "https://placekitten.com/300/300", "text": "Another cat", "likes": 3},
{"image": "https://placekitten.com/500/300", "text": "More cats", "likes": 8},
]
render_instagram_grid(posts, cols=3)

def render_modern_chat_page() -> None:
render_title_bar("💬", "Chat")
st.toast("Chat module not yet implemented.")

def render_modern_profile_page() -> None:
render_title_bar("👤", "Profile")
st.toast("Profile management pending implementation.")

def render_sidebar() -> str:
user = get_active_user()
avatar = user.get("profile_pic", "https://via.placeholder.com/64") if user else "https://via.placeholder.com/64"
username = user.get("username", "Guest") if user else "Guest"
render_profile_card(username, avatar)
with st.sidebar.expander("Create Proposal"):
st.button("Create Proposal")
with st.sidebar.expander("Run Validation"):
st.button("Run Validation")
dark = st.sidebar.toggle("Dark Mode", value=st.session_state.get("theme") == "dark")
st.session_state["theme"] = "dark" if dark else "light"
env = os.getenv("ENV", "development").lower()
env_tag = "🚀 Production" if env.startswith("prod") else "🧪 Development"
st.sidebar.markdown(env_tag)
icon_map = dict(zip(PAGES.keys(), NAV_ICONS))
choice_label = render_sidebar_nav(
PAGES,
container=st.sidebar,
icons=icon_map,
session_key="active_page",
)
return normalize_choice(PAGES.get(choice_label, choice_label))

def load_css() -> None:
pass

ACCENT_COLOR = "#4f8bf9"

from api_key_input import render_api_key_ui, render_simulation_stubs
from status_indicator import render_status_icon

try:
from ui_utils import load_rfc_entries, parse_summary, summarize_text, render_main_ui
except ImportError:  # pragma: no cover - optional dependency
def load_rfc_entries():
return []
def parse_summary(text):
return {"summary": text[:100] + "..." if len(text) > 100 else text}
def summarize_text(text):
return text[:200] + "..." if len(text) > 200 else text
def render_main_ui():
st.info("Main UI utilities not available")

# Database fallback for local testing
try:
import db_models
from db_models import Harmonizer, SessionLocal, UniverseBranch
DATABASE_AVAILABLE = True
except Exception:  # pragma: no cover - missing ORM
DATABASE_AVAILABLE = False
from stubs.mock_db import Harmonizer, SessionLocal, UniverseBranch

def _run_async(coro):
try:
loop = asyncio.get_running_loop()
except RuntimeError:
return asyncio.run(coro)
else:
if loop.is_running():
    return asyncio.run_coroutine_threadsafe(coro, loop).result()
return loop.run_until_complete(coro)

try:
from frontend_bridge import dispatch_route
except Exception:  # pragma: no cover - optional dependency
dispatch_route = None

try:
from introspection.introspection_pipeline import run_full_audit
except Exception:  # pragma: no cover - optional module
run_full_audit = None  # type: ignore

try:
from superNova_2177 import InMemoryStorage, agent, cosmic_nexus
except Exception:  # pragma: no cover - optional runtime globals
cosmic_nexus = None  # type: ignore
agent = None  # type: ignore
InMemoryStorage = None  # type: ignore

try:
from network.network_coordination_detector import build_validation_graph
from validation_integrity_pipeline import analyze_validation_integrity
except ImportError as exc:  # pragma: no cover - optional dependency
logger.warning("Analysis modules unavailable: %s", exc)
build_validation_graph = None  # type: ignore
analyze_validation_integrity = None  # type: ignore

try:
from validator_reputation_tracker import update_validator_reputations
except Exception:  # pragma: no cover - optional dependency
update_validator_reputations = None

def get_st_secrets() -> dict:
try:
return st.secrets  # type: ignore[attr-defined]
except Exception:  # pragma: no cover - optional in dev/CI
return {
    "SECRET_KEY": "dev",
    "DATABASE_URL": "sqlite:///:memory:",
}

sample_path = Path(__file__).resolve().parent / "sample_validations.json"

try:
from validation_certifier import Config as VCConfig
except Exception:  # pragma: no cover - optional debug dependencies
VCConfig = None  # type: ignore

try:
from config import Config
from superNova_2177 import HarmonyScanner
except Exception:  # pragma: no cover - optional debug dependencies
HarmonyScanner = None  # type: ignore
Config = None  # type: ignore

if Config is None:
class Config:  # type: ignore[no-redef]
METRICS_PORT = 1234

if VCConfig is None:
class VCConfig:  # type: ignore[no-redef]
HIGH_RISK_THRESHOLD = 0.7
MEDIUM_RISK_THRESHOLD = 0.4

if HarmonyScanner is None:
class HarmonyScanner:  # type: ignore[no-redef]
def __init__(self, *_a, **_k):
    pass
def scan(self, _data):
    return {"dummy": True}

def clear_memory(state: dict) -> None:
state["analysis_diary"] = []
state["run_count"] = 0
state["last_result"] = None
state["last_run"] = None

def export_latest_result(state: dict) -> str:
return json.dumps(state.get("last_result", {}), indent=2)

def diff_results(old: dict | None, new: dict) -> str:
if not old:
return ""
old_txt = json.dumps(old, indent=2, sort_keys=True).splitlines()
new_txt = json.dumps(new, indent=2, sort_keys=True).splitlines()
diff = difflib.unified_diff(
old_txt,
new_txt,
fromfile="previous",
tofile="new",
lineterm="",
)
return "\n".join(diff)

def generate_explanation(result: dict) -> str:
integrity = result.get("integrity_analysis", {})
if not integrity:
return "No integrity analysis available."
risk = integrity.get("risk_level", "unknown")
score = integrity.get("overall_integrity_score", "N/A")
lines = [f"Risk level: {risk}", f"Integrity score: {score}"]
recs = result.get("recommendations") or []
if recs:
lines.append("Recommendations:")
for r in recs:
    lines.append(f"- {r}")
return "\n".join(lines)

def run_analysis(validations, *, layout: str = "force"):
global nx, go
if nx is None:
try:
    import networkx as nx  # type: ignore
except ImportError:
    nx = None
if go is None:
try:
    import plotly.graph_objects as go  # type: ignore
except ImportError:
    go = None
if analyze_validation_integrity is None or build_validation_graph is None:
st.error(
    "Required analysis modules are missing. Please install optional dependencies."
)
return {}
if not validations:
try:
    with open(sample_path) as f:
        sample = json.load(f)
        validations = sample.get("validations", [])
except Exception:
    validations = [{"validator": "A", "target": "B", "score": 0.5}]
alert("No validations provided – using fallback data.", "warning")
if os.getenv("UI_DEBUG_PRINTS", "1") != "0":
    print("✅ UI diagnostic agent active")
with st.spinner("Loading..."):
result = analyze_validation_integrity(validations)
header("Validations")
render_instagram_grid(validations, cols=3)
consensus = result.get("consensus_score")
if consensus is not None:
st.metric("Consensus Score", round(consensus, 3))
integrity = result.get("integrity_analysis", {})
score = integrity.get("overall_integrity_score")
if score is not None:
color = "green"
if score < VCConfig.MEDIUM_RISK_THRESHOLD:
    color = "red"
elif score < VCConfig.HIGH_RISK_THRESHOLD:
    color = "yellow"
tooltip = (
    f"Green \u2265 {VCConfig.HIGH_RISK_THRESHOLD}, "
    f"Yellow \u2265 {VCConfig.MEDIUM_RISK_THRESHOLD}, "
    f"Red < {VCConfig.MEDIUM_RISK_THRESHOLD}"
)
st.markdown(
    f"<span title='{tooltip}' "
    f"style='background-color:{color};color:white;"
    f"padding:0.25em 0.5em;border-radius:0.25em;'>"
    f"Integrity Score: {score:.2f}</span>",
    unsafe_allow_html=True,
)
header("Analysis Result")
if st.session_state.get("beta_mode"):
st.json(result)
graph_data = build_validation_graph(validations)
edges = graph_data.get("edges", [])
if edges and nx is not None:
G = nx.Graph()
voter_meta: dict[str, dict[str, str]] = {}
for entry in validations:
    vid = entry.get("validator_id")
    if not vid:
        continue
    meta = voter_meta.setdefault(vid, {})
    cls = (
        entry.get("validator_class")
        or entry.get("class")
        or entry.get("affiliation")
        or entry.get("specialty")
    )
    species = entry.get("species") or entry.get("validator_species")
    if cls and "voter_class" not in meta:
        meta["voter_class"] = str(cls)
    if species and "species" not in meta:
        meta["species"] = str(species)
for node in graph_data.get("nodes", []):
    meta = voter_meta.get(node, {})
    G.add_node(
        node,
        voter_class=meta.get("voter_class", "unknown"),
        species=meta.get("species", "unknown"),
    )
for v1, v2, w in edges:
    G.add_edge(v1, v2, weight=w)
gm_buf = io.BytesIO()
try:
    nx.write_graphml(G, gm_buf)
    gm_buf.seek(0)
    st.download_button(
        "Download GraphML",
        gm_buf.getvalue(),
        file_name="graph.graphml",
    )
except Exception as exc:  # pragma: no cover - optional
    logger.warning(f"GraphML export failed: {exc}")
if layout == "circular":
    pos = nx.circular_layout(G)
elif layout == "grid":
    side = math.ceil(math.sqrt(len(G)))
    pos = {n: (i % side, i // side) for i, n in enumerate(G.nodes())}
else:
    pos = nx.spring_layout(G, seed=42)
reputations = {}
if update_validator_reputations:
    try:
        rep_result = update_validator_reputations(validations)
        if isinstance(rep_result, dict):
            reputations = rep_result.get("reputations", {})
    except Exception as exc:  # pragma: no cover - optional
        logger.warning(f"Reputation calc failed: {exc}")
if go is not None:
    edge_x = []
    edge_y = []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )
    node_x = []
    node_y = []
    texts = []
    node_sizes = []
    node_colors = []
    max_rep = max(reputations.values()) if reputations else 1.0
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        texts.append(str(node))
        rep = reputations.get(node)
        node_sizes.append(10 + (rep or 0) * 20)
        node_colors.append(rep if rep is not None else 0.5)
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=texts,
        hoverinfo="text",
        marker=dict(
            size=node_sizes,
            color=node_colors,
            colorscale="Viridis",
            cmin=0,
            cmax=max_rep,
            showscale=bool(reputations),
        ),
    )
    fig = go.Figure(data=[edge_trace, node_trace])
    header("Validator Coordination Graph")
    st.plotly_chart(fig, use_container_width=True)
    img_buf = io.BytesIO()
    try:
        fig.write_image(img_buf, format="png")
        img_buf.seek(0)
        st.download_button(
            "Download Graph Image",
            img_buf.getvalue(),
            file_name="graph.png",
        )
    except Exception as exc:  # pragma: no cover - optional
        logger.warning(f"Image export failed: {exc}")
else:
    st.info("Install plotly for graph visualization")
elif edges:
st.info("Install networkx for graph visualization")
if st.button("Explain This Score"):
explanation = generate_explanation(result)
with st.expander("Score Explanation"):
    st.markdown(explanation)
return result

def boot_diagnostic_ui():
header("Boot Diagnostic", layout="centered")
header("Config Test")
if Config is not None:
st.success("Config import succeeded")
st.write({"METRICS_PORT": Config.METRICS_PORT})
else:
alert("Config import failed", "error")
header("Harmony Scanner Check")
scanner = HarmonyScanner(Config()) if Config and HarmonyScanner else None
if scanner:
st.success("HarmonyScanner instantiated")
else:
alert("HarmonyScanner init failed", "error")
if st.button("Run Dummy Scan") and scanner:
try:
    scanner.scan("hello world")
    st.success("Dummy scan completed")
except Exception as exc:  # pragma: no cover - debug only
    alert(f"Dummy scan error: {exc}", "error")
header("Validation Analysis")
run_analysis([], layout="force")

def render_validation_ui(
sidebar: Optional[st.delta_generator.DeltaGenerator] = None,
main_container: Optional[st.delta_generator.DeltaGenerator] = None,
) -> None:
if sidebar is None:
sidebar = st.sidebar
if main_container is None:
main_container = st
try:
page_paths = {
    label: f"/pages/{mod}.py" for label, mod in PAGES.items()
}
choice_label = render_sidebar_nav(
    page_paths,
    icons=NAV_ICONS,
    session_key="active_page",
)
choice = PAGES.get(choice_label, str(choice_label)).lower()
left_col, center_col, _ = main_container.columns([1, 3, 1])
with center_col:
    st.info("Select a page above to continue.")
with left_col:
    render_status_icon()
    render_developer_tools()
except Exception as exc:
st.error("Failed to load validation UI")
st.code(str(exc))

def render_developer_tools() -> None:
st.markdown(
"""
<style>
.dev-tabs [data-testid="stTab"] button {padding:0.25rem 1rem;}
</style>
""",
unsafe_allow_html=True,
)
with st.expander("Developer Tools"):
if "cosmic_nexus" in globals() and "Harmonizer" in globals():
    try:
        user = get_active_user()
        if user and st.button("Fork with Mock Config"):
            try:
                fork_id = cosmic_nexus.fork_universe(
                    user, {"entropy_threshold": 0.5}
                )
                st.success(f"Forked universe {fork_id}")
            except Exception as exc:
                st.error(f"Fork failed: {exc}")
        elif not user:
            st.toast("No users available to fork")
    except Exception as exc:
        st.error(f"Database error: {exc}")
else:
    st.toast("Fork operation unavailable", icon="⚠️")
with st.expander("Diagnostics & Logs"):
    if "SessionLocal" in globals() and "UniverseBranch" in globals():
        try:
            with SessionLocal() as db:
                records = (
                    db.query(UniverseBranch)
                    .order_by(UniverseBranch.timestamp.desc())
                    .limit(5)
                    .all()
                )
                if records:
                    for r in records:
                        st.write(
                            {
                                "id": r.id,
                                "status": r.status,
                                "timestamp": r.timestamp,
                            }
                        )
                else:
                    st.write("No forks recorded")
        except Exception as exc:
            st.error(f"Database error: {exc}")
    else:
        st.toast("Database unavailable", icon="⚠️")
    hid = st.text_input("Hypothesis ID", key="audit_id")
    if st.button("Run Audit") and hid:
        if "dispatch_route" in globals() and "SessionLocal" in globals():
            try:
                with SessionLocal() as db:
                    with st.spinner("Working on it..."):
                        try:
                            result = _run_async(
                                dispatch_route(
                                    "trigger_full_audit",
                                    {"hypothesis_id": hid},
                                    db=db,
                                )
                            )
                            if st.session_state.get("beta_mode"):
                                st.json(result)
                            st.toast("Success!")
                        except Exception as exc:
                            st.error(f"Audit failed: {exc}")
            except Exception as exc:
                st.error(f"Database error: {exc}")
        elif "run_full_audit" in globals() and "SessionLocal" in globals():
            try:
                with SessionLocal() as db:
                    with st.spinner("Working on it..."):
                        try:
                            result = run_full_audit(hid, db)
                            if st.session_state.get("beta_mode"):
                                st.json(result)
                            st.toast("Success!")
                        except Exception as exc:
                            st.error(f"Audit failed: {exc}")
            except Exception as exc:
                st.error(f"Database error: {exc}")
        else:
            st.toast("Audit functionality unavailable", icon="⚠️")
    log_candidates = [
        Path("logchain_main.log"),
        Path("remix_logchain.log"),
        Path("transcendental_resonance.log"),
    ]
    log_path = next((p for p in log_candidates if p.exists()), None)
    searched_msg = ", ".join(p.name for p in log_candidates)
    if log_path is not None:
        try:
            lines = log_path.read_text(errors="ignore").splitlines()[-100:]
            st.text("\n".join(lines))
        except Exception:
            st.toast(f"Unable to read log file {log_path.name}", icon="⚠️")
        st.caption(f"Searched: {searched_msg}")
    else:
        st.toast(f"No log file found. Searched: {searched_msg}", icon="⚠️")
    with st.expander("Inject Event", expanded=False):
        event_json = st.text_area(
            "Event JSON", value="{}", height=150, key="inject_event"
        )
        if st.button("Process Event"):
            agent_obj = st.session_state.get("agent_instance") or globals().get(
                "agent"
            )
            if agent_obj is not None:
                try:
                    event = json.loads(event_json or "{}")
                    agent_obj.process_event(event)
                    st.success("Event processed")
                except Exception as exc:
                    st.error(f"Event failed: {exc}")
            else:
                st.toast("Agent unavailable")
    if "AGENT_REGISTRY" in globals():
        st.write("Available agents:", list(AGENT_REGISTRY.keys()))
    if "cosmic_nexus" in globals():
        st.write(
            "Sub universes:",
            list(getattr(cosmic_nexus, "sub_universes", {}).keys()),
        )
    agent_obj = st.session_state.get("agent_instance") or globals().get("agent")
    if agent_obj is not None and "InMemoryStorage" in globals():
        try:
            if isinstance(agent_obj.storage, InMemoryStorage):
                st.write(
                    f"Users: {len(agent_obj.storage.users)} / Coins: {len(agent_obj.storage.coins)}"
                )
            else:
                user_count = len(agent_obj.storage.get_all_users())
                st.write(f"User count: {user_count}")
        except Exception:
            st.toast("Inspection failed", icon="⚠️")
with st.expander("Playground"):
    flow_txt = st.text_area(
        "Agent Flow JSON", "[]", height=150, key="flow_json"
    )
    if st.button("Run Flow"):
        if "AGENT_REGISTRY" in globals():
            try:
                steps = json.loads(flow_txt or "[]")
                results = []
                for step in steps:
                    a_name = step.get("agent")
                    agent_cls = AGENT_REGISTRY.get(a_name, {}).get("class")
                    evt = step.get("event", {})
                    if agent_cls:
                        backend_fn = get_backend("dummy")
                        a = agent_cls(llm_backend=backend_fn)
                        results.append(a.process_event(evt))
                if st.session_state.get("beta_mode"):
                    st.json(results)
            except Exception as exc:
                st.error(f"Flow execution failed: {exc}")
        else:
            st.toast("Agent registry unavailable", icon="⚠️")

def parse_beta_mode(params: dict) -> bool:
val = params.get("beta")
enabled = val == "1" or (isinstance(val, list) and "1" in val)
st.session_state["beta_mode"] = enabled
return enabled

def main() -> None:
try:
st.set_page_config(
    page_title="superNova_2177",
    layout="wide",
    initial_sidebar_state="collapsed",
)
except Exception:
pass
st.markdown(
"""<style>
body, .stApp {background:#FAFAFA;}
.sn-card {border-radius:12px;box-shadow:0 2px 6px rgba(0,0,0,0.1);}
</style>""",
unsafe_allow_html=True,
)
try:
ensure_pages(PAGES, PAGES_DIR)
except Exception as exc:
logger.warning("ensure_pages failed: %s", exc)
try:
db_ready = ensure_database_exists()
if not db_ready:
    st.warning("Database initialization failed. Running in fallback mode")
except Exception as e:
st.error(f"Database initialization failed: {e}")
st.info("Running in fallback mode")
try:
params = st.query_params
except AttributeError:
params = st.experimental_get_query_params()
parse_beta_mode(params)
value = params.get(HEALTH_CHECK_PARAM)
path_info = os.environ.get("PATH_INFO", "").rstrip("/")
if (
value == "1"
or (isinstance(value, list) and "1" in value)
or path_info == f"/{HEALTH_CHECK_PARAM}"
):
st.write("ok")
st.stop()
return
try:
st.markdown(
    """
    <script>
    document.addEventListener('keydown', function(e) {
      const tag = document.activeElement.tagName;
      if (tag === 'INPUT' or tag === 'TEXTAREA') { return; }
      const params = new URLSearchParams(window.location.search);
      if (e.key === 'N' or e.key === 'n') {
        params.set('page', 'Voting');
        window.location.search = params.toString();
      }
      if (e.key === 'V' or e.key === 'v') {
        params.set('page', 'Validation');
        window.location.search = params.toString();
      }
    });
    </script>
    """,
    unsafe_allow_html=True,
)
defaults = {
    "session_start_ts": datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    ),
    "theme": "light",
    "governance_view": False,
    "validations_json": "",
    "agent_output": None,
    "last_result": None,
    "last_run": None,
    "diary": [],
    "analysis_diary": [],
    "run_count": 0,
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)
st.session_state.setdefault("users", [])
st.session_state.setdefault("logs", [])
if st.session_state.get("critical_error"):
    st.error("Application Error: " + st.session_state.get("critical_error", ""))
    if st.button("Reset Application", key="reset_app_critical"):
        st.session_state.clear()
        st.rerun()
    return
initialize_theme(st.session_state["theme"])
st.markdown(
    f"""
    <style>
    .stButton>button {{
        border-radius: 6px;
        background-color: {ACCENT_COLOR};
        color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)
render_top_bar()
page_paths: dict[str, str] = {}
missing_pages: list[str] = []
for label, slug in PAGES.items():
    candidate_files = [
        PAGES_DIR / f"{slug}.py",
        ROOT_DIR / "pages" / f"{slug}.py",
    ]
    if any(path.exists() for path in candidate_files):
        page_paths[label] = f"/pages/{slug}.py"
    else:
        missing_pages.append(label)
if missing_pages:
    st.warning("Missing pages: " + ", ".join(missing_pages))
query = st.query_params
param = query.get("page")
forced_page = param[0] if isinstance(param, list) else param
if forced_page:
    forced_slug = normalize_choice(forced_page)
    forced_page = next(
        (label for label, slug in PAGES.items() if normalize_choice(slug) == forced_slug),
        None,
    )
if st.session_state.get("sidebar_nav") not in PAGES.values():
    st.session_state["sidebar_nav"] = "validation"
if forced_page not in PAGES:
    forced_page = None
choice_label = forced_page or render_modern_sidebar(
    page_paths,
    icons=NAV_ICONS,
    session_key="active_page",
)
if not choice_label:
    choice_label = "Validation"
try:
    st.query_params["page"] = choice_label
except Exception:
    pass
st.session_state.setdefault("_main_tabs", choice_label)
left_col, center_col, _ = st.columns([1, 3, 1])
with left_col:
    render_status_icon()
    with st.expander("Environment Details"):
        secrets = get_st_secrets()
        info_text = (
            f"DB: {secrets.get('DATABASE_URL', 'not set')} | "
            f"ENV: {os.getenv('ENV', 'dev')} | "
            f"Session: {st.session_state.get('session_start_ts', '')} UTC"
        )
        st.info(info_text)
    with st.expander("Application Settings"):
        demo_mode = st.radio("Mode", ["Normal", "Demo"], horizontal=True)
        theme_selector("Theme")
    with st.expander("Data Management"):
        uploaded_file = st.file_uploader("Upload JSON", type="json")
        if st.button("Run Analysis"):
            st.success("Analysis complete!")
    with st.expander("Agent Configuration"):
        api_info = render_api_key_ui(key_prefix="devtools")
        backend_choice = api_info.get("model", "dummy")
        api_key = api_info.get("api_key") or ""
        run_agent_disabled = api_info.get("disabled", False)
        if run_agent_disabled:
            st.warning("API key required for selected model.")
        if AGENT_REGISTRY:
            agent_choice = st.selectbox(
                "Agent",
                sorted(AGENT_REGISTRY.keys()),
                key="devtools_agent_select",
            )
        else:
            agent_choice = None
            st.info("No agents registered")
        event_type = st.text_input("Event", value="LLM_INCOMING")
        payload_txt = st.text_area("Payload JSON", value="{}", height=100)
        run_agent_clicked = st.button("Run Agent", disabled=run_agent_disabled)
    with st.expander("Simulation Tools"):
        render_simulation_stubs()
    st.divider()
    governance_view = st.toggle(
        "Governance View",
        value=st.session_state.get("governance_view", False),
    )
    st.session_state["governance_view"] = governance_view
    render_developer_tools()
with center_col:
    tab_labels = ["Validation", "Voting", "Agents"]
    for label, tab in zip(tab_labels, st.tabs(tab_labels)):
        with tab:
            canonical = normalize_choice(label)
            page_key = PAGES.get(canonical, canonical.lower())
            if page_key:
                module_paths = [
                    f"transcendental_resonance_frontend.tr_pages.{page_key}",
                    f"pages.{page_key}",
                ]
                try:
                    load_page_with_fallback(label, module_paths)
                except Exception:
                    st.toast(f"Page not found: {label}", icon="⚠️")
                    _render_fallback(label)
            else:
                st.toast("Select a page above to continue.")
                _render_fallback(label)
    if run_agent_clicked and "AGENT_REGISTRY" in globals():
        try:
            payload = json.loads(payload_txt or "{}")
        except Exception as exc:
            alert(f"Invalid payload: {exc}", "error")
        else:
            try:
                backend_fn = get_backend(
                    backend_choice.lower(), api_key or None
                )
                if backend_fn is None:
                    raise KeyError("backend")
                agent_cls = AGENT_REGISTRY.get(agent_choice, {}).get("class")
                if agent_cls is None:
                    raise KeyError("agent")
                if agent_choice == "CI_PRProtectorAgent":
                    talker = backend_fn or (lambda p: p)
                    selected_agent = agent_cls(talker, llm_backend=backend_fn)
                elif agent_choice == "MetaValidatorAgent":
                    selected_agent = agent_cls({}, llm_backend=backend_fn)
                elif agent_choice == "GuardianInterceptorAgent":
                    selected_agent = agent_cls(llm_backend=backend_fn)
                else:
                    selected_agent = agent_cls(llm_backend=backend_fn)
                st.session_state["agent_instance"] = selected_agent
                result = selected_agent.process_event(
                    {"event": event_type, "payload": payload}
                )
                st.session_state["agent_output"] = result
                st.success("Agent executed")
            except KeyError as missing:
                if str(missing) == "'backend'":
                    st.warning("No backend available")
                else:
                    st.warning("No agents available")
                st.session_state["agent_output"] = None
                _render_fallback("Agents")
            except Exception as exc:
                st.session_state["agent_output"] = {"error": str(exc)}
                alert(f"Agent error: {exc}", "error")
    if st.session_state.get("agent_output") is not None:
        header("Agent Output")
        if st.session_state.get("beta_mode"):
            st.json(st.session_state.get("agent_output"))
    stats = {
        "runs": st.session_state.get("run_count", 0),
        "proposals": st.session_state.get("proposal_count", "N/A"),
        "success_rate": st.session_state.get("success_rate", "N/A"),
        "accuracy": st.session_state.get("accuracy", "N/A"),
    }
    render_stats_section(stats)
except Exception as exc:
logger.critical("Unhandled error in main: %s", exc, exc_info=True)
st.error("Critical Application Error")
st.code(traceback.format_exc())
if st.button("Reset Application"):
    st.session_state.clear()
    st.rerun()

def ensure_database_exists() -> bool:
try:
secrets = get_st_secrets()
db_url = secrets.get("DATABASE_URL", "sqlite:///harmonizers.db")
db_models.init_db(db_url)
db_models.seed_default_users()
return True
except Exception as exc:
logger.error("Database initialization failed: %s", exc)
return False

def safe_get_user():
try:
if not ensure_database_exists():
    return None
with SessionLocal() as db:
    return db.query(Harmonizer).first()
except Exception as exc:
logger.warning("Failed to fetch user: %s", exc)
users = st.session_state.get("users")
if users:
return users[0]
return None

if __name__ == "__main__":
main()
