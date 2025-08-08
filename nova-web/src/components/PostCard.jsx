"use client";

import { useState } from "react";

export default function PostCard({ post }) {
  const [likes, setLikes] = useState(post.likes || 0);
  const [reacts, setReacts] = useState(post.reacts || 0);
  const [reposts, setReposts] = useState(post.reposts || 0);

  return (
    <article className="card p-4 mb-4">
      <div className="flex items-center gap-3 mb-2">
        <img src={post.avatar} alt="" className="w-10 h-10 rounded-lg" />
        <div>
          <div className="font-semibold">{post.author}</div>
          <div className="text-sm text-[var(--muted)]">{post.title}</div>
        </div>
        {post.promoted && <span className="badge ml-auto">Promoted</span>}
      </div>

      <div className="mb-3">{post.text}</div>
      {post.image && (
        <img src={post.image} alt="" className="rounded-xl border border-[var(--stroke)] mb-3" />
      )}

      <div className="flex flex-wrap gap-2">
        <button className="btn" onClick={() => setLikes(l => l + 1)}>👍 Like {likes ? `· ${likes}` : ""}</button>
        <button className="btn">💬 Comment</button>
        <button className="btn" onClick={() => setReposts(r => r + 1)}>🔁 Repost {reposts ? `· ${reposts}` : ""}</button>
        <button className="btn" onClick={() => setReacts(r => r + 1)}>🎉 React {reacts ? `· ${reacts}` : ""}</button>
        <button className="btn">🎛️ Remix</button>
        <button className="btn">💝 Tip</button>
        <button className="btn">🏆 Reward</button>
        <button className="btn">🧭 Share</button>
      </div>
    </article>
  );
}
