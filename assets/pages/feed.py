/* ===== Supernova 2177 — sleek dark UI for Streamlit buttons/inputs/cards ===== */

:root{
  --bg:#0b0b0e;
  --panel:#0f111a;
  --card:#10131f;
  --ink:#e9ecf1;
  --muted:#9aa0a6;
  --line:#202332;
  --line-2:#2a2f45;
  --accent:#7aa2ff;
  --accent-2:#67e8f9;
  --ring:rgba(122,162,255,.35);
}

html, body, .stApp { background: var(--bg) !important; color: var(--ink) !important; }
section.main > div { padding-top: .5rem !important; }

/* --------- Headings & small text --------- */
h1, h2, h3, h4, h5, h6, p, span, div, label { color: var(--ink) !important; }
.small-muted{ color: var(--muted); font-size:.85rem }

/* --------- Card look for posts --------- */
.content-card{
  border-radius:18px;
  border:1px solid rgba(122,162,255,.08);
  background:
    radial-gradient(80% 120% at 0% 0%, rgba(103,232,249,.06), transparent 40%),
    linear-gradient(180deg, rgba(255,255,255,.02), rgba(255,255,255,0));
  box-shadow: 0 10px 30px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.05);
  padding:18px 18px 12px 18px; margin:18px 0;
  transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}
.content-card:hover{
  transform: translateY(-2px);
  border-color: var(--ring);
  box-shadow: 0 16px 40px rgba(0,0,0,.38), 0 0 0 3px rgba(122,162,255,.08) inset;
}
.meta-row{ color:var(--muted); font-size:.88rem; margin-top:8px; }

/* --------- Buttons (works on Streamlit’s native st.button) --------- */
.content-card .stButton > button,
div[data-testid="column"] .stButton > button{
  width:100%;
  padding:.55rem .9rem;
  border-radius:12px;
  border:1px solid var(--line-2);
  background:linear-gradient(180deg,#111525,#0c0f1e);
  color:#dfe3ea;
  font-weight:600; letter-spacing:.2px;
  display:flex; align-items:center; justify-content:center; gap:.55rem;
  cursor:pointer;
  transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease, background .12s ease;
}
.content-card .stButton > button:hover,
div[data-testid="column"] .stButton > button:hover{
  transform: translateY(-1px);
  border-color:#4e5fff;
  box-shadow: 0 0 0 4px rgba(91,115,255,0.17);
  background:linear-gradient(180deg,#121833,#0c1124);
}
.content-card .stButton > button:active{ transform: translateY(0); }

/* Make “icon + label” look centered and tidy even with emoji */
.content-card .stButton > button p { margin: 0 !important; }

/* --------- Inputs (text & number) --------- */
.content-card [data-testid="stTextInput"] > div,
.content-card [data-testid="stNumberInput"] > div{
  background:#0f1320 !important;
  border:1px solid #26304a !important;
  border-radius:12px !important;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.03);
}
.content-card [data-testid="stTextInput"] input,
.content-card [data-testid="stNumberInput"] input{
  background:transparent !important; color:#e6e8f2 !important;
}
.content-card [data-testid="stNumberInput"] button{
  border:0 !important; background:transparent !important; color:#cbd5e1 !important;
}

/* --------- Cute chips/badges --------- */
.badge{
  display:inline-flex; align-items:center; gap:.35rem;
  background:linear-gradient(180deg,#1a1b22,#13141a);
  color:var(--muted); border:1px solid #1f2330; border-radius:999px;
  padding:.25rem .6rem; font-size:.8rem;
}

/* --------- Balance pill (tip/remix feedback) --------- */
.balance-pill{
  display:inline-flex; align-items:center; gap:.45rem;
  background:#0f1320; border:1px solid #273046; border-radius:999px;
  padding:.3rem .7rem; color:#c7d2fe; font-size:.82rem;
}

/* --------- Sidebar polish (optional but nice) --------- */
[data-testid="stSidebar"]{
  background:#0e0f14 !important; border-right:1px solid var(--line) !important;
}
[data-testid="stSidebar"] .stButton > button{
  background:#11131b !important; border:1px solid #1f2433 !important;
  height:36px !important; border-radius:10px !important; text-align:left !important;
}
[data-testid="stSidebar"] .stButton > button:hover{
  border-color:#3c4cff !important; background:#12162a !important;
}
[data-testid="stSidebar"] img { border-radius:50% !important }

/* --------- Hide default Streamlit chrome for cleaner feel --------- */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
