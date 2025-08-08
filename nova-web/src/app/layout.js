import "./globals.css";
import Sidebar from "@/components/Sidebar";
import TopBar from "@/components/TopBar";

export const metadata = { title: "superNova_2177" };

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <div className="sn-app">
          <Sidebar />
          <div>
            <TopBar />
            <div className="sn-content">
              <div className="sn-sweep" />
              {children}
            </div>
          </div>
        </div>
      </body>
    </html>
  );
}
