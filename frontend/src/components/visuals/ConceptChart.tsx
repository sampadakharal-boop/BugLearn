'use client';

interface ConceptChartProps {
  type: 'vuln-impact' | 'owasp-top10' | 'attack-chain' | 'security-layers';
  title?: string;
}

const charts: Record<string, (id: string) => string> = {
  'vuln-impact': (id) => `<svg viewBox="0 0 720 380" xmlns="http://www.w3.org/2000/svg">
    <rect width="720" height="380" fill="white" rx="8"/>
    <text x="360" y="35" text-anchor="middle" fill="#1E293B" font-size="15" font-weight="bold">Vulnerability Impact & Frequency</text>
    <rect x="60" y="300" width="50" height="40" rx="4" fill="#3B82F6"/>
    <text x="85" y="330" text-anchor="middle" fill="white" font-size="10">XSS</text>
    <rect x="140" y="250" width="50" height="90" rx="4" fill="#EF4444"/>
    <text x="165" y="305" text-anchor="middle" fill="white" font-size="10">SQLi</text>
    <rect x="220" y="280" width="50" height="60" rx="4" fill="#F59E0B"/>
    <text x="245" y="315" text-anchor="middle" fill="white" font-size="10">CSRF</text>
    <rect x="300" y="220" width="50" height="120" rx="4" fill="#8B5CF6"/>
    <text x="325" y="295" text-anchor="middle" fill="white" font-size="10">IDOR</text>
    <rect x="380" y="180" width="50" height="160" rx="4" fill="#10B981"/>
    <text x="405" y="275" text-anchor="middle" fill="white" font-size="10">Auth</text>
    <rect x="460" y="260" width="50" height="80" rx="4" fill="#06B6D4"/>
    <text x="485" y="305" text-anchor="middle" fill="white" font-size="10">SSRF</text>
    <rect x="540" y="200" width="50" height="140" rx="4" fill="#EC4899"/>
    <text x="565" y="285" text-anchor="middle" fill="white" font-size="10">Logic</text>
    <rect x="610" y="320" width="50" height="20" rx="4" fill="#14B8A6"/>
    <text x="635" y="335" text-anchor="middle" fill="white" font-size="10">Other</text>
    <line x1="50" y1="360" x2="680" y2="360" stroke="#CBD5E1" stroke-width="1"/>
    <text x="400" y="378" text-anchor="middle" fill="#94A3B8" font-size="10">Vulnerability Type (sorted by impact)</text>
  </svg>`,

  'owasp-top10': (id) => `<svg viewBox="0 0 720 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="720" height="400" fill="white" rx="8"/>
    <text x="360" y="30" text-anchor="middle" fill="#1E293B" font-size="15" font-weight="bold">OWASP Top 10 — 2021</text>
    <g>
      ${[
        ['A01: Broken Access Control', '70%', '#EF4444'],
        ['A02: Cryptographic Failures', '60%', '#F59E0B'],
        ['A03: Injection', '80%', '#3B82F6'],
        ['A04: Insecure Design', '50%', '#8B5CF6'],
        ['A05: Security Misconfiguration', '65%', '#EC4899'],
        ['A06: Vulnerable Components', '55%', '#06B6D4'],
        ['A07: Auth Failures', '75%', '#10B981'],
        ['A08: Software Integrity', '35%', '#14B8A6'],
        ['A09: Logging & Monitoring', '40%', '#F97316'],
        ['A10: SSRF', '30%', '#6366F1'],
      ].map((item: string[], i) => {
        const [label, pct, color] = item;
        const y = 55 + i * 33;
        const w = parseInt(pct) * 4.8;
        return `
          <text x="15" y="${y + 12}" fill="#475569" font-size="10">${label}</text>
          <rect x="220" y="${y}" width="${w}" height="22" rx="4" fill="${color}" opacity="0.8"/>
          <text x="${225 + w}" y="${y + 15}" fill="#64748B" font-size="9">${pct}</text>
        `;
      }).join('')}
    </g>
  </svg>`,

  'attack-chain': (id) => `<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="300" fill="white" rx="8"/>
    <text x="400" y="30" text-anchor="middle" fill="#1E293B" font-size="15" font-weight="bold">Attack Chain Progression</text>
    ${[
      ['Recon', '#3B82F6'],
      ['Weaponize', '#6366F1'],
      ['Deliver', '#8B5CF6'],
      ['Exploit', '#EF4444'],
      ['Control', '#F59E0B'],
      ['Exfiltrate', '#EC4899'],
    ].map((item: string[], i) => {
      const [label, color] = item;
      const x = 35 + i * 130;
      const w = 110;
      return `
        <rect x="${x}" y="60" width="${w}" height="70" rx="8" fill="${color}" opacity="0.9"/>
        <text x="${x + w/2}" y="100" text-anchor="middle" fill="white" font-size="12" font-weight="bold">${label}</text>
        ${i < 5 ? `<path d="M${x + w},95 L${x + w + 20},95" stroke="#94A3B8" stroke-width="2" marker-end="url(#arrow)"/>` : ''}
      `;
    }).join('')}
    <rect x="35" y="160" width="730" height="100" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <text x="400" y="185" text-anchor="middle" fill="#64748B" font-size="11">Each stage is a detection opportunity for defenders</text>
    ${[
      ['Phase 1', 'Gather intel on target'],
      ['Phase 2', 'Craft exploit payload'],
      ['Phase 3', 'Send payload to victim'],
      ['Phase 4', 'Execute malicious code'],
      ['Phase 5', 'Establish persistence'],
      ['Phase 6', 'Steal valuable data'],
    ].map((item: string[], i) => {
      const [phase, desc] = item;
      const x = 35 + i * 130;
      return `
        <text x="${x + 55}" y="210" text-anchor="middle" fill="#1E293B" font-size="11" font-weight="bold">${phase}</text>
        <text x="${x + 55}" y="230" text-anchor="middle" fill="#64748B" font-size="10">${desc}</text>
      `;
    }).join('')}
  </svg>`,

  'security-layers': (id) => `<svg viewBox="0 0 700 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="700" height="400" fill="white" rx="8"/>
    <text x="350" y="35" text-anchor="middle" fill="#1E293B" font-size="15" font-weight="bold">Defense in Depth — Layered Security</text>
    ${[
      ['Perimeter', 'WAF, Firewall', '#EF4444', 45],
      ['Network', 'VPC, Subnets, ACLs', '#F59E0B', 95],
      ['Application', 'Auth, Validation, CSP', '#3B82F6', 145],
      ['Data', 'Encryption, Access Ctrl', '#8B5CF6', 195],
      ['Endpoint', 'EDR, AV, Hardening', '#10B981', 245],
      ['Human', 'Training, Policies', '#06B6D4', 295],
    ].map((item: (string | number)[]) => {
      const [layer, tech, color, y] = item;
      const yNum = y as number;
      return `
      <rect x="200" y="${yNum}" width="300" height="40" rx="20" fill="${color}" opacity="0.85"/>
      <text x="350" y="${yNum + 25}" text-anchor="middle" fill="white" font-size="13" font-weight="bold">${layer}</text>
      <text x="520" y="${yNum + 25}" fill="#64748B" font-size="11">${tech}</text>
    `;
    }).join('')}
    <text x="350" y="375" text-anchor="middle" fill="#94A3B8" font-size="11">Attackers must bypass ALL layers to succeed</text>
  </svg>`,
};

export default function ConceptChart({ type, title }: ConceptChartProps) {
  const svgContent = charts[type];
  if (!svgContent) return <div className="p-4 text-gray-400 text-sm">Chart not found</div>;

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4 overflow-x-auto">
      {title && (
        <div className="flex items-center gap-2 mb-3">
          <span className="text-lg">📈</span>
          <span className="text-xs font-bold text-gray-500 tracking-wider uppercase">{title}</span>
        </div>
      )}
      <div className="flex justify-center" dangerouslySetInnerHTML={{ __html: svgContent(type) }} />
    </div>
  );
}
