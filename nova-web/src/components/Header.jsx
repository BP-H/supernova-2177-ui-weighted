export default function Header() {
  return (
    <header className="mb-4">
      <h1 className="text-4xl font-extrabold tracking-tight text-white">
        superNova_2177
      </h1>
      <div className="mt-3 flex items-center gap-3">
        <span className="pill">Prototype feed (symbolic only)</span>
        <span className="text-xs text-slate-400">
          All metrics are symbolic reputation/engagement — not financial.
        </span>
      </div>
      <div className="mt-6 h-2 w-full rounded-full bg-white/5" />
    </header>
  );
}
