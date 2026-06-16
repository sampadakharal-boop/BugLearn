'use client';

import { useEffect, useState } from 'react';

interface LevelCelebrationProps {
  levelNumber: number;
  levelTitle: string;
  type: 'complete' | 'unlock' | 'achievement';
  achievementName?: string;
  onClose?: () => void;
}

function ConfettiPiece({ index }: { index: number }) {
  const colors = ['#f59e0b', '#ef4444', '#3B82F6', '#10b981', '#8B5CF6', '#06B6D4'];
  const color = colors[index % colors.length];
  const left = `${Math.random() * 100}%`;
  const delay = `${Math.random() * 2}s`;
  const duration = `${2 + Math.random() * 3}s`;
  const size = `${6 + Math.random() * 8}px`;

  return (
    <div
      className="absolute"
      style={{
        left,
        top: '-10px',
        width: size,
        height: size,
        backgroundColor: color,
        borderRadius: Math.random() > 0.5 ? '50%' : '2px',
        animation: `confetti-fall ${duration} ease-in ${delay} infinite`,
        opacity: 0.8,
      }}
    />
  );
}

export default function LevelCelebration({ levelNumber, levelTitle, type, achievementName, onClose }: LevelCelebrationProps) {
  const [visible, setVisible] = useState(true);
  const [showContent, setShowContent] = useState(false);

  useEffect(() => {
    const t1 = setTimeout(() => setShowContent(true), 100);
    const t2 = setTimeout(() => { setVisible(false); onClose?.(); }, 5000);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, [onClose]);

  if (!visible) return null;

  const title = type === 'complete' ? 'Level Complete!' : type === 'unlock' ? 'New Level Unlocked!' : 'Achievement Unlocked!';
  const icon = type === 'complete' ? '🎉' : type === 'unlock' ? '🔓' : '🏆';

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center pointer-events-none">
      {/* Confetti */}
      <div className="absolute inset-0 overflow-hidden">
        {Array.from({ length: 30 }).map((_, i) => (
          <ConfettiPiece key={i} index={i} />
        ))}
      </div>

      {/* Content */}
      <div className={`relative transition-all duration-500 ${showContent ? 'opacity-100 scale-100' : 'opacity-0 scale-50'}`}>
        <div className="glass-card p-8 text-center max-w-sm mx-4 border-[#f59e0b]/30 pointer-events-auto"
          style={{ animation: showContent ? 'glow-pulse 2s ease-in-out infinite' : 'none' }}>
          <div className="text-5xl mb-4 animate-badge-reveal">{icon}</div>
          <h3 className="text-xl font-bold mb-1">{title}</h3>
          <div className="text-sm text-[#f59e0b] font-mono mb-2">LEVEL {levelNumber}</div>
          <p className="text-[#94A3B8] text-sm">{levelTitle}</p>
          {achievementName && (
            <div className="mt-3 px-3 py-1.5 rounded-full bg-[#8B5CF6]/10 text-[#8B5CF6] text-xs border border-[#8B5CF6]/20 inline-block">
              {achievementName}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
