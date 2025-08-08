# pages/feed.py

import streamlit as st
import numpy as np
from faker import Faker
import time
import random

from services.coin_adapter import get_balance as coin_get_balance, tip as coin_tip, reward as coin_reward
from services.coin_config import DEFAULT_REWARD_SPLIT
from services.reactor_adapter import record_reaction, get_reactions
from services.remix_adapter import create_remix

fake = Faker()

@st.cache_data
def generate_post_data(num_posts=30):
    """Generates a large batch of post data."""
    posts = []
    for i in range(num_posts):
        name = fake.name()
        seed = name.replace(" ", "") + str(random.randint(0, 99999))
        posts.append({
            "id": f"post_{i}_{int(time.time())}",
            "author_name": name,
            "author_title": f"{fake.job()} at {fake.company()} • {random.choice(['1st', '2nd', '3rd'])}",
            "author_avatar": f"https://api.dicebear.com/7.x/thumbs/svg?seed={seed}",
            "post_text": fake.paragraph(nb_sentences=random.randint(1, 4)),
            "image_url": random.choice([None, f"https://picsum.photos/800/400?random={np.random.randint(1, 1000)}"]),
            "edited": random.choice([True, False]),
            "promoted": random.choice([True, False]),
            "likes": np.random.randint(10, 500),
            "comments": np.random.randint(0, 100),
            "reposts": np.random.randint(0, 50),
        })
    return posts

def render_post(post):
    """Renders a single post card."""
    st.markdown('<div class="content-card">', unsafe_allow_html=True)

    col1, col2 = st.columns([0.15, 0.85])
    with col1:
        if post["author_avatar"]:
            st.image(post["author_avatar"], width=48)
    with col2:
        st.subheader(post["author_name"])
        st.caption(post["author_title"])

    if post["promoted"]:
        st.caption("Promoted")

    st.write(post["post_text"])

    if post["image_url"]:
        st.image(post["image_url"], use_container_width=True)

    edited_text = " • Edited" if post["edited"] else ""
    st.caption(f"{post['likes']} likes • {post['comments']} comments • {post['reposts']} reposts{edited_text}")

    like_col, comment_col, repost_col, send_col = st.columns(4)
    with like_col:
        st.button("👍 Like", key=f"like_{post['id']}", use_container_width=True)
    with comment_col:
        st.button("💬 Comment", key=f"comment_{post['id']}", use_container_width=True)
    with repost_col:
        st.button("🔁 Repost", key=f"repost_{post['id']}", use_container_width=True)
    with send_col:
        st.button("➡️ Send", key=f"send_{post['id']}", use_container_width=True)

    # --- new actions ---------------------------------------------------------
    react_col, remix_col, tip_col, reward_col = st.columns(4)
    user = st.session_state.get("username", "anon")
    try:
        post_id_int = int(str(post["id"]).split("_")[1])
    except Exception:
        post_id_int = abs(hash(post["id"])) % (10**6)

    with react_col:
        if st.button("👍 React", key=f"react_{post_id_int}_btn_v2", use_container_width=True):
            res = record_reaction(post_id_int, user, "up")
            if not res.get("available", True):
                st.warning("Reaction service unavailable", icon="⚠️")
        counts = get_reactions(post_id_int)
        st.caption(f"👍 {counts.get('counts', {}).get('up', 0)}")

    with remix_col:
        note = st.text_input(
            "note",
            key=f"remix_{post_id_int}_note_v2",
            label_visibility="collapsed",
        )
        if st.button("🎛️ Remix", key=f"remix_{post_id_int}_btn_v2", use_container_width=True):
            res = create_remix(post_id_int, user, note)
            if res.get("ok"):
                st.success(f"Remix {res.get('new_post_id')} created")
            else:
                st.error("Remix failed")

    with tip_col:
        amt = st.number_input(
            "amt",
            min_value=0.0,
            key=f"tip_{post_id_int}_amount_v2",
            label_visibility="collapsed",
        )
        memo = st.text_input(
            "memo",
            key=f"tip_{post_id_int}_memo_v2",
            label_visibility="collapsed",
        )
        if st.button("💰 Tip", key=f"tip_{post_id_int}_btn_v2", use_container_width=True):
            res = coin_tip(user, post.get("author_name", ""), amt, memo or None)
            if res.get("ok"):
                bal = coin_get_balance(user)
                st.success(f"Balance: {bal.get('balance', 0):.2f}")
            else:
                st.error("Tip failed")

    with reward_col:
        can_reward = user == post.get("author_name") or st.session_state.get("is_admin")
        disabled = not can_reward
        if st.button(
            "🏆 Reward",
            key=f"reward_{post_id_int}_btn_v2",
            use_container_width=True,
            disabled=disabled,
        ):
            res = coin_reward(post_id_int, DEFAULT_REWARD_SPLIT)
            if res.get("ok"):
                st.success("Rewarded")
            else:
                st.error("Reward failed")

    st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.markdown("### Your Feed ↩️")
    st.info("Prototype feed. All content below is AI-generated placeholder data for layout testing.")

    # Init session vars
    if "feed_posts" not in st.session_state:
        st.session_state.feed_posts = generate_post_data()
    if "feed_page" not in st.session_state:
        st.session_state.feed_page = 1

    page_size = 5
    max_page = (len(st.session_state.feed_posts) + page_size - 1) // page_size
    start = 0
    end = page_size * st.session_state.feed_page

    for post in st.session_state.feed_posts[start:end]:
        render_post(post)

    if st.session_state.feed_page < max_page:
        if st.button("🔄 Load more"):
            st.session_state.feed_page += 1
    else:
        st.success("You've reached the end of the demo feed.")

if __name__ == "__main__":
    main()
