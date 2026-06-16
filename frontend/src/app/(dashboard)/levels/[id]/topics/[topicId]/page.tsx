'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { getLesson } from '@/lib/lesson-content';
import type { LessonSection } from '@/lib/lesson-content';
import MermaidDiagram from '@/components/visuals/MermaidDiagram';
import ArchitectureSVG from '@/components/visuals/ArchitectureSVG';
import CanvasAnimation from '@/components/visuals/CanvasAnimation';
import ConceptChart from '@/components/visuals/ConceptChart';

export default function LessonPage() {
  const params = useParams();
  const router = useRouter();
  const topicId = params.topicId as string;
  const levelNumber = parseInt(params.id as string);
  const [mounted, setMounted] = useState(false);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, number>>({});
  const [submittedChecks, setSubmittedChecks] = useState<Record<string, boolean>>({});


  useEffect(() => { setMounted(true); }, []);

  const lesson = getLesson(topicId);

  if (!mounted || !lesson) {
    if (!lesson) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <div className="text-6xl mb-4">📚</div>
            <h1 className="text-2xl font-bold text-gray-800 mb-2">Lesson Not Found</h1>
            <p className="text-gray-500 mb-4">This lesson doesn't exist or has been removed.</p>
            <Link href={`/levels/${levelNumber}`} className="text-blue-600 hover:underline">← Back to Level</Link>
          </div>
        </div>
      );
    }
    return <div className="min-h-screen bg-gray-50 flex items-center justify-center"><div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" /></div>;
  }

  const handleKnowledgeCheck = (label: string, selectedIndex: number) => {
    setSelectedAnswers(prev => ({ ...prev, [label]: selectedIndex }));
  };

  const submitKnowledgeCheck = (label: string) => {
    setSubmittedChecks(prev => ({ ...prev, [label]: true }));
  };

  const bgColors = [
    'from-blue-50 to-indigo-50',
    'from-emerald-50 to-teal-50',
    'from-amber-50 to-orange-50',
    'from-rose-50 to-pink-50',
    'from-violet-50 to-purple-50',
    'from-cyan-50 to-sky-50',
    'from-lime-50 to-green-50',
  ];

  const sectionBg = (() => {
    const colors = ['bg-blue-50', 'bg-emerald-50', 'bg-amber-50', 'bg-rose-50', 'bg-violet-50', 'bg-cyan-50'];
    let i = 0;
    return () => {
      const c = colors[i % colors.length];
      i++;
      return c;
    };
  })();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation Bar */}
      <div className="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-4xl mx-auto px-4 h-14 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href={`/levels/${levelNumber}`} className="text-gray-500 hover:text-gray-700 flex items-center gap-1 text-sm">
              <span>←</span>
              <span className="hidden sm:inline">Back to Level {levelNumber}</span>
            </Link>
            <div className="h-4 w-px bg-gray-200" />
            <span className="text-xs text-gray-400 font-mono">Level {levelNumber}</span>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/dashboard" className="text-xs text-gray-400 hover:text-gray-600">
              Dashboard
            </Link>
          </div>
        </div>
      </div>

      {/* White Reading Content */}
      <div className="max-w-3xl mx-auto px-4 py-10">
        {/* Lesson Header */}
        <div className="mb-10">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500/10 to-indigo-500/10 border border-blue-200 flex items-center justify-center text-2xl">
              {lesson.emoji}
            </div>
            <div>
              <span className="text-xs font-mono text-blue-600 bg-blue-50 px-2 py-1 rounded border border-blue-100">LESSON</span>
            </div>
          </div>
          <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 leading-tight">
            {lesson.title}
          </h1>
        </div>

        <div className="space-y-8">
          {lesson.sections.map((section, sIdx) => {
            switch (section.type) {
              case 'heading':
                return (
                  <h2 key={sIdx} className="text-2xl font-bold text-gray-900 pt-4 border-t border-gray-100">
                    {section.content}
                  </h2>
                );

              case 'subheading':
                return (
                  <h3 key={sIdx} className="text-xl font-semibold text-gray-800 mt-2">
                    {section.content}
                  </h3>
                );

              case 'text':
                return (
                  <p key={sIdx} className="text-gray-700 leading-relaxed text-base sm:text-lg">
                    {section.content}
                  </p>
                );

              case 'callout': {
                const variants: Record<string, { bg: string; border: string; icon: string; label: string }> = {
                  info: { bg: 'bg-blue-50', border: 'border-blue-200', icon: 'ℹ️', label: 'INFO' },
                  warning: { bg: 'bg-amber-50', border: 'border-amber-200', icon: '⚠️', label: 'WARNING' },
                  tip: { bg: 'bg-emerald-50', border: 'border-emerald-200', icon: '💡', label: 'TIP' },
                  example: { bg: 'bg-violet-50', border: 'border-violet-200', icon: '🔍', label: 'EXAMPLE' },
                  definition: { bg: 'bg-cyan-50', border: 'border-cyan-200', icon: '📖', label: 'DEFINITION' },
                };
                const v = variants[section.variant || 'info'];
                return (
                  <div key={sIdx} className={`${v.bg} ${v.border} border rounded-xl p-5`}>
                    <div className="flex items-center gap-2 mb-2">
                      <span>{v.icon}</span>
                      <span className="text-xs font-bold text-gray-500 tracking-wider">{v.label}</span>
                    </div>
                    <div className="text-gray-800 text-sm sm:text-base leading-relaxed">
                      {section.content?.split('\n').map((line, li) => {
                        const trimmed = line.trim();
                        if (trimmed.startsWith('**') && trimmed.endsWith('**')) {
                          return <p key={li} className="font-bold mb-1">{trimmed.replace(/\*\*/g, '')}</p>;
                        }
                        return <p key={li} className="mb-1">{trimmed}</p>;
                      })}
                    </div>
                  </div>
                );
              }

              case 'analogy': {
                return (
                  <div key={sIdx} className="bg-gradient-to-br from-amber-50 to-orange-50 border border-amber-200 rounded-xl p-5">
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-lg">🤔</span>
                      <span className="text-xs font-bold text-amber-700 tracking-wider">ANALOGY</span>
                    </div>
                    <p className="text-gray-800 text-sm sm:text-base leading-relaxed">
                      {section.content}
                    </p>
                    {section.items && (
                      <ul className="mt-3 space-y-1">
                        {section.items.map((item, ii) => (
                          <li key={ii} className="text-sm text-gray-600 flex items-start gap-2">
                            <span className="text-amber-500 mt-1">•</span> {item}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                );
              }

              case 'table': {
                return (
                  <div key={sIdx} className="overflow-x-auto rounded-xl border border-gray-200">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="bg-gray-50 border-b border-gray-200">
                          {section.headers?.map((h, hi) => (
                            <th key={hi} className="px-4 py-3 text-left font-semibold text-gray-700 whitespace-nowrap">{h}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-100">
                        {section.rows?.map((row, ri) => (
                          <tr key={ri} className={ri % 2 === 0 ? 'bg-white' : 'bg-gray-50/50'}>
                            {row.map((cell, ci) => (
                              <td key={ci} className={`px-4 py-3 text-gray-700 ${ci === 0 ? 'font-medium text-gray-900' : ''}`}>
                                {cell}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                );
              }

              case 'code': {
                return (
                  <div key={sIdx} className="bg-gray-900 rounded-xl overflow-hidden">
                    <div className="flex items-center justify-between px-4 py-2 bg-gray-800 border-b border-gray-700">
                      <span className="text-xs text-gray-400 font-mono">code</span>
                    </div>
                    <pre className="p-4 text-sm text-gray-100 font-mono leading-relaxed overflow-x-auto whitespace-pre-wrap">
                      {section.content}
                    </pre>
                  </div>
                );
              }

              case 'list': {
                return (
                  <ul key={sIdx} className="space-y-3">
                    {section.items?.map((item, li) => {
                      const isOrdered = item.match(/^\*\*Step \d+/) || item.match(/^\*\*Phase \d+/);
                      const prefix = isOrdered ? '🔹' : '•';
                      return (
                        <li key={li} className="text-gray-700 text-sm sm:text-base leading-relaxed flex items-start gap-2">
                          <span className="text-blue-500 mt-1 flex-shrink-0">{prefix}</span>
                          <span dangerouslySetInnerHTML={{
                            __html: item
                              .replace(/\*\*(.*?)\*\*/g, '<strong class="text-gray-900">$1</strong>')
                              .replace(/`(.*?)`/g, '<code class="bg-gray-100 text-red-600 px-1 rounded text-xs font-mono">$1</code>')
                          }} />
                        </li>
                      );
                    })}
                  </ul>
                );
              }

              case 'knowledge-check': {
                const label = section.label || `kc-${sIdx}`;
                const selected = selectedAnswers[label];
                const submitted = submittedChecks[label];
                const isCorrect = selected === 0;

                return (
                  <div key={sIdx} className="bg-indigo-50 border border-indigo-200 rounded-xl p-5">
                    <div className="flex items-center gap-2 mb-4">
                      <span className="text-lg">✏️</span>
                      <span className="text-xs font-bold text-indigo-600 tracking-wider">KNOWLEDGE CHECK</span>
                    </div>
                    <p className="text-gray-800 font-medium mb-4">{section.content}</p>
                    <div className="space-y-2">
                      {section.items?.map((opt, oi) => {
                        let btnClass = 'bg-white border-gray-200 hover:bg-indigo-50 hover:border-indigo-300 text-gray-700';
                        if (submitted) {
                          if (oi === 0) btnClass = 'bg-emerald-50 border-emerald-400 text-emerald-700';
                          else if (oi === selected) btnClass = 'bg-rose-50 border-rose-300 text-rose-700';
                          else btnClass = 'bg-gray-50 border-gray-200 text-gray-400';
                        } else if (selected === oi) {
                          btnClass = 'bg-indigo-100 border-indigo-400 text-indigo-700';
                        }
                        return (
                          <button
                            key={oi}
                            onClick={() => !submitted && handleKnowledgeCheck(label, oi)}
                            className={`w-full text-left px-4 py-3 rounded-lg border text-sm transition-all ${btnClass} ${submitted ? 'cursor-default' : 'cursor-pointer'}`}
                          >
                            <span className="font-mono mr-2 text-xs text-gray-400">{String.fromCharCode(65 + oi)}</span>
                            {opt}
                          </button>
                        );
                      })}
                    </div>
                    {!submitted && selected !== undefined && (
                      <button
                        onClick={() => submitKnowledgeCheck(label)}
                        className="mt-3 px-4 py-2 bg-indigo-600 text-white text-sm rounded-lg hover:bg-indigo-700 transition-colors"
                      >
                        Check Answer
                      </button>
                    )}
                    {submitted && (
                      <div className={`mt-3 px-4 py-2 rounded-lg text-sm ${isCorrect ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'}`}>
                        {isCorrect ? '✅ Correct!' : '❌ Not quite. The correct answer is A.'}
                      </div>
                    )}
                  </div>
                );
              }

              case 'mermaid':
                return <MermaidDiagram key={sIdx} chart={section.content || ''} title={section.chartType} />;

              case 'architecture-svg':
                return <ArchitectureSVG key={sIdx} type={(section.svgType || 'client-server') as any} title={section.content} />;

              case 'canvas-animation':
                return <CanvasAnimation key={sIdx} type={(section.animationType || 'request-flow') as any} title={section.content} />;

              case 'concept-chart':
                return <ConceptChart key={sIdx} type={(section.chartType || 'owasp-top10') as any} title={section.content} />;

              default:
                return null;
            }
          })}
        </div>

        {/* Bottom Navigation */}
        <div className="mt-12 pt-8 border-t border-gray-200 flex items-center justify-between">
          <Link href={`/levels/${levelNumber}`} className="text-blue-600 hover:text-blue-700 text-sm flex items-center gap-1">
            <span>←</span> Back to Level {levelNumber}
          </Link>
          <Link href="/dashboard" className="text-gray-400 hover:text-gray-600 text-sm">
            Dashboard
          </Link>
        </div>
      </div>


    </div>
  );
}
