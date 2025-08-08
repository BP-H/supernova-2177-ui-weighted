"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function ProposalsPage() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    (async () => {
      const res = await api("/proposals");
      const data = await res.json();
      // demo fallback shape
      setItems(data.demo ? [
        { id: 1, title: "Create music guild", desc: "Spin up an autonomous collective" },
        { id: 2, title: "Enable image posts", desc: "Ship media upload" },
      ] : data);
    })();
  }, []);

  return (
    <div style={{ display:"grid", gap:12 }}>
      <h2>Proposals</h2>
      {items.map(p => (
        <div key={p.id} className="sn-post">
          <div style={{ fontWeight:700 }}>{p.title}</div>
          <div style={{ opacity:.8 }}>{p.desc || p.description}</div>
          <div className="sn-actions">
            <button onClick={() => alert("👍 upvote (wire to /votes)")}>👍 Upvote</button>
            <button onClick={() => alert("👎 downvote (wire to /votes)")}>👎 Downvote</button>
            <button onClick={() => alert("🧮 tally (wire to /tally)")}>🧮 Tally</button>
          </div>
        </div>
      ))}
    </div>
  );
}
