'use client';

import Image from 'next/image';
import { useState } from 'react';
import ReactionBar from './ReactionBar';

export default function PostCard({ post }) {
  const [shareOpen, setShareOpen] = useState(false);
  const { author, title, avatar, text, image, stats } = post;

  return (
    <article className="glass p-5">
      {/* header */}
      <div className="flex gap-4">
        <Image src={avatar} alt={author} width={48} height={48} className="rounded-full" />
        <div>
          <div className="font-semibold text-white">{author}</div>
          <div className="text-sm text-slate-400">{title}</div>
        </div>
      </div>

      {/* body */}
      <p className="mt-4 text-slate-200">{text}</p>
      {image && (
        <div className="mt-4 overflow-hidden rounded-xl border border-white/10">
          <Image src={image} alt="" width={1600} height={900} className="h-auto w-full" />
        </div>
      )}

      {/* meta */}
      <div className="mt-3 text-sm text-slate-400">
        {stats.likes} likes • {stats.comments} comments • {stats.reposts} reposts
        {stats.edited && ' • Edited'}
      </div>

      {/* actions */}
      <div className="mt-4 grid grid-cols-4 gap-3">
        <button className="btn">👍 Like</button>
        <button className="btn">💬 Comment</button>
        <button className="btn">🔁 Repost</button>
        <button className="btn" onClick={() => setShareOpen(v => !v)}>📤 Share</button>
      </div>

      {/* emoji reactions */}
      <div className="mt-3">
        <ReactionBar />
      </div>

      {/* remix/tip row */}
      <div className="mt-3 grid grid-cols-2 gap-3">
        <button className="btn btn-ghost">🎛️ Remix</button>
        <button className="btn btn-ghost">💝 Tip</button>
      </div>

      {/* share menu */}
      {shareOpen && (
        <div className="mt-3 rounded-xl border border-white/10 bg-white/5 p-3 text-sm text-slate-300">
          Share options: copy link • post to your feed • send to a friend
        </div>
      )}
    </article>
  );
}
