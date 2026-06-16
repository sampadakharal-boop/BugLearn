'use client';

import { useEffect, useRef } from 'react';

interface MermaidDiagramProps {
  chart: string;
  title?: string;
}

export default function MermaidDiagram({ chart, title }: MermaidDiagramProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const render = async () => {
      if (!containerRef.current) return;
      try {
        const mermaid = (await import('mermaid')).default;
        mermaid.initialize({
          startOnLoad: false,
          theme: 'base',
          themeVariables: {
            background: '#ffffff',
            primaryColor: '#3B82F6',
            primaryBorderColor: '#2563EB',
            primaryTextColor: '#1E293B',
            lineColor: '#94A3B8',
            secondaryColor: '#F0F9FF',
            tertiaryColor: '#F8FAFC',
            fontSize: '14px',
          },
          flowchart: { useMaxWidth: true, htmlLabels: true },
          sequence: { showSequenceNumbers: true },
        });
        containerRef.current.innerHTML = '';
        const { svg } = await mermaid.render('mermaid-' + Math.random().toString(36).slice(2), chart);
        containerRef.current.innerHTML = svg;
      } catch (e) {
        if (containerRef.current) {
          containerRef.current.innerHTML = `<div class="p-4 text-red-500 text-sm border border-red-200 rounded-lg bg-red-50">Failed to render diagram.</div>`;
        }
      }
    };
    render();
  }, [chart]);

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-5 overflow-x-auto">
      {title && (
        <div className="flex items-center gap-2 mb-4">
          <span className="text-lg">📊</span>
          <span className="text-xs font-bold text-gray-500 tracking-wider uppercase">{title}</span>
        </div>
      )}
      <div ref={containerRef} className="flex justify-center" />
    </div>
  );
}
