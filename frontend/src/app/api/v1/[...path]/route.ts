import { NextRequest, NextResponse } from 'next/server';

const LEVELS: Record<number, any> = {
  1: {
    title: 'Internet Basics',
    subtitle: 'Level 1: How the Internet Works',
    description: 'Understand the global network that powers everything — from packets and protocols to IP addresses and infrastructure.',
    topics: [{name:'What is the Internet?',content:'The internet is a global network of computers connected by cables, satellites, and wireless signals. Data is broken into packets (like letters), addressed with IPs (like postal addresses), and routed through servers (like post offices).',emoji:'🌐'},{name:'IP Addresses & Domain Names',content:'Every device has an IP address (like a phone number). Domain names are human-readable labels (google.com) mapped to IPs via DNS. IPv4 (32-bit) is running out; IPv6 (128-bit) is the future.',emoji:'📟'},{name:'Packets, Routing & ISPs',content:'Data travels in packets that may take different routes. Routers direct traffic. ISPs provide connectivity. Traceroute shows the path packets take — useful for understanding network topology.',emoji:'📦'},{name:'The Client-Server Model',content:'Clients (browsers, apps) request data. Servers store and serve it. One server can handle millions of clients. This model is the foundation of every web interaction.',emoji:'💻'}],
    interview_prompt: 'Explain how a packet travels from your browser to a server and back.',
    key_concepts: ['internet','packet','ip address','dns','client','server','router','isp','protocol','ipv4','ipv6'],
    quiz: [{q:'What does DNS do?',opts:['Sends emails','Translates domains to IPs','Encrypts data','Hosts websites'],ans:1},{q:'What is a packet?',opts:['A network cable','A piece of data sent over a network','A type of server','A security protocol'],ans:1},{q:'In the client-server model, what is a browser?',opts:['Server','Client','Router','ISP'],ans:1}],
    xp_reward: 100
  },
  2: {title:'Web Fundamentals',subtitle:'Level 2: HTML, CSS, JavaScript Basics',description:'Learn the building blocks of every website — structure, style, and behavior.',topics:[{name:'HTML — The Structure',content:'HTML defines page structure using tags.',emoji:'📄'},{name:'CSS — The Styling',content:'CSS controls layout, colors, fonts.',emoji:'🎨'},{name:'JavaScript — The Behavior',content:'JavaScript makes pages interactive.',emoji:'⚡'},{name:'How Browsers Render Pages',content:'HTML → DOM → CSSOM → Render Tree → Paint.',emoji:'🖥️'}],interview_prompt:'Explain the roles of HTML, CSS, and JavaScript.',key_concepts:['html','css','javascript','dom'],quiz:[{q:'What does HTML define?',opts:['Page styling','Page structure','Page behavior','Server logic'],ans:1},{q:'Where does JavaScript run?',opts:['Only on servers','In the browser','Only in databases','On routers'],ans:1},{q:'What tool lets you inspect HTML?',opts:['Text editor','Browser DevTools','Command prompt','Email client'],ans:1}],xp_reward:100},
  3: {title:'Networking Basics',subtitle:'Level 3: How Data Moves Across Networks',description:'Understand TCP/IP, ports, firewalls, and network layers.',topics:[{name:'TCP/IP Protocol Stack',content:'4 layers: Application, Transport, Internet, Link.',emoji:'📚'},{name:'Ports & Services',content:'Ports are numbered doors: 80 (HTTP), 443 (HTTPS), 22 (SSH).',emoji:'🚪'},{name:'Firewalls & Network Segmentation',content:'Firewalls filter traffic based on rules.',emoji:'🛡️'},{name:'The OSI Model Reference',content:'7 layers: Physical to Application.',emoji:'🗂️'}],interview_prompt:'Explain TCP/IP layers and why open ports matter.',key_concepts:['tcp','ip','port','firewall','nmap','osi'],quiz:[{q:'What port does HTTPS use?',opts:['80','443','22','8080'],ans:1},{q:'Which protocol guarantees delivery?',opts:['UDP','TCP','HTTP','DNS'],ans:1},{q:'What tool scans open ports?',opts:['curl','nmap','ping','traceroute'],ans:1}],xp_reward:150},
  4: {title:'HTTP Deep Dive',subtitle:'Level 4: The Language of the Web',description:'Master HTTP — the protocol every bug bounty hunter must know.',topics:[{name:'HTTP Methods & Their Meanings',content:'GET (read), POST (create), PUT (update), DELETE (remove).',emoji:'📮'},{name:'Headers — Request & Response',content:'Request headers: User-Agent, Authorization, Cookie, Content-Type.',emoji:'🧢'},{name:'HTTP Status Codes',content:'2xx success, 3xx redirect, 4xx client error, 5xx server error.',emoji:'🏷️'},{name:'HTTP/1.1 vs HTTP/2 vs HTTP/3',content:'HTTP/1.1 text-based, HTTP/2 binary multiplexed, HTTP/3 over QUIC.',emoji:'⚡'},{name:'Request Smuggling Basics',content:'Exploiting parsing discrepancies between front-end and back-end.',emoji:'🕵️'}],interview_prompt:'Explain HTTP methods, status codes, and security headers.',key_concepts:['http','get','post','header','cookie','csp','smuggling'],quiz:[{q:'Which HTTP method submits form data?',opts:['GET','POST','DELETE','OPTIONS'],ans:1},{q:'What does 403 mean?',opts:['Success','Redirect','Forbidden','Server error'],ans:2},{q:'Which flag makes a cookie JS-inaccessible?',opts:['Secure','HttpOnly','SameSite','Domain'],ans:1}],xp_reward:200},
  5: {title:'Browser Security Model',subtitle:'Level 5: SOP, CORS & Browser Protections',description:'Browser security boundaries and how to find breaks in them.',topics:[{name:'Same-Origin Policy (SOP)',content:"Origin = scheme + host + port. SOP prevents cross-origin reads.",emoji:'🚧'},{name:'Cross-Origin Resource Sharing (CORS)',content:'Access-Control-Allow-Origin headers relax SOP.',emoji:'🔗'},{name:'Content Security Policy (CSP)',content:'Restricts what resources can load — prevents XSS.',emoji:'📜'},{name:'Iframe Sandboxing & Framing Protections',content:'X-Frame-Options and frame-ancestors prevent clickjacking.',emoji:'🖼️'}],interview_prompt:'What is Same-Origin Policy? How can misconfigured CORS be exploited?',key_concepts:['sop','cors','origin','csp','clickjacking'],quiz:[{q:'What three things define an origin?',opts:['Protocol, domain, port','Domain, path, query','IP, MAC, port','User, password, token'],ans:0},{q:'Which header relaxes SOP?',opts:['Set-Cookie','Access-Control-Allow-Origin','X-Frame-Options','Content-Type'],ans:1},{q:'What does CSP protect against?',opts:['SQL injection','XSS','CSRF','SSRF'],ans:1}],xp_reward:200},
};

const TOTAL_LEVELS = Object.keys(LEVELS).length;

const DEMO_USER = { id: 1, name: 'Demo Hunter', email: 'demo@buglearn.com', password: 'demo123', current_level: 1, xp_points: 0, created_at: new Date().toISOString() };

const USERS: Record<string, any> = { 'demo@buglearn.com': { ...DEMO_USER } };

function decodeUser(token: string) {
  try {
    const payload = JSON.parse(Buffer.from(token, 'base64').toString());
    return Object.values(USERS).find((u: any) => u.id === payload.sub);
  } catch { return null; }
}

function getUser(req: NextRequest) {
  const auth = req.headers.get('authorization');
  if (!auth?.startsWith('Bearer ')) return null;
  return decodeUser(auth.slice(7));
}

function match(path: string[], method: string) {
  if (path[0] === 'auth') {
    if (path[1] === 'login' && method === 'POST') return 'auth:login';
    if (path[1] === 'register' && method === 'POST') return 'auth:register';
    if (path[1] === 'me' && method === 'GET') return 'auth:me';
  }
  if (path[0] === 'levels') {
    if (path.length === 1 && method === 'GET') return 'levels:list';
    if (path[1] === 'current' && method === 'GET') return 'levels:current';
    if (path.length === 2 && method === 'GET') return 'levels:get';
    if (path[2] === 'quiz') {
      if (method === 'GET') return 'levels:quiz';
      if (method === 'POST') return 'levels:quiz-submit';
    }
    if (path[2] === 'topics' && path[3]) return 'levels:topic';
  }
  if (path[0] === 'achievements' && method === 'GET') return 'achievements';
  if (path[0] === 'leaderboard' && method === 'GET') return 'leaderboard';
  if (path[0] === 'interview') {
    if (path[1] === 'start' && method === 'POST') return 'interview:start';
    if (path[1] === 'submit' && method === 'POST') return 'interview:submit';
    if (path[1] === 'prompt' && path[2]) return 'interview:prompt';
    if (path[1] === 'history' && method === 'GET') return 'interview:history';
  }
  if (path[0] === 'notes') {
    if (path[1] === 'submit' && method === 'POST') return 'notes:submit';
    if (path[1] === 'status' && path[2]) return 'notes:status';
  }
  return null;
}

export async function GET(req: NextRequest, { params }: { params: { path?: string[] } }) {
  const path = params.path || [];
  const route = match(path, 'GET');
  const user = getUser(req);
  if (!user && !['auth:login', 'auth:register'].includes(route || '')) {
    return NextResponse.json({ detail: 'Not authenticated' }, { status: 401 });
  }

  switch (route) {
    case 'auth:me':
      return NextResponse.json({
        id: user.id, name: user.name, email: user.email,
        current_level: user.current_level, xp_points: user.xp_points,
        created_at: user.created_at,
      });

    case 'levels:list': {
      const results = Object.entries(LEVELS).map(([num, data]) => ({
        level_number: parseInt(num), title: data.title, status: 'in_progress',
        interview_score: null, last_attempt_date: null, xp_reward: data.xp_reward,
      }));
      return NextResponse.json(results);
    }

    case 'levels:current': {
      const levelData = LEVELS[user.current_level];
      return NextResponse.json({
        level_number: user.current_level,
        level_data: levelData,
        progress: { level_number: user.current_level, status: 'in_progress', interview_score: null, last_attempt_date: null },
        total_levels: TOTAL_LEVELS,
      });
    }

    case 'levels:get': {
      const levelNum = parseInt(path[1]);
      const levelData = LEVELS[levelNum];
      if (!levelData) return NextResponse.json({ detail: 'Level not found' }, { status: 404 });
      return NextResponse.json({
        level_number: levelNum, level_data: levelData,
        progress: { level_number: levelNum, status: 'in_progress', interview_score: null, last_attempt_date: null },
        total_levels: TOTAL_LEVELS,
      });
    }

    case 'levels:quiz': {
      const levelNum = parseInt(path[1]);
      const levelData = LEVELS[levelNum];
      if (!levelData) return NextResponse.json({ detail: 'Level not found' }, { status: 404 });
      const safe = levelData.quiz.map((q: any, i: number) => ({ q: q.q, opts: q.opts, id: i }));
      return NextResponse.json({ level_number: levelNum, questions: safe });
    }

    case 'levels:topic': {
      return NextResponse.json({ content: 'Topic content here', emoji: '📖' });
    }

    case 'achievements':
      return NextResponse.json([]);

    case 'leaderboard':
      return NextResponse.json([]);

    case 'interview:prompt': {
      const levelNum = parseInt(path[2]);
      const levelData = LEVELS[levelNum];
      return NextResponse.json({ prompt: levelData?.interview_prompt || 'No prompt available', level_number: levelNum });
    }

    case 'interview:history':
      return NextResponse.json([]);

    case 'notes:status': {
      const levelNum = parseInt(path[2]);
      return NextResponse.json({ has_passed_notes: false, total_attempts: 0, latest_attempt: null });
    }

    default:
      return NextResponse.json({ detail: 'Not found' }, { status: 404 });
  }
}

export async function POST(req: NextRequest, { params }: { params: { path?: string[] } }) {
  const path = params.path || [];
  const route = match(path, 'POST');
  const body = await req.json().catch(() => ({}));

  switch (route) {
    case 'auth:login': {
      const { email, password } = body;
      const u = USERS[email];
      if (!u || u.password !== password) {
        return NextResponse.json({ detail: 'Invalid email or password' }, { status: 401 });
      }
      const token = Buffer.from(JSON.stringify({ sub: u.id, email: u.email })).toString('base64');
      return NextResponse.json({
        access_token: token, token_type: 'bearer',
        user: { id: u.id, name: u.name, email: u.email, current_level: u.current_level, xp_points: u.xp_points, created_at: u.created_at },
      });
    }

    case 'auth:register': {
      const { name, email, password } = body;
      if (USERS[email]) return NextResponse.json({ detail: 'Email already registered' }, { status: 400 });
      const id = Object.keys(USERS).length + 1;
      USERS[email] = { id, name, email, password, current_level: 1, xp_points: 0, created_at: new Date().toISOString() };
      const token = Buffer.from(JSON.stringify({ sub: id, email })).toString('base64');
      return NextResponse.json({
        access_token: token, token_type: 'bearer',
        user: { id, name, email, current_level: 1, xp_points: 0, created_at: USERS[email].created_at },
      });
    }

    case 'levels:quiz-submit': {
      const levelNum = parseInt(path[1]);
      const levelData = LEVELS[levelNum];
      if (!levelData) return NextResponse.json({ detail: 'Level not found' }, { status: 404 });
      const answers = body.answers || [];
      const quiz = levelData.quiz;
      let correct = 0;
      const results = quiz.map((q: any, i: number) => {
        const isCorrect = answers[i] === q.ans;
        if (isCorrect) correct++;
        return { id: i, correct: isCorrect, correct_answer: q.ans };
      });
      const passed = correct >= quiz.length * 0.7;
      return NextResponse.json({ score: correct, total: quiz.length, passed, results });
    }

    case 'interview:start': {
      const interviewId = Date.now();
      return NextResponse.json({ attempt_id: interviewId, questions: ['Question 1', 'Question 2', 'Question 3'] });
    }

    case 'interview:submit': {
      return NextResponse.json({ passed: true, score: 90, feedback: 'Good job!' });
    }

    case 'notes:submit': {
      return NextResponse.json({ id: 1, level_number: parseInt(path[2]) || 1, quality_score: 80, passed: true, pass_threshold: 65, score_breakdown: { concept_coverage: 80, clarity_score: 80, accuracy_score: 80, completeness_score: 80, examples_score: 80 }, matched_concepts: ['internet', 'dns'], missing_concepts: [], weak_areas: [], recommended_lessons: [], flag_spam: false, flag_too_short: false, flag_copied: false, feedback: 'Good notes!', created_at: new Date().toISOString() });
    }

    default:
      return NextResponse.json({ detail: 'Not found' }, { status: 404 });
  }
}
