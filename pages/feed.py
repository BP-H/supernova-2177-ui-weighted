# pages/feed.py — modern feed w/ emoji reactions, share popover & symbolic remix spend
import time
import random
import numpy as np
import streamlit as st
from faker import Faker

# Symbolic “coin” and engagement services — safe, optional
from services.coin_adapter import (
    get_balance as coin_get_balance,
    tip as coin_tip,
    reward as coin_reward,
)
from services.coin_config import DEFAULT_REWARD_SPLIT
from services.reactor_adapter import record_reaction, get_reactions
from services.remix_adapter import create_remix



from pathlib import Path

def _inject_css_file(path="assets/supernova.css"):
    p = Path(path)
    if p.exists():
        st.markdown(f"<style>{p.read_text()}</style>", unsafe_allow_html=True)

# ...later inside main():
def main():
    _inject_css_file()   # <— add this line first
    # (rest of your code)



fake = Faker()

# ──────────────────────────────────────────────────────────────────────────────
# Styles
# ──────────────────────────────────────────────────────────────────────────────
_STYLES = """
<style>
:root{
  --bg:#0b0b0e; --card:#111218; --muted:#9aa0a6; --text:#e9ecf1;
  --accent:#7aa2ff; --accent-2:#67e8f9; --ring:rgba(122,162,255,.35);
  --stroke:#212638;
}
html, body, .stApp { background: var(--bg); }
section.main > div { padding-top: .25rem; }

h3, h2, h1, .stMarkdown p, .stCaption, .stText, .st-emotion-cache-10trblm{
  color: var(--text) !important;
}
.small-muted{ color: var(--muted); font-size:.85rem }

.feed-title{
  font-size:1.6rem; font-weight:800; letter-spacing:.3px;
  display:flex; align-items:center; gap:.6rem;
}
.badge{
  display:inline-flex; align-items:center; gap:.35rem;
  background:linear-gradient(180deg,#1a1b22, #13141a);
  color:var(--muted); border:1px solid #1f2330; border-radius:999px;
  padding:.25rem .6rem; font-size:.8rem;
}

.content-card{
  border-radius:18px;
  border:1px solid rgba(122,162,255,.08);
  background: radial-gradient(80% 120% at 0% 0%, rgba(103,232,249,.06), transparent 40%),
              linear-gradient(180deg, rgba(255,255,255,.02), rgba(255,255,255,0));
  box-shadow: 0 10px 30px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.05);
  padding:18px 18px 14px 18px; margin:18px 0;
  transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}
.content-card:hover{
  transform: translateY(-2px);
  border-color: var(--ring);
  box-shadow: 0 16px 40px rgba(0,0,0,.38), 0 0 0 3px rgba(122,162,255,.08) inset;
}
.meta-row{ color:var(--muted); font-size:.88rem; margin-top:8px; }

.row{ display:flex; gap:10px; }
.row > div{ flex:1; }
.btn{
  width:100%; padding:.55rem .8rem; border-radius:12px; border:1px solid #232634;
  background:#141622; color:#dfe3ea; font-weight:600; letter-spacing:.2px;
  display:flex; align-items:center; justify-content:center; gap:.55rem; cursor:pointer;
}
.btn:hover{ border-color:#334155; background:#151a2a; }
.btn.ghost{ background:#10121a; color:#cbd5e1; }
.btn.ghost:hover{ background:#121624; }

.emoji-bar{
  display:flex; gap:.5rem; align-items:center; flex-wrap:wrap; margin:.25rem 0 .1rem 0;
}
.emoji{
  display:flex; align-items:center; gap:.45rem;
  padding:.45rem .65rem; border:1px solid #212432; background:#0f111a; color:#e5e7eb;
  border-radius:999px; cursor:pointer; font-size:1rem; line-height:1;
}
.emoji:hover{ border-color:#334155; background:#141724; }
.emoji .count{ color:#9aa0a6; font-size:.82rem; }
.note-input > div > div > input { border-radius:12px !important; }
.slim-input > div > div > input { border-radius:12px !important; }
.number-pill > div { border-radius:999px !important; }
.balance-pill{
  display:inline-flex; align-items:center; gap:.45rem;
  background:#0f1320; border:1px solid #273046; border-radius:999px;
  padding:.3rem .7rem; color:#c7d2fe; font-size:.82rem;
}
.share-pop{
  padding:.25rem; background:#0f111a; border:1px solid #212638; border-radius:12px;
}
</style>
"""

EMOJI_SET = ["👍", "❤️", "😅", "🤗", "👀", "🔥"]  # tasteful set: like, hearts, shy-laugh, hug, eyes, fire

def _ensure_css_once():
    if not st.session_state.get("_feed_css"):
        st.markdown(_STYLES, unsafe_allow_html=True)
        st.session_state["_feed_css"] = True

# ──────────────────────────────────────────────────────────────────────────────
# Demo data
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_data
def generate_post_data(num_posts=30):
    """Generates a batch of placeholder posts for layout/testing."""
    posts = []
    for i in range(num_posts):
        name = fake.name()
        seed = name.replace(" ", "") + str(random.randint(0, 99999))
        posts.append({
            "id": f"post_{i}_{int(time.time())}",
            "author_name": name,
            "author_title": f"{fake.job()} at {fake.company()} • {random.choice(['1st','2nd','3rd'])}",
            "author_avatar": f"https://api.dicebear.com/7.x/thumbs/svg?seed={seed}",
            "post_text": fake.paragraph(nb_sentences=random.randint(1, 4)),
            "image_url": random.choice([None, f"https://picsum.photos/1024/512?random={np.random.randint(1, 9999)}"]),
            "edited": random.choice([True, False]),
            "promoted": random.choice([True, False]),
            "likes": np.random.randint(10, 500),
            "comments": np.random.randint(0, 100),
            "reposts": np.random.randint(0, 50),
        })
    return posts

# ──────────────────────────────────────────────────────────────────────────────
# Helpers (resilient to missing/temporary backends)
# ──────────────────────────────────────────────────────────────────────────────
def _counts_for(post_id_int):
    """Try the backend; fall back gracefully."""
    try:
        data = get_reactions(post_id_int) or {}
        counts = data.get("counts", data) or {}
        alias = {"up":"👍", "heart":"❤️", "laugh":"😅", "hug":"🤗", "eyes":"👀", "fire":"🔥"}
        fixed = {}
        for k,v in counts.items():
            fixed[ alias.get(k, k) ] = v
        return {e: int(fixed.get(e, 0)) for e in EMOJI_SET}
    except Exception:
        return {e: 0 for e in EMOJI_SET}

def _react(post_id_int, user, emoji):
    token_map = {"👍":"up","❤️":"heart","😅":"laugh","🤗":"hug","👀":"eyes","🔥":"fire"}
    try:
        record_reaction(post_id_int, user, token_map.get(emoji, emoji))
    except Exception:
        pass

def _symbolic_spend(user, amount, memo):
    """Symbolic root-coin move (non-financial)."""
    try:
        if amount and float(amount) > 0:
            # Send to neutral 'treasury' bucket if adapter expects a receiver.
            coin_tip(user, "treasury", float(amount), memo or None)
            return float(coin_get_balance(user).get("balance", 0.0))
    except Exception:
        return None

# ──────────────────────────────────────────────────────────────────────────────
# UI: a single post
# ──────────────────────────────────────────────────────────────────────────────
def _share_ui(post_id: int, author: str):
    """Small ‘Share’ panel: Repost / Send / Copy link (mock)."""
    popover = getattr(st, "popover", None)
    if popover:
        with popover("📤 Share", use_container_width=True):
            st.markdown('<div class="share-pop">', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                st.button("🔁 Repost", key=f"repost_{post_id}", use_container_width=True, type="secondary")
            with c2:
                st.button("✉️ Send", key=f"send_{post_id}", use_container_width=True, type="secondary")
            with c3:
                st.button("🔗 Copy link", key=f"copy_{post_id}", use_container_width=True, type="secondary", help="Mock")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        with st.expander("📤 Share"):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.button("🔁 Repost", key=f"repost_{post_id}", use_container_width=True, type="secondary")
            with c2:
                st.button("✉️ Send", key=f"send_{post_id}", use_container_width=True, type="secondary")
            with c3:
                st.button("🔗 Copy link", key=f"copy_{post_id}", use_container_width=True, type="secondary", help="Mock")

def _reaction_picker(post_id_int, user):
    """LinkedIn-style reaction panel via popover (fallback to expander)."""
    popover = getattr(st, "popover", None)
    counts = _counts_for(post_id_int)

    if popover:
        with popover("👍 React", use_container_width=True):
            cols = st.columns(len(EMOJI_SET))
            for i, emoji in enumerate(EMOJI_SET):
                with cols[i]:
                    if st.button(f"{emoji} {counts.get(emoji,0)}", key=f"rx_{emoji}_{post_id_int}", use_container_width=True):
                        _react(post_id_int, user, emoji)
                        st.rerun()
    else:
        with st.expander("👍 React"):
            cols = st.columns(len(EMOJI_SET))
            for i, emoji in enumerate(EMOJI_SET):
                with cols[i]:
                    if st.button(f"{emoji} {counts.get(emoji,0)}", key=f"rx_{emoji}_{post_id_int}", use_container_width=True):
                        _react(post_id_int, user, emoji)
                        st.rerun()

def render_post(post):
    st.markdown('<div class="content-card">', unsafe_allow_html=True)

    # header
    a1, a2 = st.columns([0.12, 0.88])
    with a1:
        if post["author_avatar"]:
            st.image(post["author_avatar"], width=50)
    with a2:
        st.markdown(f"**{post['author_name']}**")
        st.markdown(f'<span class="small-muted">{post["author_title"]}</span>', unsafe_allow_html=True)
        if post["promoted"]:
            st.markdown('<span class="badge">Promoted</span>', unsafe_allow_html=True)

    # body
    st.write(post["post_text"])
    if post["image_url"]:
        st.image(post["image_url"], use_container_width=True)

    edited = " • Edited" if post["edited"] else ""
    st.markdown(
        f'<div class="meta-row">{post["likes"]} likes • {post["comments"]} comments • {post["reposts"]} reposts{edited}</div>',
        unsafe_allow_html=True,
    )

    # primary actions
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.button("👍 Like", key=f"like_{post['id']}", use_container_width=True, type="secondary")
    with c2: st.button("💬 Comment", key=f"comment_{post['id']}", use_container_width=True, type="secondary")
    with c3: _share_ui(post_id=int(post['id'].split("_")[1]), author=post['author_name'])
    with c4: _reaction_picker(post_id_int=int(post['id'].split("_")[1]), user=st.session_state.get("username","anon"))

    # remix + symbolic spend + tip + reward
    user = st.session_state.get("username", "anon")
    try:
        post_id_int = int(str(post["id"]).split("_")[1])
    except Exception:
        post_id_int = abs(hash(post["id"])) % (10**6)

    r1, r2, r3, r4 = st.columns([1.3, 1.0, 0.9, 0.9])

    with r1:
        spend = st.number_input("Spend (root-coin)", min_value=0.0, step=0.25,
                                key=f"spend_{post_id_int}", label_visibility="collapsed",
                                help="Symbolic value only; conserved within this sandbox.")
        note = st.text_input("Add a remix note", key=f"note_{post_id_int}", label_visibility="collapsed",
                             placeholder="What are you adding / refining?")
        if st.button("🎛️ Remix", key=f"remix_{post_id_int}", use_container_width=True):
            ok = False
            try:
                res = create_remix(post_id_int, user, note, spend=spend)  # if adapter supports it
                ok = bool(res.get("ok"))
            except TypeError:
                res = create_remix(post_id_int, user, note)
                ok = bool(res.get("ok"))

            new_bal = _symbolic_spend(user, spend, f"remix spend on {post_id_int}")
            if ok:
                st.success(f"Remixed ✔️ (post #{post_id_int})")
                if new_bal is not None:
                    st.markdown(f'<span class="balance-pill">Balance: {float(new_bal):.2f}</span>', unsafe_allow_html=True)
            else:
                st.error("Remix failed")

    with r2:
        amt = st.number_input("Tip amount", min_value=0.0, step=0.25,
                              key=f"tip_amt_{post_id_int}", label_visibility="collapsed")
        memo = st.text_input("Tip memo", key=f"tip_memo_{post_id_int}", label_visibility="collapsed", placeholder="Say thanks…")
        if st.button("💝 Tip", key=f"tip_btn_{post_id_int}", use_container_width=True):
            try:
                res = coin_tip(user, post.get("author_name",""), amt, memo or None)
                if res.get("ok"):
                    bal = coin_get_balance(user).get("balance", 0.0)
                    st.markdown(f'<span class="balance-pill">Balance: {float(bal):.2f}</span>', unsafe_allow_html=True)
                    st.success("Tip sent")
                else:
                    st.warning("Tip failed")
            except Exception:
                st.warning("Tip service unavailable")

    with r3:
        can_reward = user == post.get("author_name") or st.session_state.get("is_admin")
        if st.button("🏆 Reward", key=f"reward_{post_id_int}", use_container_width=True, disabled=not can_reward):
            try:
                res = coin_reward(post_id_int, DEFAULT_REWARD_SPLIT)
                st.success("Rewarded") if res.get("ok") else st.error("Reward failed")
            except Exception:
                st.warning("Reward service unavailable")

    with r4:
        st.button("🧭 Share", key=f"share_footer_{post_id_int}", use_container_width=True, help="Same actions as above")

    st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# Page
# ──────────────────────────────────────────────────────────────────────────────
def main():
    _ensure_css_once()

    st.markdown('<div class="feed-title">superNova_2177 <span class="badge">Prototype feed (symbolic only)</span></div>', unsafe_allow_html=True)
    st.caption("All metrics here are symbolic reputation/engagement — not financial.")

    if "feed_posts" not in st.session_state:
        st.session_state.feed_posts = generate_post_data()
    if "feed_page" not in st.session_state:
        st.session_state.feed_page = 1

    page_size = 5
    end = page_size * st.session_state.feed_page

    for post in st.session_state.feed_posts[:end]:
        render_post(post)

    total = len(st.session_state.feed_posts)
    if end < total:
        if st.button("🔄 Load more"):
            st.session_state.feed_page += 1
            st.rerun()
    else:
        st.success("You’ve reached the end of the demo feed.")

if __name__ == "__main__":
    main()
