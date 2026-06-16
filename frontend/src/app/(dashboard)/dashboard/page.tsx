'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';

const statusColors: Record<string, string> = {
  locked: 'bg-[#1E293B] text-[#64748b]',
  in_progress: 'bg-[#f59e0b]/10 text-[#f59e0b] border border-[#f59e0b]/20',
  completed: 'bg-[#10b981]/10 text-[#10b981] border border-[#10b981]/20',
};

const levelEmojis = ['🌐', '📄', '📡', '📮', '🚧', '💰', '🔍', '📡', '🏢', '🗺️', '🤖', '💭', '🔓', '🍪', '🔓', '📈', '📜', '💉', '🎣', '📎', '📂', '🔄', '💻', '🔀', '🧠', '🔍', '⛓️', '📋', '📝', '🎯'];

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [levels, setLevels] = useState<any[]>([]);
  const [currentLevel, setCurrentLevel] = useState<any>(null);
  const [achievements, setAchievements] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [me, progress, cur, ach] = await Promise.all([
          api.getMe(), api.getLevelProgress(), api.getCurrentLevel(),
          api.getAchievements().catch(() => []),
        ]);
        setUser(me); setLevels(progress); setCurrentLevel(cur); setAchievements(ach || []);
      } catch (err: any) {
        if (err.message?.includes('401')) { api.clearToken(); router.push('/login'); }
      } finally { setLoading(false); }
    };
    load();
  }, []);

  if (loading) return (
    <div className="p-8 flex items-center justify-center min-h-[60vh]">
      <div className="w-8 h-8 border-2 border-[#f59e0b] border-t-transparent rounded-full animate-spin" />
    </div>
  );

  const completed = levels.filter(l => l.status === 'completed').length;
  const progressPct = Math.round((completed / 30) * 100);

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <p className="text-[#94A3B8] text-sm">Your bug bounty learning journey</p>
        </div>
        <div className="flex items-center gap-3 text-sm">
          <span className="text-[#64748b]">Level {user?.current_level}</span>
          <div className="h-2 w-24 bg-[#1E293B] rounded-full overflow-hidden">
            <div className="h-full rounded-full bg-gradient-to-r from-[#f59e0b] to-[#ef4444] transition-all" style={{ width: `${progressPct}%` }} />
          </div>
          <span className="text-[#10b981] font-mono">{user?.xp_points} XP</span>
        </div>
      </div>

      {currentLevel && (
        <div className="glass-card p-6 mb-8 glow relative overflow-hidden">
          <div className="absolute top-0 right-0 w-48 h-48 bg-[#f59e0b]/5 rounded-full blur-3xl" />
          <div className="relative">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <span className="text-xs font-mono text-[#f59e0b] bg-[#f59e0b]/10 px-2 py-1 rounded">CURRENT LEVEL</span>
                <h2 className="text-xl font-bold mt-3 mb-1">Level {currentLevel.level_number}: {currentLevel.level_data?.title}</h2>
                <p className="text-[#94A3B8] text-sm mb-4">{currentLevel.level_data?.description}</p>
                <div className="flex items-center gap-3 flex-wrap">
                  <Link href={`/levels/${currentLevel.level_number}`} className="btn-primary text-sm">Start Learning</Link>
                  <Link href="/interview" className="btn-secondary text-sm">Take Interview</Link>
                  <Link href={`/notes?level=${currentLevel.level_number}`} className="btn-accent text-sm">Write Notes</Link>
                </div>
              </div>
              <div className="text-5xl opacity-20">{levelEmojis[currentLevel.level_number - 1] || '📚'}</div>
            </div>
            <div className="mt-4 flex items-center gap-4 text-sm text-[#94A3B8]">
              <span>Status: <span className={`px-2 py-0.5 rounded text-xs ${statusColors[currentLevel.progress?.status] || statusColors.locked}`}>{currentLevel.progress?.status?.replace('_', ' ') || 'locked'}</span></span>
              {currentLevel.progress?.interview_score != null && (
                <span>Interview: <span className={currentLevel.progress.interview_score >= 86 ? 'text-[#10b981]' : 'text-[#ef4444]'}>{currentLevel.progress.interview_score}/100</span></span>
              )}
            </div>
            <div className="mt-3 flex items-center gap-3 text-xs text-[#64748b]">
              <span className={currentLevel.progress?.status !== 'locked' ? 'text-[#10b981]' : ''}>&#10003; Lessons</span>
              <span className="text-[#334155]">|</span>
              <span className={currentLevel.progress?.interview_score != null && currentLevel.progress.interview_score >= 86 ? 'text-[#10b981]' : ''}>
                {currentLevel.progress?.interview_score != null && currentLevel.progress.interview_score >= 86 ? '\u2713 ' : ''}Interview (86%)
              </span>
              <span className="text-[#334155]">|</span>
              <span className={currentLevel.progress?.notes_approved ? 'text-[#10b981]' : ''}>
                {currentLevel.progress?.notes_approved ? '\u2713 ' : ''}Notes (65%)
              </span>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="glass-card p-5">
          <div className="text-2xl font-bold text-[#f59e0b]">{completed}/30</div>
          <div className="text-sm text-[#94A3B8] mt-1">Levels Completed</div>
          <div className="mt-3 h-1.5 bg-[#1E293B] rounded-full overflow-hidden">
            <div className="h-full rounded-full bg-gradient-to-r from-[#f59e0b] to-[#ef4444]" style={{ width: `${progressPct}%` }} />
          </div>
        </div>
        <div className="glass-card p-5">
          <div className="text-2xl font-bold text-[#10b981]">{user?.xp_points || 0}</div>
          <div className="text-sm text-[#94A3B8] mt-1">Total XP Earned</div>
        </div>
        <div className="glass-card p-5">
          <div className="text-2xl font-bold text-[#3B82F6]">{achievements.length}</div>
          <div className="text-sm text-[#94A3B8] mt-1">Achievements Unlocked</div>
          {achievements.length > 0 && (
            <div className="flex gap-1 mt-2">
              {achievements.map((a: any) => <span key={a.id} title={a.title}>{a.icon}</span>)}
            </div>
          )}
        </div>
      </div>

      {achievements.length > 0 && (
        <div className="glass-card p-5 mb-8">
          <h3 className="font-semibold mb-3 flex items-center gap-2"><span>🏆</span> Achievements</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {achievements.map((a: any) => (
              <div key={a.id} className="bg-[#111827] border border-[#1E293B] rounded-lg p-3 text-center">
                <div className="text-2xl mb-1">{a.icon}</div>
                <div className="text-xs font-semibold">{a.title}</div>
                <div className="text-[10px] text-[#64748b]">{a.description}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div>
        <h3 className="font-semibold mb-4 flex items-center gap-2"><span>📚</span> All Levels</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {levels.map((level) => (
            <div key={level.level_number} className={`glass-card p-4 ${level.status === 'locked' ? 'opacity-50 pointer-events-none' : 'hover:border-[#f59e0b]/30 transition-all'}`}>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className="text-xl">{levelEmojis[level.level_number - 1] || '📚'}</span>
                  <span className="text-xs font-mono text-[#64748b]">Level {level.level_number}</span>
                </div>
                <span className={`text-xs px-2 py-0.5 rounded ${statusColors[level.status] || statusColors.locked}`}>{level.status.replace('_', ' ')}</span>
              </div>
              <h4 className="font-semibold text-sm mb-1">{level.title}</h4>
              {level.status !== 'locked' && <Link href={`/levels/${level.level_number}`} className="text-xs text-[#f59e0b] hover:underline mt-2 inline-block">Start →</Link>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
