'use client';
import Link from 'next/link';

export default function Header() {
  return (
    <header className="glass sticky top-0 z-30 mb-6 rounded-2xl px-4 py-3 backdrop-blur">
      <div className="flex items-center justify-between">
        <div className="text-xl font-bold tracking-wide">superNova_2177</div>
        <nav className="hidden md:flex items-center gap-2">
          <Link href="#" className="btn">🗳️ Voting</Link>
          <Link href="#" className="btn">📄 Proposals</Link>
          <Link href="#" className="btn">✅ Decisions</Link>
          <Link href="#" className="btn">⚙️ Execution</Link>
        </nav>
      </div>
    </header>
  );
}
