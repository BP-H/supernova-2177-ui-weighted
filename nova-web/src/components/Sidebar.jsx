"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NavItem = ({ href, icon, label }) => {
  const pathname = usePathname();
  const active = pathname === href;
  return (
    <Link
      href={href}
      className={`block w-full btn text-sm text-left ${active ? "ring-2 ring-[var(--ring)]" : ""}`}
    >
      <span className="w-5 text-center">{icon}</span>
      <span>{label}</span>
    </Link>
  );
};

export default function Sidebar() {
  return (
    <aside className="w-[260px] hidden md:flex flex-col gap-3 p-3 border-r border-[var(--stroke)] bg-[var(--panel)]">
      {/* Brand */}
      <div className="card p-3">
        <div className="font-bold text-lg">superNova_2177</div>
        <div className="text-sm text-[var(--muted)]">Prototype (symbolic only)</div>
      </div>

      {/* Workspaces */}
      <div className="text-xs text-[var(--muted)] px-1">Workspaces</div>
      <NavItem href="/" icon="🏠" label="Test Tech" />
      <NavItem href="/" icon="✨" label="superNova_2177" />
      <NavItem href="/" icon="🌍" label="GLOBALRUNWAY" />

      <div className="h-[1px] bg-[var(--stroke)] my-2" />

      {/* Navigate */}
      <div className="text-xs text-[var(--muted)] px-1">Navigate</div>
      <NavItem href="/" icon="📰" label="Feed" />
      <NavItem href="/chat" icon="💬" label="Chat" />
      <NavItem href="/messages" icon="📬" label="Messages" />
      <NavItem href="/profile" icon="👤" label="Profile" />
      <NavItem href="/proposals" icon="📑" label="Proposals" />
      <NavItem href="/decisions" icon="✅" label="Decisions" />
      <NavItem href="/execution" icon="⚙️" label="Execution" />

      <div className="h-[1px] bg-[var(--stroke)] my-2" />

      {/* Premium */}
      <div className="text-xs text-[var(--muted)] px-1">Premium</div>
      <NavItem href="/music" icon="🎶" label="Music" />
      <NavItem href="/agents" icon="🚀" label="Agents" />
      <NavItem href="/metaverse" icon="🌌" label="Enter Metaverse" />

      <div className="mt-auto text-xs text-[var(--muted)] px-1">
        Mathematically sucked into a superNova_2177 void — stay tuned for 3D immersion.
      </div>
    </aside>
  );
}
