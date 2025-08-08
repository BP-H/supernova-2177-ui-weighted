import './globals.css';
import { Inter } from 'next/font/google';
import Sidebar from '@/components/Sidebar';
import SidebarMobile from '@/components/SidebarMobile';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'superNova_2177',
  description: 'Prototype social UI (symbolic only)',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-grid`}>
        <div className="mx-auto w-full max-w-7xl grid grid-cols-1 lg:grid-cols-[280px_minmax(0,1fr)] gap-6 px-4 py-8">
          {/* Sidebar (desktop) */}
          <aside className="hidden lg:block"><Sidebar /></aside>
          {/* Main content */}
          <main>{children}</main>
        </div>
        {/* Sidebar trigger + drawer (mobile) */}
        <SidebarMobile />
      </body>
    </html>
  );
}
