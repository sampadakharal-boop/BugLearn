'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';

export default function TopBar() {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const me = await api.getMe();
        setUser(me);
      } catch {}
    };
    if (api.token) load();
  }, []);

  return (
    <div className="h-14 bg-[#111827]/80 backdrop-blur-xl border-b border-[#1E293B] flex items-center justify-between px-6">
      <div className="flex items-center gap-3">
        <span className="text-[#94A3B8] text-sm">Welcome back,</span>
        <span className="text-[#F8FAFC] font-semibold">{user?.name || 'Hunter'}</span>
      </div>
      <div className="flex items-center gap-4">
        {user && (
          <>
            <div className="flex items-center gap-2 text-sm">
              <span className="text-[#f59e0b]">Level {user.current_level}</span>
              <span className="text-[#64748b]">|</span>
              <span className="text-[#10b981]">{user.xp_points} XP</span>
            </div>
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#f59e0b] to-[#ef4444] flex items-center justify-center text-white font-bold text-xs">
              {user.name?.charAt(0)?.toUpperCase() || 'H'}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
