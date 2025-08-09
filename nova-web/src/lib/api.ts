// nova-web/src/lib/api.ts
export async function api(path: string, init?: RequestInit) {
  const stateRaw = typeof window !== "undefined" ? localStorage.getItem("sn2177:state") : null;
  const state = stateRaw ? JSON.parse(stateRaw) : {};
  const useReal = !!state.useRealBackend;
  const base = state.backendUrl || process.env.NEXT_PUBLIC_BACKEND_URL || "";

  if (!useReal || !base) {
    return { ok: true, json: async () => ({ demo: true }) } as unknown as Response;
  }

  const url = base.replace(/\/+$/, "") + path;
  const res = await fetch(url, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
    cache: "no-store",
  });
  return res;
}
