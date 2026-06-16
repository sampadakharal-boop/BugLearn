'use client';

interface ProgressPathProps {
  currentLevel: number;
  totalLevels: number;
  completedLevels: number;
}

export default function ProgressPath({ currentLevel, totalLevels, completedLevels }: ProgressPathProps) {
  const progress = totalLevels > 0 ? (completedLevels / totalLevels) * 100 : 0;

  return (
    <div className="glass-card p-6 mb-6 overflow-hidden">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-sm">Your Progression Path</h3>
        <span className="text-xs text-[#64748b] font-mono">
          {completedLevels}/{totalLevels} levels
        </span>
      </div>

      {/* Main progress bar */}
      <div className="relative h-4 bg-[#1E293B] rounded-full overflow-hidden mb-3">
        <div
          className="h-full rounded-full transition-all duration-1000 ease-out animate-progress-glow"
          style={{
            width: `${progress}%`,
            background: 'linear-gradient(90deg, #f59e0b, #ef4444, #8B5CF6)',
            animation: progress > 0 ? 'progress-glow 2s ease-in-out infinite' : 'none',
          }}
        />
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-[10px] font-bold text-white drop-shadow-md">
            {Math.round(progress)}%
          </span>
        </div>
      </div>

      {/* Level nodes */}
      <div className="relative mt-6 pt-2">
        <div className="absolute top-0 left-0 right-0 h-0.5 bg-[#1E293B]" />
        <div className="flex justify-between relative">
          {Array.from({ length: Math.min(totalLevels, 30) }).map((_, i) => {
            const levelNum = i + 1;
            const isCompleted = levelNum < currentLevel;
            const isCurrent = levelNum === currentLevel;
            const isLocked = levelNum > currentLevel;

            return (
              <div key={i} className="flex flex-col items-center relative" style={{ width: `${100 / Math.min(totalLevels, 30)}%` }}>
                {/* Connecting line fill */}
                {isCompleted && (
                  <div
                    className="absolute top-0 h-0.5 bg-gradient-to-r from-[#f59e0b] to-[#ef4444] transition-all duration-700"
                    style={{ right: '50%', left: i === 0 ? '0' : undefined, width: i === 0 ? '50%' : '100%' }}
                  />
                )}
                {/* Node */}
                <div
                  className={`relative z-10 w-5 h-5 rounded-full border-2 transition-all duration-500 flex items-center justify-center text-[9px] font-bold ${
                    isCompleted
                      ? 'bg-[#10b981] border-[#10b981] text-white scale-100'
                      : isCurrent
                      ? 'bg-[#f59e0b] border-[#f59e0b] text-[#0B1220] scale-110 animate-pulse'
                      : 'bg-[#1E293B] border-[#334155] text-[#64748b] scale-90'
                  }`}
                >
                  {isCompleted ? '✓' : isCurrent ? '●' : ''}
                </div>
                {/* Label */}
                <span className={`text-[9px] mt-1 font-mono ${
                  isCompleted ? 'text-[#10b981]' : isCurrent ? 'text-[#f59e0b]' : 'text-[#334155]'
                }`}>
                  {levelNum}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
