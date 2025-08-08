import './globals.css';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'superNova_2177',
  description: 'Prototype social UI (symbolic only)',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-grid`}>{children}</body>
    </html>
  );
}
