import "./globals.css";

export const metadata = {
  title: "superNova_2177",
  description: "white-dominant UI with neon accents",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      {/* IMPORTANT: pull colors from CSS variables, not Tailwind dark classes */}
      <body className="bg-[var(--bg)] text-[var(--text)] antialiased">
        {children}
      </body>
    </html>
  );
}
