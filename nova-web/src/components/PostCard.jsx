'use client';
import Image from 'next/image';

const avatarUrl = (seed) =>
  `https://api.dicebear.com/7.x/thumbs/svg?seed=${encodeURIComponent(seed || 'user')}`;

export default function PostCard({
  authorName = 'Ann Guzman',
  authorTitle = 'Public relations officer at Silva Group • 1st',
  text = 'Prototype content — symbolic only.',
  imageUrl = '',
  promoted = false,
  stats = { likes: 0, comments: 0, reposts: 0 }
}) {
  return (
    <article className="content-card">
      {/* header */}
      <div className="flex items-start gap-3">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={avatarUrl(authorName)} alt="" width={48} height={48} className="rounded-full" />
        <div className="flex-1">
          <div className="font-semibold">{authorName}</div>
          <div className="small-muted">{authorTitle}</div>
          {promoted && <div className="badge mt-2">Promoted</div>}
        </div>
      </div>

      {/* body */}
      <div className="mt-4 text-slate-200">{text}</div>
      {imageUrl ? (
        <div className="mt-4 overflow-hidden rounded-xl border border-white/10">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={imageUrl} alt="" className="w-full h-auto" />
        </div>
      ) : null}

      {/* meta */}
      <div className="meta-row mt-3">
        {stats.likes} likes • {stats.comments} comments • {stats.reposts} reposts
      </div>

      {/* actions */}
      <div className="mt-3 grid grid-cols-2 md:grid-cols-4 gap-2">
        <button className="btn">👍 Like</button>
        <button className="btn">💬 Comment</button>
        <button className="btn">🔁 Repost</button>
        <button className="btn">📤 Share</button>
      </div>

      {/* secondary */}
      <div className="mt-3 grid grid-cols-2 md:grid-cols-4 gap-2">
        <button className="btn ghost">❤️ React</button>
        <button className="btn ghost">🎛️ Remix</button>
        <button className="btn ghost">💝 Tip</button>
        <button className="btn ghost">🏆 Reward</button>
      </div>
    </article>
  );
}
