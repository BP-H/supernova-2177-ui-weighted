import "./globals.css";
import Link from "next/link";

export const metadata = { title: "superNova_2177" };

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <div className="app">
          <aside className="sidebar">
            <div className="brand">💫 superNova_2177</div>
            <nav className="nav">
              <Link href="/">Feed</Link>
              <Link href="/chat">Chat</Link>
              <Link href="/messages">Messages</Link>
              <Link href="/profile">Profile</Link>
              <Link href="/proposals">Proposals</Link>
              <Link href="/decisions">Decisions</Link>
              <Link href="/execution">Execution</Link>
            </nav>
          </aside>
          <main className="content">{children}</main>
        </div>
      </body>
    </html>
  );
}
