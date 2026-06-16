'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { api } from '@/lib/api';

const levels = [
  { num: 1, title: 'Internet Basics', emoji: '🌐', desc: 'How the Internet works — packets, IPs, DNS, and the client-server model' },
  { num: 2, title: 'Web Fundamentals', emoji: '📄', desc: 'HTML structure, CSS styling, JavaScript behavior, browser rendering' },
  { num: 3, title: 'Networking Basics', emoji: '📡', desc: 'TCP/IP, ports, firewalls, OSI model, and network-layer attacks' },
  { num: 4, title: 'HTTP Deep Dive', emoji: '📮', desc: 'Methods, headers, status codes, request smuggling' },
  { num: 5, title: 'Browser Security Model', emoji: '🚧', desc: 'SOP, CORS, CSP, iframe sandboxing, clickjacking' },
  { num: 6, title: 'Bug Bounty Introduction', emoji: '💰', desc: 'Platforms, ethics, legal boundaries, hunter mindset' },
  { num: 7, title: 'Reconnaissance Basics', emoji: '🔍', desc: 'Passive vs active recon, Google dorking, Wayback Machine, WHOIS' },
  { num: 8, title: 'DNS & Subdomain Enumeration', emoji: '📡', desc: 'DNS records, crt.sh, brute-forcing, subdomain takeover' },
  { num: 9, title: 'Asset Discovery', emoji: '🏢', desc: 'Company domains, tech stack detection, hidden endpoints, cloud assets' },
  { num: 10, title: 'Web Application Mapping', emoji: '🗺️', desc: 'URL structure, API discovery, auth flow mapping, state changes' },
  { num: 11, title: 'Recon Automation', emoji: '🤖', desc: 'Recon pipelines, ffuf, webhooks, bash scripting' },
  { num: 12, title: 'Hacker Thinking', emoji: '💭', desc: 'Hacker mindset, prioritization, edge cases, negative testing' },
  { num: 13, title: 'Authentication Systems', emoji: '🔓', desc: 'Auth flaws, password reset, MFA bypass, OAuth security' },
  { num: 14, title: 'Session Management', emoji: '🍪', desc: 'Cookies, JWT attacks, session hijacking, SameSite' },
  { num: 15, title: 'IDOR & Access Control', emoji: '🔓', desc: 'Insecure Direct Object Reference, mass assignment, blind IDOR' },
  { num: 16, title: 'Privilege Escalation', emoji: '📈', desc: 'Vertical/horizontal escalation, admin panels, role manipulation' },
  { num: 17, title: 'Cross-Site Scripting', emoji: '📜', desc: 'Reflected, stored, DOM-based XSS, context-aware payloads' },
  { num: 18, title: 'SQL Injection', emoji: '💉', desc: 'Union, error-based, blind SQLi, sqlmap automation' },
  { num: 19, title: 'CSRF Attacks', emoji: '🎣', desc: 'Cross-site request forgery, SameSite bypasses, token analysis' },
  { num: 20, title: 'File Upload Vulnerabilities', emoji: '📎', desc: 'RCE via uploads, type bypass, SVG XSS, Zip Slip' },
  { num: 21, title: 'Path Traversal / LFI', emoji: '📂', desc: 'Directory traversal, LFI to RCE, PHP wrappers, log poisoning' },
  { num: 22, title: 'SSRF', emoji: '🔄', desc: 'Server-Side Request Forgery, cloud metadata, blind SSRF' },
  { num: 23, title: 'Command Injection', emoji: '💻', desc: 'OS command injection, blind detection, obfuscation' },
  { num: 24, title: 'API Security Testing', emoji: '🔀', desc: 'REST, GraphQL, OWASP API Top 10, mass assignment' },
  { num: 25, title: 'Business Logic Bugs', emoji: '🧠', desc: 'Race conditions, workflow bypass, pricing flaws' },
  { num: 26, title: 'Advanced Recon', emoji: '🔍', desc: 'GitHub dorking, acquisition recon, CDN bypass, frameworks' },
  { num: 27, title: 'Vulnerability Chaining', emoji: '⛓️', desc: 'Combining bugs for critical impact, chain reporting' },
  { num: 28, title: 'Bug Bounty Case Studies', emoji: '📋', desc: 'HackerOne reports, Capital One breach, Twitter OAuth chain' },
  { num: 29, title: 'Report Writing', emoji: '📝', desc: 'Perfect reports, impact communication, handling rejections' },
  { num: 30, title: 'Final Capstone', emoji: '🎯', desc: 'Full simulated engagement + final AI interview assessment' },
];

export default function LandingPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    setIsLoggedIn(!!api.token);
  }, []);

  if (!mounted) {
    return (
      <div className="min-h-screen bg-[#0B1220] flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-[#3B82F6] border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0B1220]">
      <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0B1220]/80 backdrop-blur-xl border-b border-[#1E293B]">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#f59e0b] to-[#ef4444] flex items-center justify-center text-white font-bold text-sm">B</div>
            <span className="text-[#F8FAFC] font-bold">Bug<span className="text-[#f59e0b]">Learn</span></span>
          </div>
          <div className="flex items-center gap-4">
            {isLoggedIn ? (
              <Link href="/dashboard" className="btn-primary text-sm">Dashboard</Link>
            ) : (
              <>
                <Link href="/login" className="text-[#94A3B8] hover:text-[#F8FAFC] transition-colors text-sm">Sign In</Link>
                <Link href="/register" className="btn-primary text-sm">Start Learning</Link>
              </>
            )}
          </div>
        </div>
      </nav>

      <section className="relative pt-32 pb-20 px-6 overflow-hidden">
        <div className="absolute inset-0 bg-grid opacity-50" />
        <div className="absolute top-1/4 -left-32 w-96 h-96 bg-[#f59e0b]/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 -right-32 w-96 h-96 bg-[#ef4444]/10 rounded-full blur-3xl" />

        {/* Floating cybersecurity particles */}
        <div className="absolute inset-0 pointer-events-none overflow-hidden">
          <span className="absolute top-[15%] left-[10%] text-xl opacity-20 animate-particle" style={{animationDelay: '0s'}}>🛡️</span>
          <span className="absolute top-[25%] right-[15%] text-lg opacity-15 animate-particle" style={{animationDelay: '1.5s'}}>🔐</span>
          <span className="absolute top-[60%] left-[8%] text-2xl opacity-10 animate-particle" style={{animationDelay: '3s'}}>🌐</span>
          <span className="absolute top-[70%] right-[12%] text-xl opacity-15 animate-particle" style={{animationDelay: '0.8s'}}>⚡</span>
          <span className="absolute top-[40%] left-[5%] text-lg opacity-10 animate-particle" style={{animationDelay: '2.2s'}}>🔍</span>
          <span className="absolute top-[50%] right-[8%] text-xl opacity-12 animate-particle" style={{animationDelay: '4s'}}>💻</span>
        </div>

        <div className="max-w-5xl mx-auto text-center relative">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[#f59e0b]/10 border border-[#f59e0b]/20 text-[#f59e0b] text-sm mb-8">
            <span className="w-2 h-2 rounded-full bg-[#f59e0b] animate-pulse" />
            The world's first AI-driven Bug Bounty Learning Academy
          </div>

          <h1 className="mb-6">
            <div className={`text-4xl sm:text-5xl md:text-7xl font-extrabold leading-tight ${mounted ? 'animate-slide-up opacity-0' : ''}`}
              style={mounted ? {animationDelay: '0.1s', animationFillMode: 'forwards'} : {}}>
              Master Bug Bounty
            </div>
            <div className={`text-3xl sm:text-4xl md:text-6xl font-bold leading-tight mt-2 ${mounted ? 'animate-slide-up opacity-0' : ''}`}
              style={mounted ? {animationDelay: '0.3s', animationFillMode: 'forwards'} : {}}>
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-[#f59e0b] via-[#eab308] to-[#ef4444] tracking-tight">
                One Level at a Time
              </span>
            </div>
          </h1>

          <div className={`max-w-3xl mx-auto mb-12 ${mounted ? 'animate-slide-up opacity-0' : ''}`}
            style={mounted ? {animationDelay: '0.45s', animationFillMode: 'forwards'} : {}}>
            <p className="text-xl sm:text-2xl md:text-3xl font-semibold text-[#22D3EE] leading-snug">
              Make your notes ready and let's begin the journey from learner to bug hunter.
            </p>
          </div>

          <div className="flex items-center justify-center gap-4 flex-wrap mb-6">
            {isLoggedIn ? (
              <Link href="/dashboard" className="btn-primary text-lg px-8 py-3">Continue Learning</Link>
            ) : (
              <Link href="/register" className="btn-primary text-lg px-8 py-3">Start Your Journey</Link>
            )}
            <a href="#curriculum" className="btn-secondary text-lg px-8 py-3">View Curriculum</a>
          </div>

          <div className={`max-w-5xl mx-auto mt-12 pt-8 border-t border-[#1E293B]/60 ${mounted ? 'animate-fade-in opacity-0' : ''}`}
            style={mounted ? {animationDelay: '0.9s', animationFillMode: 'forwards'} : {}}>
            <div className="text-center mb-5">
              <h2 className="text-sm font-semibold text-[#64748b] tracking-widest uppercase">
                Why Bug<span className="text-[#94A3B8]">Learn</span>?
              </h2>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
              {[
                { icon: '🎯', title: 'One Level at a Time', desc: 'Progressive skill development — master each step before unlocking the next.' },
                { icon: '🌱', title: 'Beginner-Friendly', desc: 'No prior experience needed. Start from basics and grow into a bug hunter.' },
                { icon: '🎤', title: 'AI-Powered Interviews', desc: 'Voice-based AI interviews test real understanding, not memorization.' },
                { icon: '🔬', title: 'Interactive Learning', desc: 'Diagrams, animations, and tasks ensure you truly understand each topic.' },
                { icon: '📓', title: 'Built-in Notes System', desc: 'Handwrite notes for every level. Build a personal knowledge base.' },
                { icon: '📱', title: 'Mobile-Friendly Access', desc: 'Upload from your phone. Revise anytime, anywhere.' },
              ].map((feature, i) => (
                <div key={i} className={`group flex items-start gap-2.5 p-3 rounded-lg transition-all duration-300 ${mounted ? 'animate-fade-in opacity-0' : ''}`}
                  style={mounted ? {animationDelay: `${1.0 + i * 0.08}s`, animationFillMode: 'forwards'} : {}}>
                  <span className="text-base mt-0.5 shrink-0 opacity-70 group-hover:opacity-100 transition-opacity">{feature.icon}</span>
                  <div>
                    <h3 className="text-xs font-medium text-[#94A3B8] group-hover:text-[#CBD5E1] transition-colors">{feature.title}</h3>
                    <p className="text-[11px] text-[#64748b] mt-0.5 leading-relaxed group-hover:text-[#94A3B8] transition-colors">{feature.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="py-12 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="glass-card p-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {[
                { value: '30', label: 'Learning Levels', suffix: 'progressive' },
                { value: '86', label: 'Pass Score', suffix: 'or higher' },
                { value: '100%', label: 'Voice-Based', suffix: 'AI interviews' },
                
              ].map((stat) => (
                <div key={stat.label} className="text-center">
                  <div className="text-3xl md:text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[#f59e0b] to-[#ef4444] mb-1">{stat.value}</div>
                  <div className="text-sm text-[#64748b]">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section id="curriculum" className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Your <span className="bg-clip-text text-transparent bg-gradient-to-r from-[#f59e0b] to-[#ef4444]">Learning Path</span></h2>
            <p className="text-lg text-[#94A3B8] max-w-2xl mx-auto">
              Each level unlocks only after you pass the AI Voice Interview Certification.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {levels.map((level) => (
              <div key={level.num} className="glass-card-hover p-6 group cursor-default">
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#f59e0b]/20 to-[#ef4444]/20 border border-[#f59e0b]/20 flex items-center justify-center text-xl">
                    {level.emoji}
                  </div>
                  <span className="text-xs font-mono text-[#64748b]">Level {level.num}</span>
                </div>
                <h3 className="font-semibold text-[#F8FAFC] mb-1">{level.title}</h3>
                <p className="text-[#94A3B8] text-sm">{level.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="glass-card p-10 glow relative overflow-hidden">
            <div className="absolute top-0 right-0 w-64 h-64 bg-[#f59e0b]/5 rounded-full blur-3xl" />
            <div className="absolute bottom-0 left-0 w-64 h-64 bg-[#ef4444]/5 rounded-full blur-3xl" />
            <div className="relative text-center">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                Ready to Become a{' '}
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-[#f59e0b] to-[#ef4444]">Bug Bounty Hunter</span>?
              </h2>
              <p className="text-lg text-[#94A3B8] mb-8 max-w-2xl mx-auto">
                No overwhelming theory dumps. No skipping ahead. Just structured learning with AI guidance every step of the way.
              </p>
              <div className="flex items-center justify-center gap-4">
                <Link href="/register" className="btn-primary text-lg px-8 py-3">Start Free Learning</Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      <footer className="border-t border-[#1E293B] py-8 px-6">
        <div className="max-w-6xl mx-auto flex items-center justify-between text-sm text-[#64748b]">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded bg-gradient-to-br from-[#f59e0b] to-[#ef4444] flex items-center justify-center text-white font-bold text-xs">B</div>
            <span>BugLearn</span>
          </div>
          <p>ReconForge Learning System — AI-Powered Bug Bounty Education</p>
        </div>
      </footer>
    </div>
  );
}
