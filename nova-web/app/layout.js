// nova-web/app/layout.js
import "./globals.css";

export const metadata = { title: "superNova_2177" };

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body style={{ background:"#0a0b10", color:"#e9ecf1", margin:0 }}>
        {children}
      </body>
    </html>
  );
}
