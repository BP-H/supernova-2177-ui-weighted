"use client";
import { useAppState } from "@/lib/state";
import Link from "next/link";
import { usePathname } from "next/navigation";

const NavButton = ({ href, children }) => {
  const pathname = usePathname();
  const active = pathname === href;
  return (
    <Link href={href}>
      <button className="sn-btn" style={active ? { outline: "2px solid var(--ring)" } : undefined}>
        {children}
      </button>
    </Link>
  );
};

export default function Sidebar() {
  const { state, set } = useAppState();

  return (
    <aside className="sn-sidebar">
      <div className="brand">💫 superNova_2177</div>

      <div className="sn-card">
        <img
          src="https://placehold.co/320x140/11131d/FFFFFF?text=superNova_2177"
          alt=""
          style={{ width: "100%", borderRadius: 12 }}
        />
        <div style={{ marginTop: 8, fontWeight: 700 }}>taha_gungor</div>
        <div style={{ opacity: 0.75 }}>ceo / test_tech</div>
      </div>

      <div className="sn-sec">Identity</div>
      <div className="sn-card">
        <label style={{ fontSize: 12, opacity: 0.8 }}>I am a…</label>
        <select
          value={state.species}
          onChange={(e) => set("species", e.target.value)}
          style={{ width: "100%", padding: 10, borderRadius: 10, background: "#161a28", border: "1px solid var(--stroke)", color: "var(--text)" }}
        >
          <option value="human">human</option>
          <option value="company">company</option>
          <option value="ai">ai</option>
        </select>

        <div style={{ height: 8 }} />

        <label style={{ fontSize: 12, opacity: 0.8 }}>Decision kind</label>
        <select
          value={state.decisionKind}
          onChange={(e) => set("decisionKind", e.target.value)}
          style={{ width: "100%", padding: 10, borderRadius: 10, background: "#161a28", border: "1px solid var(--stroke)", color: "var(--text)" }}
        >
          <option value="standard">standard</option>
          <option value="important">important</option>
        </select>
      </div>

      <div className="sn-sec">Backend</div>
      <div className="sn-card">
        <label style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <input
            type="checkbox"
            checked={state.useRealBackend}
            onChange={(e) => set("useRealBackend", e.target.checked)}
          />
          Use real backend
        </label>
        <div style={{ height: 8 }} />
        <input
          placeholder="https://api.example.com"
          value={state.backendUrl}
          onChange={(e) => set("backendUrl", e.target.value)}
          style={{ width: "100%", padding: 10, borderRadius: 10, background: "#161a28", border: "1px solid var(--stroke)", color: "var(--text)" }}
        />
      </div>

      <div className="sn-sec">Navigate</div>
      <NavButton href="/">Feed</NavButton>
      <NavButton href="/chat">Chat</NavButton>
      <NavButton href="/messages">Messages</NavButton>
      <NavButton href="/profile">Profile</NavButton>
      <NavButton href="/proposals">Proposals</NavButton>
      <NavButton href="/decisions">Decisions</NavButton>
      <NavButton href="/execution">Execution</NavButton>

      <div className="sn-sec">Premium</div>
      <NavButton href="/music">Music</NavButton>
      <NavButton href="/agents">Agents</NavButton>
      <NavButton href="/metaverse">Enter Metaverse</NavButton>
    </aside>
  );
}
