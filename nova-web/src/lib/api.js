// nova-web/src/lib/api.js

// Small fetch helper for the nova-web UI. It talks to your FastAPI backend if
// NEXT_PUBLIC_BACKEND_URL is set; otherwise it gracefully falls back to a demo feed.

const readStored = (k, d = null) =>
  typeof window === "undefined" ? d : (localStorage.getItem(k) || d);

let BASE =
  process.env.NEXT_PUBLIC_BACKEND_URL ||
  readStored("backend_url", "http://127.0.0.1:8000"); // fallback for local dev

function setBackend(url) {
  BASE = url || BASE;
  try { localStorage.setItem("backend_url", BASE); } catch (_) {}
}

function getBackend() {
  return BASE;
}

async function jsonFetch(path, opts = {}) {
  const url = `${BASE}${path}`;
  const init = {
    method: "GET",
    headers: { "Content-Type": "application/json", ...(opts.headers || {}) },
    credentials: "include",      // include cookies if your API sets them
    mode: "cors",
    ...opts,
  };
  if (opts.body && typeof opts.body !== "string") {
    init.body = JSON.stringify(opts.body);
  }
  const res = await fetch(url, init);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} @ ${path}`);
  const ct = res.headers.get("content-type") || "";
  return ct.includes("application/json") ? res.json() : res.text();
}

async function safePost(path, body) {
  try {
    const out = await jsonFetch(path, { method: "POST", body });
    return typeof out === "object" ? out : { ok: true, data: out };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}

// --- API surface the UI will use --------------------------------------------

async function health() {
  try { return await jsonFetch("/healthz"); }
  catch (e) { return { status: "degraded", error: e.message }; }
}

async function getReactions(postId) {
  try { return await jsonFetch(`/reactions/${postId}`); }
  catch { return { counts: {} }; }
}

function like(postId, user) {
  // your FastAPI has POST /vibenodes/{id}/like
  return safePost(`/vibenodes/${postId}/like`, { user });
}

function react(postId, user, emoji) {
  // map emojis to tokens if your backend expects them
  const map = { "👍": "up", "❤️": "heart", "😅": "laugh", "🤗": "hug", "👀": "eyes", "🔥": "fire" };
  return safePost(`/reactions`, { post_id: postId, user, emoji: map[emoji] || emoji });
}

function remix(postId, user, note, spend) {
  // backend may ignore spend if not implemented—safe.
  return safePost(`/remix`, { post_id: postId, user, note, spend });
}

function tip(fromUser, toUser, amount, memo) {
  return safePost(`/tip`, { from: fromUser, to: toUser, amount, memo });
}

function reward(postId, split) {
  return safePost(`/reward`, { post_id: postId, split });
}

function share(postId, channel = "link") {
  // cheap client-side success for now; wire a real endpoint later.
  return Promise.resolve({ ok: true, postId, channel });
}

function createVibeNode(name, description, tags = [], author = "guest") {
  return safePost(`/vibenodes`, { name, description, tags, author });
}

// --- Demo data if backend is down -------------------------------------------
function demoFeed(n = 8) {
  const now = Date.now();
  const names = ["Ann Guzman", "Mike Wagner", "Steven Carroll"];
  const titles = [
    "Public relations officer at Silva Group • 1st",
    "Designer at Brown Ltd • 3rd",
    "Paramedic at Petty-Juarez • 2nd",
  ];
  return Array.from({ length: n }).map((_, i) => ({
    id: i + 1,
    author_name: names[i % names.length],
    author_title: titles[i % titles.length],
    author_avatar: `https://api.dicebear.com/7.x/thumbs/svg?seed=${i}`,
    text: "Prototype content — symbolic only.",
    image_url: i % 2 === 0 ? `https://picsum.photos/seed/${i + now}/1024/512` : null,
    stats: { likes: 0, comments: 0, reposts: 0 },
  }));
}

async function feedOrDemo() {
  try {
    const data = await jsonFetch("/feed");
    return Array.isArray(data) ? data : demoFeed();
  } catch {
    return demoFeed();
  }
}

export const API = {
  setBackend,
  getBackend,
  health,
  getReactions,
  like,
  react,
  remix,
  tip,
  reward,
  share,
  createVibeNode,
  feedOrDemo,
};

export default API;
