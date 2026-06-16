'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';

export default function LeaderboardPage() {
  const [entries, setEntries] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await api.getLeaderboard();
        setEntries(data);
      } catch {}
      setLoading(false);
    };
    load();
  }, []);

  const getRankStyle = (rank: number) => {
    if (rank === 1) return 'text-[#f59e0b]';
    if (rank === 2) return 'text-[#94A3B8]';
    if (rank === 3) return 'text-[#d97706]';
    return 'text-[#64748b]';
  };

  const getRankEmoji = (rank: number) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
  };

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[60vh]">
        <div className="w-8 h-8 border-2 border-[#f59e0b] border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold mb-2">🏆 Leaderboard</h1>
        <p className="text-[#94A3B8] text-sm">Top bug bounty learners ranked by XP</p>
      </div>

      <div className="glass-card overflow-hidden">
        <div className="grid grid-cols-12 gap-4 px-6 py-3 bg-[#111827] border-b border-[#1E293B] text-xs text-[#64748b] font-mono">
          <div className="col-span-1">Rank</div>
          <div className="col-span-5">Hunter</div>
          <div className="col-span-3 text-center">Level</div>
          <div className="col-span-3 text-right">XP</div>
        </div>
        {entries.length === 0 ? (
          <div className="p-8 text-center text-[#64748b]">No learners yet. Be the first!</div>
        ) : (
          entries.map((entry: any) => (
            <div
              key={entry.user_id}
              className={`grid grid-cols-12 gap-4 px-6 py-4 border-b border-[#1E293B] last:border-0 items-center ${
                entry.is_current_user ? 'bg-[#f59e0b]/5' : 'hover:bg-[#1E293B]/50'
              } transition-colors`}
            >
              <div className={`col-span-1 text-sm font-bold ${getRankStyle(entry.rank)}`}>
                {getRankEmoji(entry.rank)}
              </div>
              <div className="col-span-5 flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#f59e0b]/20 to-[#ef4444]/20 border border-[#f59e0b]/20 flex items-center justify-center text-sm">
                  {entry.name?.charAt(0)?.toUpperCase() || '?'}
                </div>
                <div>
                  <span className="text-sm font-medium text-[#F8FAFC]">{entry.name || 'Anonymous'}</span>
                  {entry.is_current_user && <span className="text-xs text-[#f59e0b] ml-2">(you)</span>}
                </div>
              </div>
              <div className="col-span-3 text-center text-sm text-[#94A3B8]">
                Level {entry.level_reached}
              </div>
              <div className="col-span-3 text-right text-sm font-semibold text-[#f59e0b]">
                {entry.xp_points} XP
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
