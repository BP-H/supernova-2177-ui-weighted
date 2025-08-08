const BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "";

export async function healthz() {
  try {
    const r = await fetch(`${BASE}/healthz`, { cache: "no-store" });
    if (!r.ok) throw new Error();
    return await r.json();
  } catch { return null; }
}

export async function listFeed() {
  // Try a real endpoint if you add one later (e.g. /feed)
  try {
    const r = await fetch(`${BASE}/feed`, { cache: "no-store" });
    if (r.ok) return await r.json();
  } catch {}

  // Fallback demo data
  return Array.from({ length: 6 }).map((_, i) => ({
    id: `post-${i}`,
    author: {
      name: ["Rebecca Bauer","Robert Owens","Sophia Sanders"][i%3],
      title: ["Herbalist • 1st","Control surveyor • 3rd","PR officer • 1st"][i%3],
      avatar: `https://api.dicebear.com/7.x/thumbs/svg?seed=nv${i}`
    },
    text: "Available might fast minute create her.",
    image: i % 2 ? `https://picsum.photos/1024/512?random=${i+7}` : null,
    promoted: i === 0,
    likes: 120 + i*7, comments: 30 + i*3, reposts: 10 + i
  }));
}

export async function react(postId, emoji) {
  try {
    await fetch(`${BASE}/reactions/${postId}`, {
      method: "POST",
      headers: { "Content-Type":"application/json" },
      body: JSON.stringify({ emoji })
    });
  } catch {}
}

export async function remixSpend(user, postId, amount, note) {
  try {
    await fetch(`${BASE}/remix/${postId}`, {
      method: "POST",
      headers: { "Content-Type":"application/json" },
      body: JSON.stringify({ user, amount, note })
    });
  } catch {}
}
