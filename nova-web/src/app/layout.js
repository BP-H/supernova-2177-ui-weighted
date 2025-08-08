export const metadata = { title: "superNova_2177", description: "Prototype UI" };

import "../app/globals.css";
import Sidebar from "../components/Sidebar";
import TopBar from "../components/TopBar";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen flex">
          <Sidebar />
          <main className="flex-1 min-w-0">
            <TopBar />
            <div className="p-4 md:p-6">{children}</div>
          </main>
        </div>
      </body>
    </html>
  );
}
