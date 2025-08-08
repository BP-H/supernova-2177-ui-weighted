"use client";

import { useEffect, useState } from "react";
import API from "../lib/api";

const EMOJI_SET = ["👍", "❤️", "😅", "🤗", "👀", "🔥"];

export default function Page() {
  const [posts, setPosts] = useState([]);
  const [counts, setCounts] = useState({}); // { [postId]: { "👍": 0, ... } }
  const user = "guest"; // swap with real user when auth is wired

  useEffect(() => {
    (async () => {
      const feed = await API.feedOrDemo();
      setPosts(feed);
      // prefetch reaction counts
      const all = await Promise.all(
        feed.map((p) => API.getReactions(p.id).catch(() => ({ counts: {} })))
      );
      const byId = {};
      feed.forEach((p, i) => {
        const c = all[i]?.counts || {};
        // normalize to our emoji keys
        byId[p.id] = EMOJI_SET.reduce((acc, e) => {
          acc[e] = c[e] || 0;
          return acc;
        }, {});
      });
      setCounts(byId);
    })();
  }, []);

  const bump = (postId, emoji) => {
    setCounts((prev) => ({
      ...prev,
      [postId]: { ...(prev[postId] || {}), [emoji]: (prev[postId]?.[emoji] || 0) + 1 },
    }));
  };

  async function onLike(postId) {
    await API.like(postId, user).catch(() => {});
    bump(postId, "👍");
  }

  async function onReact(postId, emoji) {
    await API.react(postId, user, emoji).catch(() => {});
    bump(postId, emoji);
  }

  async function onRemix(postId) {
    const note = prompt("Remix note? (optional)") || "";
    const spend = 0;
    const res = await API.remix(postId, user, note, spend);
    if (res?.ok) alert("Remixed!");
  }

  async function onTip(author) {
    const amt = parseFloat(prompt("Tip amount (symbolic):", "0.25") || "0");
    const memo = prompt("Memo?", "Thanks!") || "";
    if (!amt || isNaN(amt)) return;
    const res = await API.tip(user, author, amt, memo);
    alert(res.ok ? "Tipped!" : `Tip failed: ${res.error}`);
  }

  async function onShare(postId) {
    await API.share(postId);
    try {
      await navigator.clipboard.writeText(window.location.href);
      alert("Link copied!");
    } catch {
      alert("Shared!");
    }
  }

  return (
    <main className="mx-auto max-w-3xl p-4">
      <h1 className="text-3xl font-semibold mb-6">superNova_2177</h1>
      {posts.map((p) => (
        <div
          key={p.id}
          className="mb-6 rounded-2xl border border-white/10 bg-[#111218] p-4 shadow-lg"
        >
          <div className="flex items-center gap-3">
            <img
              src={p.author_avatar}
              alt=""
              className="h-10 w-10 rounded-full border border-white/10"
            />
            <div>
              <div className="font-semibold">{p.author_name}</div>
              <div className="text-sm text-white/60">{p.author_title}</div>
            </div>
          </div>

          <p className="mt-3 text-white/90">{p.text}</p>

          {p.image_url ? (
            <img
              src={p.image_url}
              alt=""
              className="mt-3 w-full rounded-xl border border-white/10"
            />
          ) : null}

          <div className="mt-3 flex gap-2">
            <button
              className="rounded-lg border border-white/10 px-3 py-2 text-sm hover:border-white/25"
              onClick={() => onLike(p.id)}
            >
              👍 Like
            </button>
            <button
              className="rounded-lg border border-white/10 px-3 py-2 text-sm hover:border-white/25"
              onClick={() => onRemix(p.id)}
            >
              🎛️ Remix
            </button>
            <button
              className="rounded-lg border border-white/10 px-3 py-2 text-sm hover:border-white/25"
              onClick={() => onTip(p.author_name)}
            >
              💝 Tip
            </button>
            <button
              className="rounded-lg border border-white/10 px-3 py-2 text-sm hover:border-white/25"
              onClick={() => onShare(p.id)}
            >
              📤 Share
            </button>
          </div>

          <div className="mt-3 flex flex-wrap gap-2">
            {EMOJI_SET.map((e) => (
              <button
                key={e}
                className="rounded-full border border-white/10 px-3 py-1 text-sm hover:border-white/25"
                onClick={() => onReact(p.id, e)}
              >
                {e} {counts[p.id]?.[e] ?? 0}
              </button>
            ))}
          </div>
        </div>
      ))}
    </main>
  );
}
