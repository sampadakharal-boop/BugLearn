'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import toast from 'react-hot-toast';

type ScoreBreakdown = {
  concept_coverage: number;
  clarity_score: number;
  accuracy_score: number;
  completeness_score: number;
  examples_score: number;
};

type NotesResult = {
  id: number;
  level_number: number;
  quality_score: number;
  passed: boolean;
  pass_threshold: number;
  score_breakdown: ScoreBreakdown;
  matched_concepts: string[];
  missing_concepts: string[];
  weak_areas: string[];
  recommended_lessons: string[];
  flag_spam: boolean;
  flag_too_short: boolean;
  flag_copied: boolean;
  feedback: string;
  created_at: string;
};

export default function NotesPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const levelFromParam = searchParams.get('level');
  const [currentLevel, setCurrentLevel] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [files, setFiles] = useState<File[]>([]);
  const [previews, setPreviews] = useState<string[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<NotesResult | null>(null);
  const [prevAttempts, setPrevAttempts] = useState<number>(0);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const targetLevel = levelFromParam ? parseInt(levelFromParam) : null;
  const MAX_FILES = 5;

  useEffect(() => {
    const load = async () => {
      try {
        await api.getMe();
        let levelNum = targetLevel;
        if (!levelNum) {
          const cur = await api.getCurrentLevel();
          setCurrentLevel(cur);
          levelNum = cur.level_number;
        } else {
          const cur = await api.getCurrentLevel();
          setCurrentLevel(cur);
        }

        if (levelNum === null) return;
        try {
          const status = await api.getNotesStatus(levelNum);
          if (status.has_passed_notes) {
            toast.success('Notes already approved for this level!');
            router.push('/dashboard');
            return;
          }
          setPrevAttempts(status.total_attempts);
          if (status.latest_attempt) {
            setResult(status.latest_attempt);
          }
        } catch {
          // No notes yet
        }
      } catch {
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [router, targetLevel]);

  const handleFilesSelected = (newFiles: FileList | null) => {
    if (!newFiles) return;
    const remaining = MAX_FILES - files.length;
    const toAdd = Array.from(newFiles).slice(0, remaining);
    setFiles(prev => [...prev, ...toAdd]);
    toAdd.forEach(f => {
      const reader = new FileReader();
      reader.onload = e => setPreviews(prev => [...prev, e.target?.result as string]);
      reader.readAsDataURL(f);
    });
  };

  const removeFile = (idx: number) => {
    setFiles(prev => prev.filter((_, i) => i !== idx));
    setPreviews(prev => prev.filter((_, i) => i !== idx));
  };

  const handleSubmit = async () => {
    const levelNum = targetLevel || currentLevel?.level_number;
    if (!levelNum) return;

    if (files.length === 0) {
      toast.error('Upload at least one photo of your handwritten notes');
      return;
    }

    setSubmitting(true);
    try {
      const res = await api.submitNotes(levelNum, files);
      setResult(res);
      if (res.passed) {
        toast.success(`Notes approved! Score: ${res.quality_score}%`);
      } else {
        toast.error(`Score: ${res.quality_score}%. Need ${res.pass_threshold}% to pass.`);
      }
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const scoreColor = (score: number) =>
    score >= 80 ? 'text-[#10b981]' : score >= 50 ? 'text-[#f59e0b]' : 'text-[#ef4444]';

  const barColor = (score: number) =>
    score >= 80 ? 'bg-[#10b981]' : score >= 50 ? 'bg-[#f59e0b]' : 'bg-[#ef4444]';

  if (loading) {
    return (
      <div className="p-6 max-w-4xl mx-auto">
        <div className="animate-pulse space-y-4">
          <div className="h-8 w-64 skeleton" />
          <div className="h-4 w-96 skeleton" />
          <div className="h-64 skeleton" />
        </div>
      </div>
    );
  }

  const levelNum = targetLevel || currentLevel?.level_number || 1;

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold mb-2">Handwritten Notes</h1>
        <p className="text-[#94A3B8] text-sm">
          Upload photos of your handwritten notes for Level {levelNum}. Write on paper, take a photo, and upload.
        </p>
      </div>

      {/* Level context */}
      {currentLevel && (
        <div className="glass-card p-4 mb-6 flex items-center gap-3">
          <span className="text-xs font-mono text-[#f59e0b] bg-[#f59e0b]/10 px-2 py-1 rounded shrink-0">
            LEVEL {levelNum}
          </span>
          <span className="text-sm text-[#94A3B8]">
            {currentLevel.level_data?.title || `Level ${levelNum}`}
          </span>
          {prevAttempts > 0 && (
            <span className="text-xs text-[#64748b] ml-auto">
              {prevAttempts} previous attempt(s)
            </span>
          )}
        </div>
      )}

      {/* Tips */}
      <div className="glass-card p-4 mb-6 border-[#3B82F6]/20 bg-[#3B82F6]/5">
        <h3 className="text-sm font-semibold text-[#3B82F6] mb-2">Tips for Good Notes</h3>
        <ul className="text-xs text-[#94A3B8] space-y-1 list-disc list-inside">
          <li>Cover all the key concepts from this level</li>
          <li>Write in your own words — don't copy from the lesson</li>
          <li>Include real-world bug bounty examples</li>
          <li>Use diagrams and flowcharts to visualize attack flows</li>
          <li>Add a summary section to reinforce key takeaways</li>
          <li>Take clear, well-lit photos of each page</li>
          <li>Upload up to {MAX_FILES} pages (PNG/JPG/WebP, max 10MB each)</li>
        </ul>
      </div>

      {/* Upload zone */}
      {(!result || !result.passed) && (
        <div className="glass-card p-6 mb-6">
          <h3 className="font-semibold mb-3">Upload Your Handwritten Notes</h3>

          {/* Drop zone */}
          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-all cursor-pointer ${
              dragOver
                ? 'border-[#3B82F6] bg-[#3B82F6]/10'
                : 'border-[#1E293B] hover:border-[#64748b] bg-[#111827]/50'
            }`}
            onDragOver={e => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={e => { e.preventDefault(); setDragOver(false); handleFilesSelected(e.dataTransfer.files); }}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="image/png,image/jpeg,image/webp"
              capture="environment"
              multiple
              className="hidden"
              onChange={e => handleFilesSelected(e.target.files)}
            />
            <div className="text-4xl mb-2">📷</div>
            <p className="text-sm text-[#94A3B8] mb-1">
              {files.length === 0
                ? 'Drop photos here or click to browse'
                : `Tap to add more (${files.length}/${MAX_FILES})`}
            </p>
            <p className="text-xs text-[#64748b]">
              PNG, JPG, or WebP &middot; Up to 10MB each &middot; {MAX_FILES} max
            </p>
          </div>

          {/* Preview gallery */}
          {previews.length > 0 && (
            <div className="mt-4 grid grid-cols-2 sm:grid-cols-3 gap-3">
              {previews.map((src, i) => (
                <div key={i} className="relative group rounded-lg overflow-hidden border border-[#1E293B]">
                  <img src={src} alt={`Note page ${i + 1}`} className="w-full h-32 object-cover" />
                  <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <button
                      onClick={e => { e.stopPropagation(); removeFile(i); }}
                      className="bg-red-500/80 text-white text-xs px-3 py-1 rounded-full hover:bg-red-500"
                    >
                      Remove
                    </button>
                  </div>
                  <div className="absolute bottom-0 left-0 right-0 bg-black/60 text-[10px] text-white text-center py-0.5">
                    Page {i + 1}
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="flex items-center justify-between mt-4">
            <button
              onClick={() => { setFiles([]); setPreviews([]); }}
              className="btn-secondary text-sm"
              disabled={submitting || files.length === 0}
            >
              Clear All
            </button>
            <button
              onClick={handleSubmit}
              disabled={submitting || files.length === 0}
              className="btn-primary text-sm"
            >
              {submitting ? 'Analyzing...' : 'Submit Notes for Review'}
            </button>
          </div>
        </div>
      )}

      {/* Result */}
      {result && (
        <div>
          {/* Score Overview */}
          <div className={`glass-card p-6 mb-6 ${result.passed ? 'border-[#10b981]/30' : 'border-[#ef4444]/30'}`}>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-bold">Notes Review Result</h3>
                <p className="text-xs text-[#64748b] mt-1">
                  {result.passed ? 'Your notes demonstrate good understanding!' : 'Keep improving'}
                </p>
              </div>
              <div className="text-center">
                <div className={`text-3xl font-bold ${result.passed ? 'text-[#10b981]' : 'text-[#ef4444]'}`}>
                  {result.quality_score}%
                </div>
                <div className={`text-xs ${result.passed ? 'text-[#10b981]' : 'text-[#ef4444]'}`}>
                  {result.passed ? 'PASSED' : `Need ${result.pass_threshold}%`}
                </div>
              </div>
            </div>

            {/* Progress bar */}
            <div className="h-3 bg-[#1E293B] rounded-full overflow-hidden mb-4">
              <div
                className={`h-full rounded-full transition-all duration-700 ${result.passed ? 'bg-[#10b981]' : ''}`}
                style={{
                  width: `${result.quality_score}%`,
                  background: result.passed
                    ? 'linear-gradient(90deg, #10b981, #34d399)'
                    : 'linear-gradient(90deg, #ef4444, #f97316)',
                }}
              />
            </div>

            <div className={`p-4 rounded-lg ${result.passed ? 'bg-[#10b981]/10 border border-[#10b981]/20' : 'bg-[#ef4444]/10 border border-[#ef4444]/20'}`}>
              <p className={`font-semibold text-sm ${result.passed ? 'text-[#10b981]' : 'text-[#ef4444]'}`}>
                {result.passed ? 'NOTES APPROVED' : 'NEEDS IMPROVEMENT'}
                <span className="font-normal ml-2 opacity-80">
                  (minimum {result.pass_threshold}%)
                </span>
              </p>
            </div>
          </div>

          {/* Score Breakdown */}
          {!result.passed && (
            <div className="glass-card p-6 mb-6">
              <h3 className="font-semibold mb-4">Score Breakdown</h3>
              <div className="space-y-3">
                {([
                  ['Concept Coverage', result.score_breakdown.concept_coverage, 'Covers key topics from the level'],
                  ['Completeness', result.score_breakdown.completeness_score, 'Depth and structure of notes'],
                  ['Clarity & Understanding', result.score_breakdown.clarity_score, 'Own words, explanations, analogies'],
                  ['Accuracy', result.score_breakdown.accuracy_score, 'Correct explanations of concepts'],
                  ['Examples & Application', result.score_breakdown.examples_score, 'Real-world bug bounty examples'],
                ] as const).map(([label, score, hint]) => (
                  <div key={label}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs text-[#94A3B8]">{label}</span>
                      <div className="flex items-center gap-2">
                        <span className={`text-xs font-mono font-semibold ${scoreColor(score)}`}>
                          {score}%
                        </span>
                        <span className="text-[10px] text-[#64748b]">({hint})</span>
                      </div>
                    </div>
                    <div className="h-2 bg-[#1E293B] rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all duration-500 ${barColor(score)}`}
                        style={{ width: `${score}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-4 p-3 bg-[#111827] rounded-lg">
                <span className="text-xs text-[#64748b]">
                  Handwriting authenticity analysis
                  {result.flag_spam && ' | Flagged: low quality'}
                  {result.flag_copied && ' | Flagged: suspicious content'}
                  {result.flag_too_short && ' | Flagged: insufficient content'}
                </span>
              </div>
            </div>
          )}

          {/* Missing Concepts */}
          {result.missing_concepts.length > 0 && (
            <div className="glass-card p-6 mb-6">
              <h3 className="font-semibold mb-3 text-[#f59e0b]">Missing Concepts</h3>
              <p className="text-xs text-[#94A3B8] mb-3">
                These important topics were not found in your notes. Add your understanding of each:
              </p>
              <div className="flex flex-wrap gap-2">
                {result.missing_concepts.map((concept, i) => (
                  <span key={i} className="text-xs px-3 py-1.5 rounded-full bg-[#f59e0b]/10 text-[#f59e0b] border border-[#f59e0b]/20">
                    {concept}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Matched Concepts */}
          {result.matched_concepts.length > 0 && (
            <div className="glass-card p-6 mb-6">
              <h3 className="font-semibold mb-3 text-[#10b981]">Concepts Covered</h3>
              <div className="flex flex-wrap gap-2">
                {result.matched_concepts.map((concept, i) => (
                  <span key={i} className={`text-xs px-3 py-1.5 rounded-full ${
                    result.passed
                      ? 'bg-[#10b981]/10 text-[#10b981] border border-[#10b981]/20'
                      : 'bg-[#3B82F6]/10 text-[#3B82F6] border border-[#3B82F6]/20'
                  }`}>
                    &#10003; {concept}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Weak Areas */}
          {result.weak_areas.length > 0 && !result.passed && (
            <div className="glass-card p-6 mb-6">
              <h3 className="font-semibold mb-3 text-[#ef4444]">Areas to Improve</h3>
              <ul className="space-y-2">
                {result.weak_areas.map((area, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-[#94A3B8]">
                    <span className="text-[#ef4444] mt-0.5">&#9654;</span>
                    {area}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommended Lessons */}
          {result.recommended_lessons.length > 0 && !result.passed && (
            <div className="glass-card p-6 mb-6">
              <h3 className="font-semibold mb-3">Recommended Lessons</h3>
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

          {/* Detailed Feedback */}
          <div className="glass-card p-6 mb-6">
            <h3 className="font-semibold mb-3">Detailed Feedback</h3>
            <div className="bg-[#111827] border border-[#1E293B] rounded-lg p-4">
              <p className="text-sm text-[#94A3B8] whitespace-pre-wrap leading-relaxed">{result.feedback}</p>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-3">
            {!result.passed ? (
              <button onClick={() => { setResult(null); setFiles([]); setPreviews([]); }} className="btn-primary text-sm">
                Revise & Upload New Notes
              </button>
            ) : (
              <Link href="/dashboard" className="btn-success text-sm">
                Back to Dashboard
              </Link>
            )}
            <Link href={`/levels/${levelNum}`} className="btn-secondary text-sm">
              Review Level Content
            </Link>
          </div>
        </div>
      )}

      {/* No result, show empty state */}
      {!result && (
        <div className="glass-card p-6 text-center">
          <p className="text-[#94A3B8] text-sm">
            Upload clear photos of your handwritten notes for Level {levelNum}.
            Your notes will be analyzed for handwriting authenticity and content coverage.
          </p>
        </div>
      )}
    </div>
  );
}
