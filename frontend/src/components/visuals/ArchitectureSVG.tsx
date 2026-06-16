'use client';

interface ArchitectureSVGProps {
  type: 'client-server' | 'dns-resolution' | 'request-response' | 'osi-model' | 'three-tier';
  title?: string;
}

const diagrams: Record<string, (id: string) => string> = {
  'client-server': (id) => `<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="client-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#3B82F6;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#2563EB;stop-opacity:1" />
      </linearGradient>
      <linearGradient id="server-grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#10B981;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#059669;stop-opacity:1" />
      </linearGradient>
      <linearGradient id="arrow-grad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:#3B82F6;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#10B981;stop-opacity:1" />
      </linearGradient>
      <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
        <feDropShadow dx="0" dy="2" stdDeviation="4" flood-opacity="0.15" />
      </filter>
    </defs>
    <rect x="50" y="120" width="200" height="160" rx="16" fill="url(#client-grad)" filter="url(#shadow)"/>
    <text x="150" y="185" text-anchor="middle" fill="white" font-size="20" font-weight="bold">Client</text>
    <text x="150" y="210" text-anchor="middle" fill="#BFDBFE" font-size="13">Browser / App</text>
    <text x="150" y="235" text-anchor="middle" fill="#DBEAFE" font-size="11">Requests Data</text>
    <rect x="550" y="120" width="200" height="160" rx="16" fill="url(#server-grad)" filter="url(#shadow)"/>
    <text x="650" y="185" text-anchor="middle" fill="white" font-size="20" font-weight="bold">Server</text>
    <text x="650" y="210" text-anchor="middle" fill="#A7F3D0" font-size="13">Backend / API</text>
    <text x="650" y="235" text-anchor="middle" fill="#D1FAE5" font-size="11">Responds with Data</text>
    <line x1="250" y1="180" x2="550" y2="180" stroke="#94A3B8" stroke-width="2" stroke-dasharray="8,4"/>
    <polygon points="540,174 560,180 540,186" fill="#10B981"/>
    <text x="400" y="170" text-anchor="middle" fill="#10B981" font-size="13" font-weight="600">Request (GET / POST)</text>
    <line x1="550" y1="220" x2="250" y2="220" stroke="#94A3B8" stroke-width="2" stroke-dasharray="8,4"/>
    <polygon points="260,214 240,220 260,226" fill="#3B82F6"/>
    <text x="400" y="260" text-anchor="middle" fill="#3B82F6" font-size="13" font-weight="600">Response (200 / Data)</text>
    <rect x="300" y="50" width="200" height="40" rx="8" fill="#F59E0B" opacity="0.9" filter="url(#shadow)"/>
    <text x="400" y="75" text-anchor="middle" fill="white" font-size="13" font-weight="600">Internet (HTTP/HTTPS)</text>
    <circle cx="400" cy="340" r="8" fill="#EF4444"/>
    <circle cx="400" cy="320" r="6" fill="#F59E0B"/>
    <circle cx="400" cy="305" r="4" fill="#10B981"/>
    <text x="420" y="345" fill="#64748B" font-size="10">Data flows in packets</text>
  </svg>`,

  'dns-resolution': (id) => `<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <filter id="shadow2" x="-5%" y="-5%" width="110%" height="110%">
        <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.12" />
      </filter>
    </defs>
    <rect x="20" y="20" width="140" height="60" rx="10" fill="#3B82F6" filter="url(#shadow2)"/>
    <text x="90" y="55" text-anchor="middle" fill="white" font-size="13" font-weight="bold">Your Browser</text>
    <rect x="220" y="20" width="140" height="60" rx="10" fill="#6366F1" filter="url(#shadow2)"/>
    <text x="290" y="55" text-anchor="middle" fill="white" font-size="13" font-weight="bold">OS Cache</text>
    <rect x="420" y="20" width="140" height="60" rx="10" fill="#8B5CF6" filter="url(#shadow2)"/>
    <text x="490" y="55" text-anchor="middle" fill="white" font-size="13" font-weight="bold">Router Cache</text>
    <rect x="620" y="20" width="160" height="60" rx="10" fill="#F59E0B" filter="url(#shadow2)"/>
    <text x="700" y="55" text-anchor="middle" fill="white" font-size="13" font-weight="bold">ISP DNS Resolver</text>
    <rect x="150" y="140" width="160" height="60" rx="10" fill="#10B981" filter="url(#shadow2)"/>
    <text x="230" y="175" text-anchor="middle" fill="white" font-size="13" font-weight="bold">Root DNS Server</text>
    <rect x="370" y="140" width="160" height="60" rx="10" fill="#14B8A6" filter="url(#shadow2)"/>
    <text x="450" y="175" text-anchor="middle" fill="white" font-size="13" font-weight="bold">.com TLD Server</text>
    <rect x="590" y="140" width="160" height="60" rx="10" fill="#06B6D4" filter="url(#shadow2)"/>
    <text x="670" y="175" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Authoritative</text>
    <text x="670" y="192" text-anchor="middle" fill="#CFFAFE" font-size="11">DNS Server</text>
    <path d="M160,60 L220,60" stroke="#94A3B8" stroke-width="1.5" fill="none" marker-end="url(#arrowBlue)"/>
    <path d="M360,60 L420,60" stroke="#94A3B8" stroke-width="1.5" fill="none"/>
    <path d="M560,60 L620,60" stroke="#94A3B8" stroke-width="1.5" fill="none"/>
    <path d="M700,80 L700,130" stroke="#94A3B8" stroke-width="1.5" fill="none" stroke-dasharray="4,3"/>
    <path d="M700,130 L230,130 L230,140" stroke="#94A3B8" stroke-width="1.5" fill="none" stroke-dasharray="4,3"/>
    <path d="M230,200 L230,210 L450,210 L450,200" stroke="#94A3B8" stroke-width="1.5" fill="none" stroke-dasharray="4,3"/>
    <path d="M450,200 L450,210 L670,210 L670,200" stroke="#94A3B8" stroke-width="1.5" fill="none" stroke-dasharray="4,3"/>
    <path d="M670,140 L670,300 L90,300 L90,80" stroke="#10B981" stroke-width="2" fill="none" stroke-dasharray="6,3"/>
    <polygon points="90,72 84,84 96,84" fill="#10B981"/>
    <circle cx="700" cy="130" r="4" fill="#F59E0B"/>
    <circle cx="230" cy="130" r="4" fill="#F59E0B"/>
    <circle cx="450" cy="210" r="4" fill="#F59E0B"/>
    <text x="650" y="260" fill="#64748B" font-size="10">IP: 142.250.190.46</text>
    <text x="650" y="275" fill="#64748B" font-size="10">Returned back to browser</text>
    <text x="100" y="320" fill="#64748B" font-size="11" font-style="italic">Question: What is google.com?</text>
    <text x="100" y="340" fill="#10B981" font-size="11" font-style="italic">Answer: IP is 142.250.190.46</text>
    <rect x="80" y="360" width="600" height="50" rx="8" fill="#FEF3C7" stroke="#F59E0B" stroke-width="1"/>
    <text x="380" y="382" text-anchor="middle" fill="#92400E" font-size="11">Result: Browser connects to 142.250.190.46:443 and sends HTTP request</text>
    <text x="380" y="398" text-anchor="middle" fill="#92400E" font-size="11">Each level caches the result for faster future lookups!</text>
  </svg>`,

  'request-response': (id) => `<svg viewBox="0 0 800 360" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <filter id="shadow3" x="-5%" y="-5%" width="110%" height="110%">
        <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.1" />
      </filter>
    </defs>
    <rect x="30" y="100" width="160" height="160" rx="12" fill="#EFF6FF" stroke="#3B82F6" stroke-width="2" filter="url(#shadow3)"/>
    <text x="110" y="145" text-anchor="middle" fill="#1E40AF" font-size="14" font-weight="bold">Step 1</text>
    <text x="110" y="165" text-anchor="middle" fill="#1E3A8A" font-size="11">DNS Resolution</text>
    <text x="110" y="195" text-anchor="middle" fill="#64748B" font-size="10">google.com</text>
    <text x="110" y="210" text-anchor="middle" fill="#64748B" font-size="10">→ 142.250.x.x</text>
    <rect x="230" y="100" width="160" height="160" rx="12" fill="#F0FDF4" stroke="#10B981" stroke-width="2" filter="url(#shadow3)"/>
    <text x="310" y="145" text-anchor="middle" fill="#065F46" font-size="14" font-weight="bold">Step 2</text>
    <text x="310" y="165" text-anchor="middle" fill="#064E3B" font-size="11">TCP Connection</text>
    <text x="310" y="195" text-anchor="middle" fill="#64748B" font-size="10">SYN → SYN-ACK</text>
    <text x="310" y="210" text-anchor="middle" fill="#64748B" font-size="10">→ ACK</text>
    <rect x="430" y="100" width="160" height="160" rx="12" fill="#FEF3C7" stroke="#F59E0B" stroke-width="2" filter="url(#shadow3)"/>
    <text x="510" y="145" text-anchor="middle" fill="#92400E" font-size="14" font-weight="bold">Step 3</text>
    <text x="510" y="165" text-anchor="middle" fill="#78350F" font-size="11">TLS Handshake</text>
    <text x="510" y="195" text-anchor="middle" fill="#64748B" font-size="10">Encryption</text>
    <text x="510" y="210" text-anchor="middle" fill="#64748B" font-size="10">Keys Established</text>
    <rect x="630" y="100" width="150" height="160" rx="12" fill="#FDF2F8" stroke="#EC4899" stroke-width="2" filter="url(#shadow3)"/>
    <text x="705" y="145" text-anchor="middle" fill="#9D174D" font-size="14" font-weight="bold">Step 4</text>
    <text x="705" y="165" text-anchor="middle" fill="#831843" font-size="11">HTTP Request</text>
    <text x="705" y="195" text-anchor="middle" fill="#64748B" font-size="10">GET /index.html</text>
    <text x="705" y="210" text-anchor="middle" fill="#64748B" font-size="10">Headers + Body</text>
    <path d="M190,120 L220,120" stroke="#3B82F6" stroke-width="2" marker-end="url(#arrowBlue)"/>
    <path d="M390,140 L420,140" stroke="#10B981" stroke-width="2"/>
    <path d="M590,160 L620,160" stroke="#F59E0B" stroke-width="2"/>
    <text x="400" y="310" text-anchor="middle" fill="#3B82F6" font-size="13" font-weight="600">↓ HTTP flows through the chain ↓</text>
    <rect x="160" y="40" width="500" height="36" rx="8" fill="#1E293B"/>
    <text x="410" y="64" text-anchor="middle" fill="white" font-size="14" font-weight="bold">Full HTTP Request-Response Lifecycle</text>
  </svg>`,

  'osi-model': (id) => `<svg viewBox="0 0 600 460" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="l7" x1="0" y1="0" x2="600" y2="0"><stop offset="0%" stop-color="#3B82F6"/><stop offset="100%" stop-color="#2563EB"/></linearGradient>
      <linearGradient id="l6" x1="0" y1="0" x2="600" y2="0"><stop offset="0%" stop-color="#6366F1"/><stop offset="100%" stop-color="#4F46E5"/></linearGradient>
      <linearGradient id="l5" x1="0" y1="0" x2="600" y2="0"><stop offset="0%" stop-color="#8B5CF6"/><stop offset="100%" stop-color="#7C3AED"/></linearGradient>
      <linearGradient id="l4" x1="0" y1="0" x2="600" y2="0"><stop offset="0%" stop-color="#F59E0B"/><stop offset="100%" stop-color="#D97706"/></linearGradient>
      <linearGradient id="l3" x1="0" y1="0" x2="600" y2="0"><stop offset="0%" stop-color="#10B981"/><stop offset="100%" stop-color="#059669"/></linearGradient>
      <linearGradient id="l2" x1="0" y1="0" x2="600" y2="0"><stop offset="0%" stop-color="#06B6D4"/><stop offset="100%" stop-color="#0891B2"/></linearGradient>
      <linearGradient id="l1" x1="0" y1="0" x2="600" y2="0"><stop offset="0%" stop-color="#EF4444"/><stop offset="100%" stop-color="#DC2626"/></linearGradient>
    </defs>
    <rect x="20" y="10" width="560" height="55" rx="6" fill="url(#l7)"/>
    <text x="100" y="43" fill="white" font-size="13" font-weight="bold">Layer 7: Application</text>
    <text x="350" y="43" fill="#DBEAFE" font-size="11">HTTP, FTP, DNS, SMTP — User-facing protocols</text>
    <rect x="20" y="72" width="560" height="55" rx="6" fill="url(#l6)"/>
    <text x="100" y="105" fill="white" font-size="13" font-weight="bold">Layer 6: Presentation</text>
    <text x="350" y="105" fill="#E0E7FF" font-size="11">Encryption, compression, data formatting</text>
    <rect x="20" y="134" width="560" height="55" rx="6" fill="url(#l5)"/>
    <text x="100" y="167" fill="white" font-size="13" font-weight="bold">Layer 5: Session</text>
    <text x="350" y="167" fill="#EDE9FE" font-size="11">Session management, checkpoints, recovery</text>
    <rect x="20" y="196" width="560" height="55" rx="6" fill="url(#l4)"/>
    <text x="100" y="229" fill="white" font-size="13" font-weight="bold">Layer 4: Transport</text>
    <text x="350" y="229" fill="#FEF3C7" font-size="11">TCP / UDP — Reliable delivery, flow control</text>
    <rect x="20" y="258" width="560" height="55" rx="6" fill="url(#l3)"/>
    <text x="100" y="291" fill="white" font-size="13" font-weight="bold">Layer 3: Network</text>
    <text x="350" y="291" fill="#D1FAE5" font-size="11">IP routing, packet forwarding, addressing</text>
    <rect x="20" y="320" width="560" height="55" rx="6" fill="url(#l2)"/>
    <text x="100" y="353" fill="white" font-size="13" font-weight="bold">Layer 2: Data Link</text>
    <text x="350" y="353" fill="#CFFAFE" font-size="11">MAC addresses, Ethernet, switches, frames</text>
    <rect x="20" y="382" width="560" height="55" rx="6" fill="url(#l1)"/>
    <text x="100" y="415" fill="white" font-size="13" font-weight="bold">Layer 1: Physical</text>
    <text x="350" y="415" fill="#FEE2E2" font-size="11">Cables, radio waves, fiber optics, voltage</text>
    <text x="580" y="430" fill="#94A3B8" font-size="9" text-anchor="end">Data travels DOWN layers to send, UP layers to receive</text>
  </svg>`,

  'three-tier': (id) => `<svg viewBox="0 0 800 360" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <filter id="shadowT"><feDropShadow dx="0" dy="2" stdDeviation="4" flood-opacity="0.12"/></filter>
    </defs>
    <rect x="40" y="100" width="180" height="160" rx="14" fill="#EFF6FF" stroke="#3B82F6" stroke-width="2" filter="url(#shadowT)"/>
    <text x="130" y="145" text-anchor="middle" fill="#1E40AF" font-size="15" font-weight="bold">Presentation</text>
    <text x="130" y="165" text-anchor="middle" fill="#1E3A8A" font-size="11">Tier 1</text>
    <text x="130" y="195" text-anchor="middle" fill="#64748B" font-size="11">React / Next.js</text>
    <text x="130" y="212" text-anchor="middle" fill="#64748B" font-size="11">HTML, CSS, JS</text>
    <text x="130" y="235" text-anchor="middle" fill="#3B82F6" font-size="10">User Interface</text>
    <rect x="310" y="100" width="180" height="160" rx="14" fill="#F0FDF4" stroke="#10B981" stroke-width="2" filter="url(#shadowT)"/>
    <text x="400" y="145" text-anchor="middle" fill="#065F46" font-size="15" font-weight="bold">Application</text>
    <text x="400" y="165" text-anchor="middle" fill="#064E3B" font-size="11">Tier 2</text>
    <text x="400" y="195" text-anchor="middle" fill="#64748B" font-size="11">FastAPI / Python</text>
    <text x="400" y="212" text-anchor="middle" fill="#64748B" font-size="11">Business Logic</text>
    <text x="400" y="235" text-anchor="middle" fill="#10B981" font-size="10">API / Processing</text>
    <rect x="580" y="100" width="180" height="160" rx="14" fill="#FEF3C7" stroke="#F59E0B" stroke-width="2" filter="url(#shadowT)"/>
    <text x="670" y="145" text-anchor="middle" fill="#92400E" font-size="15" font-weight="bold">Database</text>
    <text x="670" y="165" text-anchor="middle" fill="#78350F" font-size="11">Tier 3</text>
    <text x="670" y="195" text-anchor="middle" fill="#64748B" font-size="11">SQLite / PostgreSQL</text>
    <text x="670" y="212" text-anchor="middle" fill="#64748B" font-size="11">Data Storage</text>
    <text x="670" y="235" text-anchor="middle" fill="#F59E0B" font-size="10">Persistence</text>
    <path d="M220,150 L310,150" stroke="#3B82F6" stroke-width="2" stroke-dasharray="8,4"/>
    <polygon points="300,144 316,150 300,156" fill="#3B82F6"/>
    <text x="265" y="140" text-anchor="middle" fill="#3B82F6" font-size="11" font-weight="600">API Calls</text>
    <path d="M490,170 L580,170" stroke="#F59E0B" stroke-width="2" stroke-dasharray="8,4"/>
    <polygon points="570,164 586,170 570,176" fill="#F59E0B"/>
    <text x="535" y="160" text-anchor="middle" fill="#F59E0B" font-size="11" font-weight="600">Queries</text>
    <rect x="240" y="60" width="320" height="30" rx="8" fill="#1E293B"/>
    <text x="400" y="80" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Three-Tier Web Application Architecture</text>
    <text x="400" y="310" text-anchor="middle" fill="#64748B" font-size="11">Each tier is independent and can be scaled separately</text>
  </svg>`,
};

export default function ArchitectureSVG({ type, title }: ArchitectureSVGProps) {
  const svgContent = diagrams[type];
  if (!svgContent) return <div className="p-4 text-gray-400 text-sm">Architecture diagram not found</div>;

  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4 overflow-x-auto">
      {title && (
        <div className="flex items-center gap-2 mb-3">
          <span className="text-lg">🏗️</span>
          <span className="text-xs font-bold text-gray-500 tracking-wider uppercase">{title}</span>
        </div>
      )}
      <div className="flex justify-center" dangerouslySetInnerHTML={{ __html: svgContent(type) }} />
    </div>
  );
}
