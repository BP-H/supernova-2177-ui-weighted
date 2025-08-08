"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState, useEffect } from "react";

const NAV = [
  { href: "/feed", label: "Feed", icon: "📰" },
  { href: "/chat", label: "Chat", icon: "💬" },
  { href: "/messages", label: "Messages", icon: "📬" },
  { href: "/profile", label: "Profile", icon: "👤" },
  { href: "/proposals", label: "Proposals", icon: "📑" },
  { href: "/decisions", label: "Decisions", icon: "✅" },
  { href: "/execution", label: "Execution", icon: "⚙️" },
];

export default function Shell({ children }) {
  const pathname = usePathname();
  const router = useRouter();

  // --- “backend” controls like ui.py
  const [useReal, setUseReal] = useState(false);
  const [backend, setBackend] = useState(
    process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000"
  );
  useEffect(() => {
    // Persist to localStorage so it survives reloads
    const s = localStorage.getItem("sn_use_real") === "1";
    const b = localStorage.getItem("sn_backend") || backend;
    setUseReal(s);
    setBackend(b);
  }, []);
  useEffect(() => {
    localStorage.setItem("sn_use_real", useReal ? "1" : "0");
  }, [useReal]);
  useEffect(() => {
    localStorage.setItem("sn_backend", backend);
  }, [backend]);

  // --- simple search
  const [q, setQ] = useState("");
  const onSearch = (e) => {
    e.preventDefault();
    router.push(`/search?q=${encodeURIComponent(q)}`);
  };

  return (
    <div className="sn-root">
      <aside className="sn-sidebar">
        <div className="sn-card">
          <img
            className="sn-cover"
            src="https://placehold.co/640x280/11131d/FFFFFF?text=superNova_2177"
            alt="cover"
          />
          <div className="sn-title">💫 superNova_2177 💫</div>
          <div className="sn-sub">Prototype — symbolic only</div>
        </div>

        <div className="sn-section">Navigate</div>
        <nav className="sn-nav">
          {NAV.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`sn-navbtn ${active ? "active" : ""}`}
              >
                <span className="sn-ico">{item.icon}</span>
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="sn-section">Search</div>
        <form onSubmit={onSearch} className="sn-search">
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Search posts, people…"
          />
        </form>

        <div className="sn-section">Backend</div>
        <div className="sn-kv">
          <label className="sn-switch">
            <input
              type="checkbox"
              checked={useReal}
              onChange={(e) => setUseReal(e.target.checked)}
            />
            <span>Use real backend</span>
          </label>
          <input
            className="sn-input"
            value={backend}
            onChange={(e) => setBackend(e.target.value)}
            placeholder="http://127.0.0.1:8000"
          />
        </div>

        <div className="sn-section">Premium</div>
        <div className="sn-premium">
          <button className="sn-pill">🎶 Music</button>
          <button className="sn-pill">🚀 Agents</button>
          <button className="sn-pill">🌌 Enter Metaverse</button>
        </div>

        <div className="sn-foot">Mathematically sucked into a superNova_2177 void — stay tuned for 3D.</div>
      </aside>

      <main className="sn-main">
        <header className="sn-header">
          <h1 className="sn-brand">superNova_2177</h1>
          <div className="sn-sweep" />
          <div className="sn-quick">
            <button onClick={() => router.push("/proposals")}>🗳️ Voting</button>
            <button onClick={() => router.push("/proposals")}>📄 Proposals</button>
            <button onClick={() => router.push("/decisions")}>✅ Decisions</button>
            <button onClick={() => router.push("/execution")}>⚙️ Execution</button>
          </div>
        </header>
        <section className="sn-content">{children}</section>
      </main>
    </div>
  );
}
