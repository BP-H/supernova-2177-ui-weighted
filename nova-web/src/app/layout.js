// Root layout required by Next.js App Router
import './globals.css';

export const metadata = { title: 'superNova_2177' };

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#0a0b10] text-white antialiased">
        {children}
      </body>
    </html>
  );
}
