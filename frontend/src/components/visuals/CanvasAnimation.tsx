'use client';

import { useEffect, useRef, useState } from 'react';

interface CanvasAnimationProps {
  type: 'tcp-handshake' | 'request-flow' | 'xss-attack';
  title?: string;
}

const animations: Record<string, (ctx: CanvasRenderingContext2D, w: number, h: number, frame: number) => void> = {
  'tcp-handshake': (ctx, w, h, frame) => {
    ctx.clearRect(0, 0, w, h);
    const progress = Math.min(frame / 120, 1);
    const phase = Math.floor(progress * 3);
    const t = (progress * 3) - phase;

    const clientX = 120, serverX = w - 120;
    const clientY1 = 100, serverY1 = 100;
    const clientY2 = 150, serverY2 = 150;
    const clientY3 = 200, serverY3 = 200;

    ctx.fillStyle = '#3B82F6';
    ctx.beginPath();
    ctx.roundRect(30, 30, 180, 220, 12);
    ctx.fill();
    ctx.fillStyle = 'white';
    ctx.font = 'bold 14px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Client', 120, 80);
    ctx.font = '11px Inter, sans-serif';
    ctx.fillStyle = '#BFDBFE';
    ctx.fillText('Browser', 120, 100);

    ctx.fillStyle = '#10B981';
    ctx.beginPath();
    ctx.roundRect(w - 210, 30, 180, 220, 12);
    ctx.fill();
    ctx.fillStyle = 'white';
    ctx.font = 'bold 14px Inter, sans-serif';
    ctx.fillText('Server', w - 120, 80);
    ctx.font = '11px Inter, sans-serif';
    ctx.fillStyle = '#A7F3D0';
    ctx.fillText('Web Server', w - 120, 100);

    const drawArrow = (x1: number, y1: number, x2: number, y2: number, label: string, color: string, alpha: number) => {
      ctx.strokeStyle = color;
      ctx.lineWidth = 2.5;
      ctx.globalAlpha = alpha;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();
      const angle = Math.atan2(y2 - y1, x2 - x1);
      ctx.beginPath();
      ctx.moveTo(x2, y2);
      ctx.lineTo(x2 - 12 * Math.cos(angle - 0.4), y2 - 12 * Math.sin(angle - 0.4));
      ctx.lineTo(x2 - 12 * Math.cos(angle + 0.4), y2 - 12 * Math.sin(angle + 0.4));
      ctx.closePath();
      ctx.fill();
      ctx.fillStyle = color;
      ctx.font = '12px Inter, sans-serif';
      ctx.globalAlpha = 0.9;
      ctx.fillText(label, (x1 + x2) / 2, (y1 + y2) / 2 - 8);
      ctx.globalAlpha = 1;
    };

    if (phase >= 0 && t > 0) {
      drawArrow(clientX, clientY1, serverX, serverY1, 'SYN', '#3B82F6', phase === 0 ? t : 1);
    }
    if (phase >= 1 && t > 0) {
      drawArrow(serverX, serverY2, clientX, clientY2, 'SYN-ACK', '#F59E0B', phase === 1 ? t : 1);
    }
    if (phase >= 2 && t > 0) {
      drawArrow(clientX, clientY3, serverX, serverY3, 'ACK', '#10B981', phase === 2 ? t : 1);
    }

    if (progress >= 1) {
      ctx.fillStyle = '#1E293B';
      ctx.font = 'bold 13px Inter, sans-serif';
      ctx.globalAlpha = 1;
      ctx.fillText('✓ Connection Established', w / 2, h - 30);
    }
  },

  'request-flow': (ctx, w, h, frame) => {
    ctx.clearRect(0, 0, w, h);
    const progress = Math.min(frame / 150, 1);
    const phases = 6;
    const phase = Math.floor(progress * phases);
    const t = Math.min((progress * phases) - phase, 1);

    const items = [
      { label: 'Type URL', emoji: '🔤', x: 60, y: 60 },
      { label: 'DNS Lookup', emoji: '📞', x: 185, y: 60 },
      { label: 'Connect', emoji: '🔗', x: 310, y: 60 },
      { label: 'Send Request', emoji: '📤', x: 435, y: 60 },
      { label: 'Server Process', emoji: '⚙️', x: 560, y: 60 },
      { label: 'Render Page', emoji: '🖥️', x: 685, y: 60 },
    ];

    for (let i = 0; i < items.length; i++) {
      const isActive = phase >= i;
      ctx.fillStyle = isActive ? (i === phase ? '#3B82F6' : '#10B981') : '#E2E8F0';
      ctx.globalAlpha = isActive ? (i === phase ? 0.7 + 0.3 * Math.sin(frame * 0.1) : 1) : 0.4;
      ctx.beginPath();
      ctx.arc(items[i].x, items[i].y, 22, 0, Math.PI * 2);
      ctx.fill();
      ctx.font = '16px sans-serif';
      ctx.textAlign = 'center';
      ctx.globalAlpha = isActive ? 1 : 0.4;
      ctx.fillText(items[i].emoji, items[i].x, items[i].y + 6);
      ctx.fillStyle = '#1E293B';
      ctx.font = '10px Inter, sans-serif';
      ctx.globalAlpha = isActive ? 0.9 : 0.4;
      ctx.fillText(items[i].label, items[i].x, items[i].y + 50);
    }

    for (let i = 0; i < phase && i < items.length - 1; i++) {
      ctx.strokeStyle = '#10B981';
      ctx.lineWidth = 2;
      ctx.globalAlpha = 0.6;
      ctx.beginPath();
      ctx.moveTo(items[i].x + 22, items[i].y);
      ctx.lineTo(items[i + 1].x - 22, items[i + 1].y);
      ctx.stroke();
    }

    if (phase < items.length) {
      const idx = Math.min(phase, items.length - 2);
      const x1 = items[idx].x + 22;
      const x2 = items[idx + 1].x - 22;
      const y = items[idx].y;
      ctx.strokeStyle = '#3B82F6';
      ctx.lineWidth = 2;
      ctx.globalAlpha = 0.8;
      ctx.beginPath();
      ctx.moveTo(x1, y);
      ctx.lineTo(x1 + (x2 - x1) * t, y);
      ctx.stroke();

      const cx = x1 + (x2 - x1) * t;
      ctx.fillStyle = '#3B82F6';
      ctx.beginPath();
      ctx.arc(cx, y, 4, 0, Math.PI * 2);
      ctx.fill();
    }

    if (progress >= 1) {
      ctx.fillStyle = '#10B981';
      ctx.font = 'bold 14px Inter, sans-serif';
      ctx.globalAlpha = 1;
      ctx.fillText('✅ Page Loaded Successfully', w / 2, h - 30);
    }

    ctx.fillStyle = '#94A3B8';
    ctx.font = '10px Inter, sans-serif';
    ctx.globalAlpha = 0.7;
    ctx.fillText('Animation shows the step-by-step flow of loading a webpage', w / 2, h - 10);
  },

  'xss-attack': (ctx, w, h, frame) => {
    ctx.clearRect(0, 0, w, h);
    const progress = Math.min(frame / 180, 1);
    const phase = Math.floor(progress * 5);
    const t = Math.min((progress * 5) - phase, 1);

    const drawBadge = (x: number, y: number, label: string, color: string, filled: boolean) => {
      ctx.fillStyle = filled ? color : 'white';
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.roundRect(x - 55, y - 18, 110, 36, 8);
      filled ? ctx.fill() : ctx.stroke();
      ctx.fillStyle = filled ? 'white' : color;
      ctx.font = 'bold 12px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(label, x, y + 4);
    };

    drawBadge(100, 50, 'Attacker', '#EF4444', true);
    drawBadge(400, 50, 'Server', '#F59E0B', true);
    drawBadge(700, 50, 'Victim', '#3B82F6', true);

    const drawArrowLabel = (x1: number, y1: number, x2: number, y2: number, label: string, show: boolean) => {
      if (!show) return;
      ctx.strokeStyle = '#94A3B8';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();
      ctx.fillStyle = '#64748B';
      ctx.font = '10px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(label, (x1 + x2) / 2, ((y1 + y2) / 2) - 8);
    };

    drawArrowLabel(155, 50, 345, 50, 'Injects malicious script', phase >= 1);
    drawArrowLabel(155, 80, 345, 80, 'Stores in database', phase >= 2);
    drawArrowLabel(455, 50, 645, 50, 'Serves page with script', phase >= 3);

    if (phase >= 1) {
      const x = 100 + t * 245;
      ctx.fillStyle = '#EF4444';
      ctx.beginPath();
      ctx.arc(x, 50, 4, 0, Math.PI * 2);
      ctx.fill();
    }

    if (phase >= 3) {
      const x = 460 + t * 185;
      ctx.fillStyle = '#F59E0B';
      ctx.beginPath();
      ctx.arc(x, 50, 4, 0, Math.PI * 2);
      ctx.fill();
    }

    if (phase >= 4) {
      ctx.setLineDash([4, 3]);
      ctx.strokeStyle = '#EF4444';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(700, 70);
      ctx.lineTo(700, 200);
      ctx.lineTo(100, 200);
      ctx.lineTo(100, 70);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = '#EF4444';
      ctx.font = 'bold 11px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('🔥 Cookie & data stolen', 400, 225);
      ctx.fillStyle = '#64748B';
      ctx.font = '10px Inter, sans-serif';
      ctx.fillText('(data exfiltration via JavaScript)', 400, 243);
    }

    if (progress >= 1) {
      ctx.fillStyle = '#EF4444';
      ctx.font = 'bold 13px Inter, sans-serif';
      ctx.fillText('❌ Attack Complete — Victim compromised', w / 2, h - 25);
    } else {
      ctx.fillStyle = '#64748B';
      ctx.font = '10px Inter, sans-serif';
      ctx.fillText(`Phase: ${phase + 1}/5`, w / 2, h - 10);
    }
  },
};

export default function CanvasAnimation({ type, title }: CanvasAnimationProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const frameRef = useRef(0);
  const [isPlaying, setIsPlaying] = useState(true);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    let animId: number;
    const animate = () => {
      if (!isPlaying) {
        if (!animations[type]) return;
        animations[type](ctx, rect.width, rect.height, frameRef.current);
        animId = requestAnimationFrame(animate);
        return;
      }
      frameRef.current = (frameRef.current + 1) % 300;
      if (!animations[type]) return;
      animations[type](ctx, rect.width, rect.height, frameRef.current);
      animId = requestAnimationFrame(animate);
    };
    animate();

    return () => cancelAnimationFrame(animId);
  }, [type, isPlaying]);

  return (
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
      {title && (
        <div className="flex items-center justify-between px-4 py-2 bg-gray-50 border-b border-gray-200">
          <div className="flex items-center gap-2">
            <span className="text-lg">🎬</span>
            <span className="text-xs font-bold text-gray-500 tracking-wider uppercase">{title}</span>
          </div>
          <button
            onClick={() => {
              frameRef.current = 0;
              setIsPlaying(!isPlaying);
            }}
            className="text-xs px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium"
          >
            {isPlaying ? 'Pause' : 'Play'}
          </button>
        </div>
      )}
      <canvas
        ref={canvasRef}
        className="w-full"
        style={{ height: '280px', minHeight: '280px' }}
      />
    </div>
  );
}
