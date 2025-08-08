'use client';
import { useState } from 'react';
import Sidebar from './Sidebar';

export default function SidebarMobile() {
  const [open, setOpen] = useState(false);
  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="btn fixed bottom-5 left-5 z-40 lg:hidden"
        aria-label="Open menu"
      >
        ☰ Menu
      </button>

      {open && (
        <div className="fixed inset-0 z-50">
          <div className="absolute inset-0 bg-black/60" onClick={() => setOpen(false)} />
          <div className="absolute left-0 top-0 h-full w-[85%] max-w-[320px] p-4">
            <div className="glass h-full overflow-y-auto p-2">
              <div className="mb-3 flex items-center justify-between px-2">
                <div className="text-sm text-slate-300">Navigation</div>
                <button className="btn" onClick={() => setOpen(false)}>✕</button>
              </div>
              <Sidebar />
            </div>
          </div>
        </div>
      )}
    </>
  );
}
