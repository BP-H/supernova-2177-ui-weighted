'use client';
import { useEffect, useState } from 'react';

function Section({ title, children }) {
  return (
    <div className="glass p-4">
      <div className="mb-3 text-sm font-semibold text-slate-300">{title}</div>
      {children}
    </div>
  );
}

function NavButton({ icon, label, active = false }) {
  return (
    <button className={`w-full text-left mb-2 btn ${active ? 'ring-1 ring-white/10 bg-white/10' : ''}`}>
      <span className="mr-2">{icon}</span>{label}
    </button>
  );
}

export default function Sidebar() {
  const [useReal, setUseReal] = useState(false);
  const [url, setUrl] = useState('');

  // simple persistence to localStorage so the values stick while testing
  useEffect(() => {
    setUrl(localStorage.getItem('backend_url') || 'http://127.0.0.1:8000');
    setUseReal(localStorage.getItem('use_real_backend') === '1');
  }, []);
  useEffect(() => { localStorage.setItem('backend_url', url); }, [url]);
  useEffect(() => { localStorage.setItem('use_real_backend', useReal ? '1' : '0'); }, [useReal]);

  return (
    <div className="sticky top-6 h-[calc(100dvh-48px)] overflow-y-auto space-y-4">
      <Section title="Backend URL">
        <input
          className="w-full rounded-xl bg-slate-900/60 border border-white/10 px-3 py-2 text-sm text-slate-200 outline-none focus:border-white/20"
          value={url}
          onChange={e => setUrl(e.target.value)}
          placeholder="https://your-fastapi-host:8000"
        />
        <label className="mt-3 flex items-center gap-2 text-sm text-slate-300">
          <input type="checkbox" checked={useReal} onChange={e => setUseReal(e.target.checked)} />
          Use real backend
        </label>
      </Section>

      <Section title="Workspaces">
        <NavButton icon="🏠" label="Test Tech" />
        <NavButton icon="✨" label="superNova_2177" active />
        <NavButton icon="🌍" label="GLOBALRUNWAY" />
      </Section>

      <Section title="Navigate">
        <NavButton icon="📰" label="Feed" />
        <NavButton icon="💬" label="Chat" />
        <NavButton icon="📬" label="Messages" />
        <NavButton icon="👤" label="Profile" />
        <NavButton icon="📑" label="Proposals" />
        <NavButton icon="✅" label="Decisions" />
        <NavButton icon="⚙️" label="Execution" />
        <NavButton icon="🪙" label="Coin" />
        <NavButton icon="🍴" label="Forks" />
        <NavButton icon="🎛️" label="Remixes" />
      </Section>

      <Section title="Premium">
        <NavButton icon="🎶" label="Music" />
        <NavButton icon="🚀" label="Agents" />
        <NavButton icon="🌌" label="Enter Metaverse" />
      </Section>

      <Section title="Settings">
        <NavButton icon="⚙️" label="Settings" />
      </Section>
    </div>
  );
}
