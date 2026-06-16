'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import toast from 'react-hot-toast';

type Question = {
  id: number;
  question: string;
  options: string[];
};

type WrongQuestion = {
  question_id: number;
  question: string;
  user_answer: string;
  correct_answer: string;
  explanation: string;
};

type InterviewResult = {
  total: number;
  correct_count: number;
  score_pct: number;
  passed: boolean;
  pass_threshold: number;
  min_score_pct: number;
  weak_areas: string[];
  recommended_lessons: string[];
  feedback: string;
  wrong_questions: WrongQuestion[];
};

export default function InterviewPage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [currentLevel, setCurrentLevel] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // Interview state
  const [questions, setQuestions] = useState<Question[]>([]);
  const [attemptId, setAttemptId] = useState<number | null>(null);
  const [answers, setAnswers] = useState<number[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<InterviewResult | null>(null);
  const [starting, setStarting] = useState(false);
  const [startError, setStartError] = useState<string | null>(null);

  // History
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    const load = async () => {
      try {
        const [me, cur] = await Promise.all([api.getMe(), api.getCurrentLevel()]);
        setUser(me);
        setCurrentLevel(cur);

        const hist = await api.getInterviewHistory().catch(() => []);
        setHistory(hist || []);
      } catch {
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [router]);

  const handleStart = async () => {
    if (!currentLevel) return;
    setStarting(true);
    setStartError(null);
    try {
      const data = await api.startInterview(currentLevel.level_number);
      setQuestions(data.questions);
      setAttemptId(data.attempt_id);
      setAnswers(new Array(data.total_questions).fill(-1));
      setResult(null);
    } catch (err: any) {
      setStartError(err.message);
    } finally {
      setStarting(false);
    }
  };

  const setAnswer = (questionIndex: number, optionIndex: number) => {
    setAnswers(prev => {
      const next = [...prev];
      next[questionIndex] = optionIndex;
      return next;
    });
  };

  const handleSubmit = async () => {
    if (attemptId === null) return;

    // Check all questions answered
    const unanswered = answers.findIndex(a => a === -1);
    if (unanswered !== -1) {
      toast.error(`Question ${unanswered + 1} not answered`);
      return;
    }

    setSubmitting(true);
    try {
      const res = await api.submitInterview(attemptId, answers);
      setResult(res);
      if (res.passed) {
        toast.success('Passed! Next level unlocked.');
      } else {
        toast.error(`Score: ${res.correct_count}/${res.total}. Need ${res.pass_threshold}/${res.total}.`);
      }
      setHistory(await api.getInterviewHistory());
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleRetry = () => {
    setQuestions([]);
    setAttemptId(null);
    setAnswers([]);
    setResult(null);
  };

  if (loading) {
    return (
      <div className="p-6 max-w-4xl mx-auto">
        <div className="animate-pulse space-y-4">
          <div className="h-8 w-64 skeleton" />
          <div className="h-4 w-96 skeleton" />
          <div className="h-40 skeleton" />
        </div>
      </div>
    );
  }

  const answeredCount = answers.filter(a => a !== -1).length;

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold mb-2">Mastery Interview</h1>
        <p className="text-[#94A3B8] text-sm">
          Answer 10 questions covering all topics. Pass with {currentLevel ? `${Math.ceil(10/10*100)}%` : '90%'} ({9}/10) to unlock the next level.
        </p>
      </div>

      {/* Level Info */}
      {currentLevel && !questions.length && !result && (
        <div className="glass-card p-6 mb-6">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-lg bg-[#3B82F6]/10 flex items-center justify-center text-xl shrink-0">
              {currentLevel.level_number}
            </div>
            <div className="flex-1">
              <span className="text-xs font-mono text-[#f59e0b] bg-[#f59e0b]/10 px-2 py-1 rounded">
                LEVEL {currentLevel.level_number}
              </span>
              <h3 className="font-semibold mt-2 mb-1">{currentLevel.level_data?.title}</h3>
              <p className="text-[#94A3B8] text-sm leading-relaxed">
                {currentLevel.level_data?.interview_prompt}
              </p>
            </div>
          </div>

          {startError && (
            <div className="mt-4 p-4 bg-[#f59e0b]/5 border border-[#f59e0b]/30 rounded-lg">
              <p className="text-sm text-[#f59e0b] font-semibold">Cannot Start Interview</p>
              <p className="text-xs text-[#94A3B8] mt-1">{startError}</p>
              <Link
                href={`/levels/${currentLevel.level_number}`}
                className="text-xs text-[#3B82F6] hover:underline mt-2 inline-block"
              >
                Go to Level Page &rarr;
              </Link>
            </div>
          )}

          <div className="mt-6">
            <button
              onClick={handleStart}
              disabled={starting}
              className="btn-primary text-sm"
            >
              {starting ? 'Preparing Questions...' : 'Start Interview'}
            </button>
          </div>
        </div>
      )}

      {/* Questions */}
      {questions.length > 0 && !result && (
        <div>
          {/* Progress Header */}
          <div className="glass-card p-4 mb-6 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-sm text-[#94A3B8]">
                Question {answeredCount > 0 ? answers.findIndex(a => a === -1) !== -1 ? answers.findIndex(a => a === -1) + 1 : answers.length : 1} of {questions.length}
              </span>
              <div className="w-32 h-2 bg-[#1E293B] rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-300"
                  style={{
                    width: `${(answeredCount / questions.length) * 100}%`,
                    background: 'linear-gradient(90deg, #3B82F6, #06B6D4)',
                  }}
                />
              </div>
            </div>
            <span className="text-xs text-[#64748b]">
              {answeredCount}/{questions.length} answered
            </span>
          </div>

          {/* Questions List */}
          <div className="space-y-4 mb-6">
            {questions.map((q, qi) => {
              const selected = answers[qi];

              return (
                <div
                  key={q.id}
                  className={`glass-card p-5 transition-all duration-200 ${
                    qi === answers.findIndex(a => a === -1)
                      ? 'border-[#3B82F6]/40'
                      : selected !== -1
                      ? 'border-[#10b981]/20'
                      : 'border-[#1E293B]'
                  }`}
                >
                  <div className="flex items-start gap-3 mb-3">
                    <span className="w-7 h-7 rounded-full bg-[#3B82F6]/10 text-[#3B82F6] text-xs font-bold flex items-center justify-center shrink-0">
                      {qi + 1}
                    </span>
                    <p className="text-sm text-[#F8FAFC] leading-relaxed">{q.question}</p>
                  </div>
                  <div className="ml-10 space-y-2">
                    {q.options.map((opt, oi) => (
                      <label
                        key={oi}
                        className={`flex items-start gap-3 p-3 rounded-lg cursor-pointer transition-all duration-150 ${
                          selected === oi
                            ? 'bg-[#3B82F6]/10 border border-[#3B82F6]/30'
                            : 'bg-[#1E293B]/50 border border-[#1E293B] hover:border-[#334155]'
                        }`}
                      >
                        <input
                          type="radio"
                          name={`q-${q.id}`}
                          checked={selected === oi}
                          onChange={() => setAnswer(qi, oi)}
                          className="mt-0.5 accent-[#3B82F6]"
                        />
                        <span className="text-sm text-[#94A3B8] leading-relaxed">{opt}</span>
                      </label>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Submit */}
          <div className="glass-card p-4 mb-6 flex items-center justify-between">
            <span className="text-xs text-[#64748b]">
              {answeredCount === questions.length
                ? 'All questions answered'
                : `${questions.length - answeredCount} question(s) remaining`}
            </span>
            <button
              onClick={handleSubmit}
              disabled={submitting || answeredCount !== questions.length}
              className="btn-success text-sm"
            >
              {submitting ? 'Evaluating...' : 'Submit Answers'}
            </button>
          </div>
        </div>
      )}

      {/* Results */}
      {result && (
        <div>
          {/* Score Card */}
          <div className={`glass-card p-6 mb-6 ${result.passed ? 'border-[#10b981]/30' : 'border-[#ef4444]/30'}`}>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-bold">Interview Result</h3>
                <p className="text-xs text-[#64748b] mt-1">
                  {result.passed ? 'Level completed!' : 'Keep practicing'}
                </p>
              </div>
              <div className="text-center">
                <div className={`text-3xl font-bold ${result.passed ? 'text-[#10b981]' : 'text-[#ef4444]'}`}>
                  {result.correct_count}/{result.total}
                </div>
                <div className={`text-xs ${result.passed ? 'text-[#10b981]' : 'text-[#ef4444]'}`}>
                  {result.score_pct.toFixed(0)}%
                </div>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="h-3 bg-[#1E293B] rounded-full overflow-hidden mb-4">
              <div
                className={`h-full rounded-full transition-all duration-700 ${
                  result.passed ? 'progress-fill-green' : ''
                }`}
                style={{
                  width: `${result.score_pct}%`,
                  background: result.passed
                    ? 'linear-gradient(90deg, #10b981, #34d399)'
                    : 'linear-gradient(90deg, #ef4444, #f97316)',
                }}
              />
            </div>

            <div className={`p-4 rounded-lg ${result.passed ? 'bg-[#10b981]/10 border border-[#10b981]/20' : 'bg-[#ef4444]/10 border border-[#ef4444]/20'}`}>
              <p className={`font-semibold text-sm ${result.passed ? 'text-[#10b981]' : 'text-[#ef4444]'}`}>
                {result.passed ? 'PASSED' : 'NOT PASSED'}
                <span className="font-normal ml-2 opacity-80">
                  (need {result.pass_threshold}/{result.total} = {result.min_score_pct.toFixed(0)}%)
                </span>
              </p>
            </div>
          </div>

          {/* Wrong Questions */}
          {result.wrong_questions.length > 0 && (
            <div className="glass-card p-6 mb-6">
              <h3 className="font-semibold mb-4 flex items-center gap-2">
                <span className="text-[#ef4444]">Mistakes</span>
                <span className="text-xs text-[#64748b] font-normal">({result.wrong_questions.length} incorrect)</span>
              </h3>
              <div className="space-y-4">
                {result.wrong_questions.map((wq, i) => (
                  <div key={i} className="bg-[#1E293B]/50 border border-[#ef4444]/20 rounded-lg p-4">
                    <p className="text-sm text-[#F8FAFC] font-medium mb-2">{wq.question}</p>
                    <div className="grid grid-cols-2 gap-3 mb-2">
                      <div className="bg-[#ef4444]/5 rounded p-2">
                        <span className="text-xs text-[#ef4444] font-mono">Your answer</span>
                        <p className="text-sm text-[#F8FAFC] mt-0.5">{wq.user_answer}</p>
                      </div>
                      <div className="bg-[#10b981]/5 rounded p-2">
                        <span className="text-xs text-[#10b981] font-mono">Correct</span>
                        <p className="text-sm text-[#F8FAFC] mt-0.5">{wq.correct_answer}</p>
                      </div>
                    </div>
                    <div className="bg-[#111827] rounded p-3">
                      <span className="text-xs text-[#3B82F6] font-mono">Explanation</span>
                      <p className="text-xs text-[#94A3B8] mt-1 leading-relaxed">{wq.explanation}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Weak Areas */}
          {result.weak_areas.length > 0 && (
            <div className="glass-card p-6 mb-6">
              <h3 className="font-semibold mb-3">Weak Areas</h3>
              <div className="flex flex-wrap gap-2">
                {result.weak_areas.map((area, i) => (
                  <span key={i} className="text-xs px-3 py-1.5 rounded-full bg-[#f59e0b]/10 text-[#f59e0b] border border-[#f59e0b]/20">
                    {area}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Recommended Lessons */}
          {result.recommended_lessons.length > 0 && !result.passed && (
            <div className="glass-card p-6 mb-6">
              <h3 className="font-semibold mb-3">Recommended Lessons to Review</h3>
              <div className="space-y-2">
                {result.recommended_lessons.map((lesson, i) => (
                  <div key={i} className="flex items-center gap-3 p-3 bg-[#1E293B]/50 rounded-lg border border-[#1E293B]">
                    <span className="text-[#3B82F6]">&#9654;</span>
                    <span className="text-sm text-[#94A3B8]">{lesson}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Feedback */}
          <div className="glass-card p-6 mb-6">
            <h3 className="font-semibold mb-3">Detailed Feedback</h3>
            <div className="bg-[#111827] border border-[#1E293B] rounded-lg p-4">
              <p className="text-sm text-[#94A3B8] whitespace-pre-wrap leading-relaxed">{result.feedback}</p>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-3">
            {!result.passed ? (
              <button onClick={handleRetry} className="btn-primary text-sm">
                Try Again (New Questions)
              </button>
            ) : (
              <Link href="/dashboard" className="btn-success text-sm">
                Back to Dashboard
              </Link>
            )}
            <Link href={`/levels/${currentLevel?.level_number}`} className="btn-secondary text-sm">
              Review Level
            </Link>
          </div>
        </div>
      )}

      {/* Past Attempts */}
      {history.length > 0 && !questions.length && (
        <div className="glass-card p-6 mt-6">
          <h3 className="font-semibold mb-4">Past Attempts</h3>
          <div className="space-y-2">
            {history
              .filter((a: any) => a.level_number === currentLevel?.level_number)
              .slice(0, 5)
              .map((a: any) => (
                <div key={a.id} className="bg-[#111827] border border-[#1E293B] rounded-lg p-3 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className={`text-sm font-semibold ${a.passed ? 'text-[#10b981]' : 'text-[#ef4444]'}`}>
                      {a.correct_count}/{a.total}
                    </span>
                    <span className={`text-xs ${a.passed ? 'text-[#10b981]' : 'text-[#ef4444]'}`}>
                      {a.passed ? 'Passed' : 'Failed'}
                    </span>
                  </div>
                  <span className="text-xs text-[#64748b]">
                    {new Date(a.created_at).toLocaleDateString(undefined, {
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </span>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* Error state */}
      {!currentLevel && (
        <div className="glass-card p-6 text-center">
          <p className="text-[#94A3B8] text-sm">Could not load level information. Make sure you're logged in.</p>
          <Link href="/dashboard" className="btn-primary text-sm mt-4 inline-block">Go to Dashboard</Link>
        </div>
      )}
    </div>
  );
}
