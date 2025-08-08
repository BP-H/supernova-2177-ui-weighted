"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function TopBar() {
  const r = useRouter();
  const [q, setQ] = useState("");

  return (
    <div className="sn-top">
      <div style={{ fontWeight: 800 }}>superNova_2177</div>
      <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
        <input
          placeholder="🔍 Search…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onKeyDown={(e)=> e.key==='Enter' && r.push(`/search?q=${encodeURIComponent(q)}`)}
          style={{ padding: 10, width: 320, borderRadius: 10, background: "#161a28", border: "1px solid var(--stroke)", color: "var(--text)" }}
        />
        <div className="sn-quick">
          <button onClick={() => r.push("/voting")}>🗳️ Voting</button>
          <button onClick={() => r.push("/proposals")}>📄 Proposals</button>
          <button onClick={() => r.push("/decisions")}>✅ Decisions</button>
          <button onClick={() => r.push("/execution")}>⚙️ Execution</button>
        </div>
      </div>
    </div>
  );
}
