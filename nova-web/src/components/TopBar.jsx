"use client";

import Link from "next/link";

const Tile = ({ href, icon, label }) => (
  <Link href={href} className="btn h-12">
    <span>{icon}</span>
    <span className="font-medium">{label}</span>
  </Link>
);

export default function TopBar() {
  return (
    <div className="sticky top-0 z-20 bg-[var(--panel-2)]/80 backdrop-blur border-b border-[var(--stroke)]">
      <div className="flex items-center gap-3 px-4 py-3">
        <Tile href="/voting" icon="🗳️" label="Voting" />
        <Tile href="/proposals" icon="📄" label="Proposals" />
        <Tile href="/decisions" icon="✅" label="Decisions" />
        <Tile href="/execution" icon="⚙️" label="Execution" />
        <div className="ml-auto w-64">
          <input
            placeholder="🔍 Search…"
            className="w-full h-10 px-3 rounded-md border border-[var(--stroke)] bg-[#161a28] outline-none"
          />
        </div>
      </div>
    </div>
  );
}
