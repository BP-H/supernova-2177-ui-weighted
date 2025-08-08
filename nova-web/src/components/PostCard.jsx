"use client";
import { useState } from "react";
import { ThumbsUp, MessageCircle, Share2, X } from "lucide-react";
import Image from "next/image";
import { react as reactApi, remixSpend } from "../lib/api";

const EMOJI_SET = [
  { k:"👍", label:"Like" },
  { k:"❤️", label:"Love" },
  { k:"😅", label:"Haha" },
  { k:"🤗", label:"Hug" },
  { k:"👀", label:"Watch" },
  { k:"🔥", label:"Fire" }
];

export default function PostCard({ post }) {
  const [showShare, setShowShare] = useState(false);
  const [showRemix, setShowRemix] = useState(false);
  const [spend, setSpend] = useState(0);
  const [note, setNote] = useState("");

  return (
    <div className="card soft p-4 mb-6">
      {/* Header */}
      <div className="flex gap-3">
        <div className="relative w-12 h-12">
          <Image src={post.author.avatar} alt="" fill className="rounded-full" />
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <div className="font-semibold">{post.author.name}</div>
            {post.promoted && (
              <span className="rounded-full border border-white/10 px-2 py-0.5 text-xs text-white/70">Promoted</span>
            )}
          </div>
          <div className="text-sm text-white/70">{post.author.title}</div>
        </div>
      </div>

      {/* Body */}
      <div className="mt-3 text-[15px] leading-relaxed">{post.text}</div>
      {post.image && (
        <div className="mt-3 overflow-hidden rounded-2xl border border-white/10">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={post.image} alt="" className="w-full h-auto" />
        </div>
      )}
      <div className="mt-3 text-sm text-white/60">
        {post.likes} likes · {post.comments} comments · {post.reposts} reposts
      </div>

      {/* Actions */}
      <div className="mt-3 grid grid-cols-4 gap-2">
        <button className="btn"><ThumbsUp className="w-4 h-4" /> Like</button>
        <button className="btn"><MessageCircle className="w-4 h-4" /> Comment</button>
        <button className="btn" onClick={()=>setShowShare(v=>!v)}><Share2 className="w-4 h-4" /> Share</button>
        <div className="flex items-center justify-center gap-1">
          {EMOJI_SET.map(e => (
            <button
              key={e.k}
              className="px-2 py-1 rounded-full border border-white/10 bg-black/30 text-sm hover:bg-black/50"
              title={e.label}
              onClick={() => reactApi(post.id, e.k)}
            >
              {e.k}
            </button>
          ))}
        </div>
      </div>

      {/* Share popover */}
      {showShare && (
        <div className="relative">
          <div className="absolute z-20 mt-2 w-64 rounded-xl border border-white/10 bg-[var(--card)] p-3 shadow-xl">
            <div className="flex items-center justify-between text-sm mb-2">
              <div className="text-white/80">Share this post</div>
              <button onClick={()=>setShowShare(false)}><X className="w-4 h-4" /></button>
            </div>
            <div className="grid gap-2">
              <button className="btn">Copy link</button>
              <button className="btn">Repost to feed</button>
              <button className="btn">Send via DM</button>
            </div>
          </div>
        </div>
      )}

      {/* Remix drawer (bottom) */}
      <div className="mt-3 grid grid-cols-2 gap-3">
        <button className="btn" onClick={()=>setShowRemix(true)}>🎛️ Remix</button>
        <button className="btn">💝 Tip (symbolic)</button>
      </div>

      {showRemix && (
        <div className="fixed inset-0 z-30">
          <div className="absolute inset-0 bg-black/60" onClick={()=>setShowRemix(false)} />
          <div className="absolute bottom-0 left-0 right-0 rounded-t-2xl border border-white/10 bg-[var(--card)] p-5">
            <div className="flex items-center justify-between mb-3">
              <div className="text-white/80">Symbolic remix spend (root coin)</div>
              <button onClick={()=>setShowRemix(false)}><X className="w-5 h-5" /></button>
            </div>
            <div className="text-sm text-white/70 mb-2">Amount: {spend.toFixed(2)}</div>
            <input
              type="range" min="0" max="10" step="0.25"
              value={spend} onChange={e=>setSpend(parseFloat(e.target.value))}
              className="w-full"
            />
            <input
              className="mt-3 w-full rounded-xl border border-white/10 bg-black/30 px-3 py-2 text-sm"
              placeholder="What are you adding / refining?"
              value={note} onChange={e=>setNote(e.target.value)}
            />
            <div className="mt-4 flex gap-2">
              <button
                className="btn"
                onClick={() => remixSpend("guest", post.id, spend, note)}
              >
                Commit Remix
              </button>
              <div className="text-sm text-white/60 self-center">Symbolic only — not financial.</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
