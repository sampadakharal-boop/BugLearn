'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navItems = [
  { href: '/dashboard', label: 'Dashboard', icon: '◈' },
  { href: '/interview', label: 'Interview', icon: '🎤' },
  { href: '/notes', label: 'Notes', icon: '📝' },
  { href: '/leaderboard', label: 'Leaderboard', icon: '🏆' },
];

export default function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  const isActive = (href: string) => {
    if (href === '/dashboard') return pathname === '/dashboard';
    return pathname.startsWith(href);
  };

  return (
    <div className={`${collapsed ? 'w-16' : 'w-56'} bg-[#111827] border-r border-[#1E293B] flex flex-col transition-all duration-300`}>
      <div className="h-16 flex items-center justify-between px-4 border-b border-[#1E293B]">
        <Link href="/" className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-md bg-gradient-to-br from-[#f59e0b] to-[#ef4444] flex items-center justify-center text-white font-bold text-xs">B</div>
          {!collapsed && <span className="text-sm font-bold">Bug<span className="text-[#f59e0b]">Learn</span></span>}
        </Link>
        <button onClick={() => setCollapsed(!collapsed)} className="text-[#64748b] hover:text-[#F8FAFC] transition-colors">
          {collapsed ? '▶' : '◀'}
        </button>
      </div>
      <nav className="flex-1 py-4 px-2 space-y-1">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-200 ${
              isActive(item.href)
                ? 'text-[#f59e0b] bg-[#f59e0b]/10 border border-[#f59e0b]/20'
                : 'text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-[#1E293B]'
            }`}
            title={collapsed ? item.label : undefined}
          >
            <span className="text-lg">{item.icon}</span>
            {!collapsed && <span>{item.label}</span>}
          </Link>
        ))}
      </nav>
      <div className="p-4 border-t border-[#1E293B]">
        <Link
          href="/login"
          onClick={() => { if (typeof window !== 'undefined') localStorage.removeItem('token'); }}
          className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-[#64748b] hover:text-red-400 hover:bg-red-500/5 transition-all"
        >
          <span>🚪</span>
          {!collapsed && <span>Logout</span>}
        </Link>
      </div>
    </div>
  );
}
