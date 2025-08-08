// nova-web/src/app/layout.js
import "./globals.css";

export const metadata = {
  title: "superNova_2177",
  description: "Prototype UI",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
