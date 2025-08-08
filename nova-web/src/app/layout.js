import "./globals.css";

export const metadata = {
  title: "superNova_2177",
  description: "Symbolic social sandbox — not financial."
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <div className="container">
          <div className="py-6">
            <h1 className="text-4xl font-extrabold tracking-tight">superNova_2177</h1>
            <div className="mt-2 text-sm text-white/70">
              Prototype feed (symbolic only). All metrics are symbolic reputation/engagement — not financial.
            </div>
          </div>
          <div className="grid grid-cols-5 gap-6">
            <aside className="col-span-1 space-y-2">
              <div className="card soft p-3">✨ superNova_2177</div>
              <div className="card soft p-3">📰 Feed</div>
              <div className="card soft p-3">💬 Chat</div>
              <div className="card soft p-3">✅ Decisions</div>
              <div className="card soft p-3">⚙️ Execution</div>
            </aside>
            <main className="col-span-4">{children}</main>
          </div>
        </div>
      </body>
    </html>
  );
}
