# pages/feed.py — sleeker feed with popover reactions & share menu (symbolic-safe)

from __future__ import annotations
import time, random
import numpy as np
import streamlit as st
from faker import Faker

from services.coin_adapter import (
    get_balance as coin_get_balance,
    tip as coin_tip,
    reward as coin_reward,
)
from services.coin_config import DEFAULT_REWARD_SPLIT
from services.reactor_adapter import record_reaction, get_reactions
from services.remix_adapter import create_remix

# at top of file if not present
import inspect

fake = Faker()

# ─────────────────────────── CSS: cleaner cards/buttons ───────────────────────────
_STYLES = """
<style>
:root{
  --bg:#0b0b0e; --card:#111218; --muted:#9aa0a6; --text:#e9ecf1;
  --accent:#7aa2ff; --ring:rgba(122,162,255,.33);
}
html, body, .stApp { background: var(--bg); }
section.main > div { padding-top: .25rem; }

h1,h2,h3,h4,p,span,div { color: var(--text) !important; }
.small-muted{ color: var(--muted); font-size:.85rem }

.content-card{
  border-radius:18px;
  border:1px solid rgba(122,162,255,.08);
  background: linear-gradient(180deg, rgba(255,255,255,.02), rgba(255,255,255,0));
  box-shadow: 0 10px 30px rgba(0,0,0,.32), inset 0 1px 0 rgba(255,255,255,.05);
  padding:18px 18px 12px 18px; margin:18px 0;
  transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}
.content-card:hover{
  transform: translateY(-2px);
  border-color: var(--ring);
  box-shadow: 0 16px 40px rgba(0,0,0,.44);
}

.meta-row{ color:var(--muted); font-size:.88rem; margin-top:8px; }

.btn{ width:100%; padding:.55rem .8rem; border-radius:12px;
  border:1px solid #232634; background:#141622; color:#dfe3ea; font-weight:600;
  display:flex; align-items:center; justify-content:center; gap:.55rem; }
.btn:hover{ border-color:#334155; background:#151a2a; }

.badge{ display:inline-flex; align-items:center; gap:.35rem; padding:.25rem .6rem;
  border-radius:999px; border:1px solid #273046; color:#cbd5e1; font-size:.78rem;
  background:#0f1320; }

.number-pill > div { border-radius:999px !important; }
.note-input > div > div > input { border-radius:12px !important; }
</style>
"""

EMOJI_SET = ["👍", "❤️", "😅", "🤗", "👀", "🔥"]

def _ensure_css_once():
    if not st.session_state.get("_feed_css"):
        st.markdown(_STYLES, unsafe_allow_html=True)
        st.session_state["_feed_css"] = True

# ─────────────────────────── demo data ───────────────────────────
@st.cache_data
def generate_post_data(num_posts=18):
    posts = []
    now = int(time.time())
    for i in range(num_posts):
        name = fake.name()
        seed = name.replace(" ", "") + str(random.randint(0, 99999))
        posts.append({
            "id": f"post_{i}_{now}",
            "author_name": name,
            "author_title": f"{fake.job()} at {fake.company()} • {random.choice(['1st','2nd','3rd'])}",
            "author_avatar": f"https://api.dicebear.com/7.x/thumbs/svg?seed={seed}",
            "post_text": fake.paragraph(nb_sentences=random.randint(1, 4)),
            "image_url": random.choice([None, f"https://picsum.photos/1200/620?random={np.random.randint(1, 9999)}"]),
            "edited": random.choice([True, False]),
            "promoted": random.choice([True, False]),
            "likes": np.random.randint(10, 500),
            "comments": np.random.randint(0, 100),
            "reposts": np.random.randint(0, 50),
        })
    return posts

# ─────────────────────────── helpers ───────────────────────────
def _counts_for(post_id_int):
    try:
        data = get_reactions(post_id_int) or {}
        counts = data.get("counts", data) or {}
        alias = {"up":"👍","heart":"❤️","laugh":"😅","hug":"🤗","eyes":"👀","fire":"🔥"}
        fixed = {}
        for k,v in counts.items(): fixed[ alias.get(k,k) ] = v
        return {e:int(fixed.get(e,0)) for e in EMOJI_SET}
    except Exception:
        return {e:0 for e in EMOJI_SET}

def _react(post_id_int, user, emoji):
    token_map = {"👍":"up","❤️":"heart","😅":"laugh","🤗":"hug","👀":"eyes","🔥":"fire"}
    try:
        record_reaction(post_id_int, user, token_map.get(emoji, emoji))
    except Exception:
        pass

def _popover(label: str, key: str):
    """Open a popover in both newer and older Streamlit builds."""
    pop = st.popover
    try:
        # Prefer passing key if this build supports it
        if "key" in inspect.signature(pop).parameters:
            return pop(label, key=key, use_container_width=True)
        # Fallback: older builds don't accept key
        return pop(label, use_container_width=True)
    except TypeError:
        # Very old signature without use_container_width
        return pop(label)


def _symbolic_spend(user, amount, memo):
    try:
        if amount and float(amount) > 0:
            coin_tip(user, "treasury", float(amount), memo or None)  # symbolic only
            return coin_get_balance(user).get("balance", 0.0)
    except Exception:
        return None

# ─────────────────────────── UI: one post ───────────────────────────
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

    # primary row
    r1, r2, r3, r4 = st.columns(4)
    with r1: st.button("👍 Like", key=f"like_{post['id']}", use_container_width=True)
    with r2: st.button("💬 Comment", key=f"comment_{post['id']}", use_container_width=True)

    # Share menu (repost/send/copy)
    with r3:
        with _popover("📤 Share ▾", f"share_pop_{post['id']}"):
            st.button("🔁 Repost", key=f"repost_{post['id']}", use_container_width=True)
            st.button("✉️ Send", key=f"send_{post['id']}", use_container_width=True)
            st.code(f"/vibenodes/{post['id']}", language="text")  # simple copyable link text

    # Reactions popover (LinkedIn-style)
    user = st.session_state.get("username", "anon")
    try:
        post_id_int = int(str(post["id"]).split("_")[1])
    except Exception:
        post_id_int = abs(hash(post["id"])) % (10**6)

    with r4:
        counts = _counts_for(post_id_int)
        with _popover("✨ React ▾", f"rx_pop_{post['id']}"):
            cols = st.columns(len(EMOJI_SET))
            for i, emoji in enumerate(EMOJI_SET):
                with cols[i]:
                    if st.button(f"{emoji} {counts.get(emoji,0)}", key=f"rx_{emoji}_{post_id_int}", use_container_width=True):
                        _react(post_id_int, user, emoji)
                        st.rerun()

    # secondary row: spend/note + tip + reward + remix
    b1, b2, b3, b4 = st.columns([1.3, 1.0, 0.9, 0.9])

    with b1:
        spend = st.number_input("Spend (root-coin)", min_value=0.0, step=0.25,
                                key=f"spend_{post_id_int}", label_visibility="collapsed",
                                help="Symbolic only; conserved inside this sandbox.")
        note = st.text_input("Add a remix note", key=f"note_{post_id_int}", label_visibility="collapsed",
                             placeholder="What are you adding / refining?")
        if st.button("🎛️ Remix", key=f"remix_{post_id_int}", use_container_width=True):
            ok = False
            try:
                res = create_remix(post_id_int, user, note, spend=spend)
                ok = bool(res.get("ok"))
            except TypeError:
                res = create_remix(post_id_int, user, note)
                ok = bool(res.get("ok"))
            new_bal = _symbolic_spend(user, spend, f"remix spend on {post_id_int}")
            if ok:
                st.success("Remixed ✔️")
                if new_bal is not None:
                    st.caption(f"Balance: {float(new_bal):.2f}")
            else:
                st.error("Remix failed")

    with b2:
        amt = st.number_input("Tip amount", min_value=0.0, step=0.25,
                              key=f"tip_amt_{post_id_int}", label_visibility="collapsed")
        memo = st.text_input("Tip memo", key=f"tip_memo_{post_id_int}", label_visibility="collapsed", placeholder="Say thanks…")
        if st.button("💝 Tip", key=f"tip_btn_{post_id_int}", use_container_width=True):
            try:
                res = coin_tip(user, post.get("author_name",""), amt, memo or None)
                if res.get("ok"):
                    bal = coin_get_balance(user).get("balance", 0.0)
                    st.caption(f"Balance: {float(bal):.2f}")
                    st.success("Tip sent")
                else:
                    st.warning("Tip failed")
            except Exception:
                st.warning("Tip service unavailable")

    with b3:
        can_reward = user == post.get("author_name") or st.session_state.get("is_admin")
        if st.button("🏆 Reward", key=f"reward_{post_id_int}", use_container_width=True, disabled=not can_reward):
            try:
                res = coin_reward(post_id_int, DEFAULT_REWARD_SPLIT)
                st.success("Rewarded") if res.get("ok") else st.error("Reward failed")
            except Exception:
                st.warning("Reward service unavailable")

    with b4:
        st.button("🧭 Share", key=f"share_inline_{post_id_int}", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────── page ───────────────────────────
def main():
    _ensure_css_once()
    st.markdown("### superNova_2177 <span class='badge'>Prototype feed (symbolic only)</span>", unsafe_allow_html=True)
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
