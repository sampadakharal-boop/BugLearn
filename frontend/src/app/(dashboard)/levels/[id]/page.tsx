'use client';

import { useState, useEffect, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import { getTopicIdFromName } from '@/lib/lesson-content';
import toast from 'react-hot-toast';
import LevelCelebration from '@/components/ui/LevelCelebration';

export default function LevelDetailPage() {
  const params = useParams();
  const router = useRouter();
  const levelNumber = parseInt(params.id as string);
  const [levelData, setLevelData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState('topics');
  const [quiz, setQuiz] = useState<any>(null);
  const [quizAnswers, setQuizAnswers] = useState<number[]>([]);
  const [quizResult, setQuizResult] = useState<any>(null);
  const [quizLoading, setQuizLoading] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [celebration, setCelebration] = useState<{type: 'complete' | 'unlock' | 'achievement'; title: string} | null>(null);
  const topicsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMounted(true);
    const load = async () => {
      try {
        const data = await api.getLevel(levelNumber);
        setLevelData(data);
        const q = await api.getQuiz(levelNumber);
        setQuiz(q);
        setQuizAnswers(new Array(q.questions.length).fill(-1));
      } catch (err: any) {
        if (err.message?.includes('401')) { api.clearToken(); router.push('/login'); }
        else toast.error(err.message);
      } finally { setLoading(false); }
    };
    load();
  }, [levelNumber]);

  const setAns = (qIdx: number, ansIdx: number) => {
    const copy = [...quizAnswers];
    copy[qIdx] = ansIdx;
    setQuizAnswers(copy);
  };

  const submitQuiz = async () => {
    if (quizAnswers.includes(-1)) { toast.error('Answer all questions first'); return; }
    setQuizLoading(true);
    try {
      const res = await api.submitQuiz(levelNumber, quizAnswers);
      setQuizResult(res);
      if (res.passed) {
        toast.success('Quiz passed! Now you can take the interview.');
        setCelebration({ type: 'achievement', title: 'Quiz Passed' });
      }
      else toast.error(`Score: ${res.score}/${res.total}. Need 70% to pass.`);
    } catch (err: any) { toast.error(err.message); }
    finally { setQuizLoading(false); }
  };

  if (loading) return (
    <div className="p-8 flex items-center justify-center min-h-[60vh]">
      <div className="w-8 h-8 border-2 border-[#f59e0b] border-t-transparent rounded-full animate-spin" />
    </div>
  );

  if (!levelData) return (
    <div className="p-8 text-center"><p className="text-[#94A3B8]">Level not found or locked.</p><Link href="/dashboard" className="btn-primary mt-4 inline-block">Back</Link></div>
  );

  const { level_data } = levelData;
  const tabs = [
    { id: 'topics', label: '📖 Topics', icon: '📖' },
    { id: 'quiz', label: '📝 Quiz', icon: '📝' },
    { id: 'task', label: '🎯 Task', icon: '🎯' },
    { id: 'notes', label: '📓 Notes', icon: '📓' },
  ];

  return (
    <div className="p-6 max-w-4xl mx-auto pb-20">
      {celebration && (
        <LevelCelebration
          levelNumber={levelNumber}
          levelTitle={celebration.title}
          type={celebration.type as any}
          onClose={() => setCelebration(null)}
        />
      )}

      <Link href="/dashboard" className="text-[#94A3B8] hover:text-[#F8FAFC] text-sm flex items-center gap-1 mb-4 group">
        <span className="transition-transform group-hover:-translate-x-1 inline-block">←</span> Dashboard
      </Link>

      <div className={`mb-6 ${mounted ? 'animate-slide-up opacity-0' : ''}`} style={mounted ? {animationDelay: '0.1s', animationFillMode: 'forwards'} : {}}>
        <div className="flex items-center gap-3 mb-3">
          <span className="text-xs font-mono text-[#f59e0b] bg-[#f59e0b]/10 px-3 py-1.5 rounded-full border border-[#f59e0b]/20">
            LEVEL {levelNumber}
          </span>
          {level_data.xp_reward && (
            <span className="text-xs font-mono text-[#8B5CF6] bg-[#8B5CF6]/10 px-3 py-1.5 rounded-full border border-[#8B5CF6]/20">
              +{level_data.xp_reward} XP
            </span>
          )}
        </div>
        <h1 className="text-3xl font-bold mt-2 mb-1">{level_data.title}</h1>
        <p className="text-[#94A3B8] text-sm">{level_data.description}</p>
      </div>

      <div className={`flex gap-1 mb-6 bg-[#111827] rounded-lg p-1 border border-[#1E293B] ${mounted ? 'animate-slide-up opacity-0' : ''}`} style={mounted ? {animationDelay: '0.2s', animationFillMode: 'forwards'} : {}}>
        {tabs.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)} className={`flex-1 px-4 py-2.5 rounded-md text-sm font-medium transition-all duration-200 ${tab === t.id ? 'bg-[#f59e0b]/10 text-[#f59e0b] border border-[#f59e0b]/20 shadow-sm' : 'text-[#64748b] hover:text-[#F8FAFC] hover:bg-[#1E293B]'}`}>
            <span className="mr-1.5">{t.icon}</span>
            {t.label}
          </button>
        ))}
      </div>

      {tab === 'topics' && (
        <div className="space-y-3" ref={topicsRef}>
          {level_data.topics?.map((topic: any, i: number) => {
            const lessonId = getTopicIdFromName(topic.name);
            return (
              <Link
                key={i}
                href={lessonId ? `/levels/${levelNumber}/topics/${lessonId}` : '#'}
                className={`glass-card group flex items-center gap-4 p-5 transition-all duration-300 card-hover-lift ${mounted ? 'animate-slide-up opacity-0' : ''} ${lessonId ? 'hover:border-[#f59e0b]/30 hover:bg-[#f59e0b]/5 cursor-pointer border-flow' : 'cursor-default'}`}
                style={mounted ? {animationDelay: `${0.3 + i * 0.08}s`, animationFillMode: 'forwards'} : {}}
              >
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#f59e0b]/20 to-[#ef4444]/20 border border-[#f59e0b]/20 flex items-center justify-center text-xl flex-shrink-0 group-hover:scale-110 transition-transform duration-300">
                  {topic.emoji}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-sm group-hover:text-[#f59e0b] transition-colors duration-200">{topic.name}</h3>
                  <p className="text-xs text-[#64748b] mt-0.5 line-clamp-1">{topic.content?.slice(0, 100)}...</p>
                </div>
                <div className="flex items-center gap-2 text-[#64748b] group-hover:text-[#f59e0b] transition-colors duration-200">
                  <span className="text-xs hidden sm:inline">Read Lesson</span>
                  <span className="text-lg transition-transform group-hover:translate-x-1 inline-block">→</span>
                </div>
              </Link>
            );
          })}

          <div className={`mt-6 glass-card p-4 border-[#f59e0b]/30 bg-gradient-to-r from-[#f59e0b]/5 to-transparent ${mounted ? 'animate-slide-up opacity-0' : ''}`} style={mounted ? {animationDelay: `${0.3 + level_data.topics?.length * 0.08}s`, animationFillMode: 'forwards'} : {}}>
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-[#f59e0b]/20 flex items-center justify-center text-sm animate-heartbeat">📖</div>
              <p className="text-sm text-[#f59e0b] font-semibold">Click any topic to open the full lesson with diagrams, examples, and knowledge checks.</p>
            </div>
          </div>
        </div>
      )}

      {tab === 'quiz' && (
        <div className={`glass-card p-6 ${mounted ? 'animate-scale-in opacity-0' : ''}`} style={mounted ? {animationDelay: '0.2s', animationFillMode: 'forwards'} : {}}>
          <div className="flex items-center gap-3 mb-2">
            <span className="text-lg">📝</span>
            <h3 className="font-bold">Knowledge Check</h3>
          </div>
          <p className="text-[#94A3B8] text-sm mb-6">Answer all questions correctly (70%+) to unlock the interview.</p>

          {quiz?.questions?.map((q: any, qi: number) => (
            <div key={qi} className={`mb-5 p-4 rounded-lg transition-all duration-500 ${
              quizResult
                ? (quizResult.results[qi]?.correct
                  ? 'bg-[#10b981]/5 border border-[#10b981]/20'
                  : 'bg-[#ef4444]/5 border border-[#ef4444]/20')
                : 'bg-[#111827] border border-[#1E293B] hover:border-[#f59e0b]/20'
            } ${mounted ? 'animate-fade-in opacity-0' : ''}`} style={mounted ? {animationDelay: `${0.3 + qi * 0.1}s`, animationFillMode: 'forwards'} : {}}>
              <p className="text-sm font-medium mb-3 flex items-center gap-2">
                <span className="w-6 h-6 rounded-full bg-[#f59e0b]/10 text-[#f59e0b] text-xs flex items-center justify-center font-mono">{qi + 1}</span>
                {q.q}
              </p>
              <div className="space-y-2">
                {q.opts.map((opt: string, oi: number) => {
                  const isSelected = quizAnswers[qi] === oi;
                  const isCorrect = quizResult?.results[qi]?.correct_answer === oi;
                  const showResult = quizResult && (isSelected || isCorrect);
                  let cls = 'bg-[#1E293B] hover:bg-[#334155] border-[#334155]';
                  if (showResult && isCorrect) cls = 'bg-[#10b981]/10 border-[#10b981]/30 text-[#10b981]';
                  else if (showResult && isSelected && !isCorrect) cls = 'bg-[#ef4444]/10 border-[#ef4444]/30 text-[#ef4444]';
                  else if (isSelected) cls = 'bg-[#f59e0b]/10 border-[#f59e0b]/30 text-[#f59e0b]';
                  return (
                    <button key={oi} onClick={() => !quizResult && setAns(qi, oi)} disabled={!!quizResult}
                      className={`w-full text-left px-4 py-2.5 rounded-lg border text-sm transition-all duration-200 ${cls} ${quizResult ? 'cursor-default' : 'cursor-pointer hover:scale-[1.01] active:scale-[0.99]'}`}>
                      <span className="w-5 h-5 rounded-full border border-current inline-flex items-center justify-center mr-2 text-[10px] font-mono shrink-0">
                        {String.fromCharCode(65 + oi)}
                      </span>
                      {opt}
                    </button>
                  );
                })}
              </div>
              {quizResult && (
                <div className={`mt-2 text-xs ${quizResult.results[qi]?.correct ? 'text-[#10b981]' : 'text-[#ef4444]'}`}>
                  {quizResult.results[qi]?.correct ? '✓ Correct' : `✗ Incorrect — answer: ${String.fromCharCode(65 + quizResult.results[qi]?.correct_answer)}`}
                </div>
              )}
            </div>
          ))}

          {!quizResult ? (
            <button onClick={submitQuiz} disabled={quizLoading}
              className="btn-primary text-sm mt-4 transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]">
              {quizLoading ? (
                <span className="flex items-center gap-2">
                  <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Submitting...
                </span>
              ) : 'Submit Quiz'}
            </button>
          ) : (
            <div className={`mt-6 p-6 rounded-lg transition-all duration-500 ${
              quizResult.passed
                ? 'bg-gradient-to-r from-[#10b981]/10 to-emerald-500/5 border border-[#10b981]/20 animate-scale-in'
                : 'bg-gradient-to-r from-[#ef4444]/10 to-red-500/5 border border-[#ef4444]/20 animate-scale-in'
            }`}>
              <div className="flex items-center gap-3 mb-2">
                <span className={`text-2xl ${quizResult.passed ? 'animate-badge-reveal' : ''}`}>
                  {quizResult.passed ? '🎉' : '💪'}
                </span>
                <div>
                  <p className={`font-bold text-lg ${quizResult.passed ? 'text-[#10b981]' : 'text-[#ef4444]'}`}>
                    {quizResult.passed ? 'Quiz Passed!' : 'Keep Trying'}
                  </p>
                  <p className="text-sm text-[#94A3B8]">
                    Score: {quizResult.score}/{quizResult.total} ({Math.round((quizResult.score / quizResult.total) * 100)}%)
                  </p>
                </div>
              </div>
              {quizResult.passed && (
                <p className="text-sm text-[#10b981] mt-1">You can now take the AI Voice Interview and submit your handwritten notes.</p>
              )}
              {!quizResult.passed && (
                <p className="text-sm text-[#ef4444] mt-1">Review the topics above and try again. You need 70% to pass.</p>
              )}
              <div className="flex gap-3 mt-4">
                {quizResult.passed && (
                  <>
                    <Link href="/interview" className="btn-primary text-sm hover:scale-[1.02] active:scale-[0.98] transition-all">
                      Take Interview
                    </Link>
                    <Link href={`/notes?level=${levelNumber}`} className="btn-accent text-sm hover:scale-[1.02] active:scale-[0.98] transition-all">
                      Submit Notes
                    </Link>
                  </>
                )}
                <button onClick={() => { setQuizResult(null); setQuizAnswers(new Array(quiz?.questions?.length || 0).fill(-1)); }}
                  className="btn-secondary text-sm">
                  Retry Quiz
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {tab === 'notes' && (
        <div className={`glass-card p-6 ${mounted ? 'animate-scale-in opacity-0' : ''}`} style={mounted ? {animationDelay: '0.2s', animationFillMode: 'forwards'} : {}}>
          <div className="flex items-center gap-3 mb-4">
            <span className="text-2xl">📓</span>
            <div>
              <h3 className="font-bold text-lg">Handwritten Notes</h3>
              <p className="text-xs text-[#64748b]">Upload photos of your handwritten notes for evaluation</p>
            </div>
          </div>
          <div className="bg-gradient-to-r from-[#f59e0b]/5 to-transparent border border-[#f59e0b]/10 rounded-lg p-4 mb-4">
            <p className="text-sm text-[#94A3B8]">
              Write comprehensive study notes on paper, take a photo, and upload it. Your notes will be analyzed for handwriting authenticity and content coverage. Pass both the interview (86%+) and notes (65%+) to complete this level.
            </p>
          </div>
          <div className="bg-[#111827] border border-[#1E293B] rounded-lg p-4 mb-4">
            <p className="text-xs text-[#64748b] mb-2 font-mono uppercase tracking-wider">Requirements</p>
            <ul className="text-sm text-[#94A3B8] space-y-1.5">
              {[
                'Cover all key concepts from the level',
                'Write in your own words on paper',
                'Take clear, well-lit photos',
                'Upload PNG/JPG/WebP (max 10MB each)',
                'Minimum quality score of 65% to pass',
              ].map((req, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-[#10b981] mt-0.5">✓</span>
                  {req}
                </li>
              ))}
            </ul>
          </div>
          <Link href={`/notes?level=${levelNumber}`}
            className="btn-primary text-sm inline-flex items-center gap-2 hover:scale-[1.02] active:scale-[0.98] transition-all duration-200">
            <span>📸</span>
            Upload Notes
          </Link>
        </div>
      )}

      {tab === 'task' && level_data.task && (
        <div className={`glass-card p-6 border-[#f59e0b]/30 ${mounted ? 'animate-scale-in opacity-0' : ''}`} style={mounted ? {animationDelay: '0.2s', animationFillMode: 'forwards'} : {}}>
          <div className="flex items-center gap-3 mb-4">
            <span className="text-2xl">🎯</span>
            <div>
              <h3 className="font-bold text-lg">{level_data.task.title}</h3>
              <p className="text-xs text-[#64748b]">Practical task — apply what you learned</p>
            </div>
          </div>
          <p className="text-[#94A3B8] text-sm mb-4">{level_data.task.description}</p>
          <div className="bg-[#111827] border border-[#1E293B] rounded-lg p-4 mb-4">
            <p className="text-xs text-[#64748b] mb-2 font-mono">Expected solution:</p>
            <div className="text-[#F8FAFC] text-sm whitespace-pre-wrap font-mono leading-relaxed">{level_data.task.expected_answer}</div>
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono text-[#8B5CF6] bg-[#8B5CF6]/10 px-2.5 py-1 rounded-full border border-[#8B5CF6]/20">
                +{level_data.task.xp_reward} XP
              </span>
            </div>
            <button onClick={() => setTab('quiz')}
              className="btn-primary text-sm hover:scale-[1.02] active:scale-[0.98] transition-all duration-200">
              Take Quiz
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
