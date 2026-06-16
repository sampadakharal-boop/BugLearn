import aiohttp
import asyncio
import re
import json
from typing import Optional
from urllib.parse import urljoin, urlparse


class JSAnalyzer:
    def __init__(self):
        self.secret_patterns = [
            {"name": "AWS Access Key", "pattern": r'AKIA[0-9A-Z]{16}', "severity": "critical", "category": "cloud"},
            {"name": "AWS Secret Key", "pattern": r'(?i)aws[_-]?(secret|access)[_-]?key[\s"\'=:]+["\']?([A-Za-z0-9/+=]{40})["\']?', "severity": "critical", "category": "cloud"},
            {"name": "Google API Key", "pattern": r'AIza[0-9A-Za-z\-_]{35}', "severity": "high", "category": "cloud"},
            {"name": "Google OAuth", "pattern": r'[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com', "severity": "high", "category": "cloud"},
            {"name": "Firebase URL", "pattern": r'firebaseio\.com|firestore\.googleapis\.com', "severity": "medium", "category": "cloud"},
            {"name": "Slack Token", "pattern": r'xox[baprs]-[0-9a-zA-Z\-]{10,}', "severity": "high", "category": "communication"},
            {"name": "Slack Webhook", "pattern": r'https://hooks\.slack\.com/services/[A-Za-z0-9/]+', "severity": "high", "category": "communication"},
            {"name": "GitHub Token", "pattern": r'gh[pousr]_[A-Za-z0-9_]{36,}', "severity": "critical", "category": "scm"},
            {"name": "GitHub Classic Token", "pattern": r'[A-Za-z0-9_]{40}', "severity": "high", "category": "scm"},
            {"name": "GitLab Token", "pattern": r'glpat-[A-Za-z0-9\-_]{20,}', "severity": "high", "category": "scm"},
            {"name": "JWT Token", "pattern": r'eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+', "severity": "high", "category": "authentication"},
            {"name": "Stripe Live Key", "pattern": r'(?:sk|pk)_live_[0-9A-Za-z]{24,}', "severity": "critical", "category": "payment"},
            {"name": "Stripe Test Key", "pattern": r'(?:sk|pk)_test_[0-9A-Za-z]{24,}', "severity": "low", "category": "payment"},
            {"name": "PayPal Secret", "pattern": r'access_token\$prod\$[0-9A-Za-z]{16,}', "severity": "critical", "category": "payment"},
            {"name": "Heroku API Key", "pattern": r'[hH][eE][rR][oO][kK][uU].*?[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}', "severity": "high", "category": "cloud"},
            {"name": "Mailgun API Key", "pattern": r'key-[0-9A-Za-z]{32}', "severity": "high", "category": "communication"},
            {"name": "Twilio API Key", "pattern": r'SK[0-9A-Za-z]{32}', "severity": "high", "category": "communication"},
            {"name": "SendGrid API Key", "pattern": r'SG\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+', "severity": "high", "category": "communication"},
            {"name": "MongoDB URI", "pattern": r'mongodb(?:\+srv)?://[A-Za-z0-9_\-:%]+@', "severity": "critical", "category": "database"},
            {"name": "PostgreSQL URI", "pattern": r'postgresql?://[A-Za-z0-9_\-:%]+@', "severity": "critical", "category": "database"},
            {"name": "MySQL URI", "pattern": r'mysql://[A-Za-z0-9_\-:%]+@', "severity": "critical", "category": "database"},
            {"name": "Redis URI", "pattern": r'redis://[A-Za-z0-9_\-:%]+@', "severity": "high", "category": "database"},
            {"name": "Private Key", "pattern": r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----', "severity": "critical", "category": "cryptography"},
            {"name": "Docker Auth", "pattern": r'{"auths":\s*{', "severity": "high", "category": "container"},
            {"name": "npm Token", "pattern": r'npm_[A-Za-z0-9]{36}', "severity": "high", "category": "package"},
            {"name": "SSH Key", "pattern": r'ssh-rsa AAAA[0-9A-Za-z+/]+[=]{0,3}', "severity": "high", "category": "cryptography"},
            {"name": "Password in Variable", "pattern": r'(?:password|passwd|pwd|secret|token)\s*[:=]\s*["\'][^"\']+["\']', "severity": "high", "category": "credentials"},
            {"name": "API Key in Variable", "pattern": r'(?:api[_-]?key|apikey|api_secret)\s*[:=]\s*["\'][^"\']+["\']', "severity": "high", "category": "credentials"},
            {"name": "Slack Bot Token", "pattern": r'xoxb-[0-9A-Za-z\-]{10,}', "severity": "high", "category": "communication"},
            {"name": "Facebook Access Token", "pattern": r'EAACEdEose0cBA[0-9A-Za-z]+', "severity": "high", "category": "social"},
            {"name": "Twitter API Key", "pattern": r'(?:twitter|twtr)[_-]?(?:api|consumer)[_-]?(?:key|secret)\s*[:=]\s*["\'][^"\']+["\']', "severity": "high", "category": "social"},
            {"name": "Azure Connection String", "pattern": r'DefaultEndpointsProtocol=https;AccountName=[A-Za-z0-9]+;AccountKey=[A-Za-z0-9+/=]+', "severity": "critical", "category": "cloud"},
            {"name": "S3 Bucket", "pattern": r'[A-Za-z0-9\-_\.]+\.s3\.amazonaws\.com', "severity": "medium", "category": "cloud"},
            {"name": "S3 Bucket URL", "pattern": r's3://[A-Za-z0-9\-_\.]+', "severity": "medium", "category": "cloud"},
            {"name": "Cloudfront URL", "pattern": r'[A-Za-z0-9]+\.cloudfront\.net', "severity": "low", "category": "cdn"},
            {"name": "SonarQube Token", "pattern": r'sonar[_-]?token\s*[:=]\s*["\'][A-Za-z0-9]+["\']', "severity": "high", "category": "ci"},
            {"name": "Jenkins Token", "pattern": r'jenkins[_-]?token\s*[:=]\s*["\'][A-Za-z0-9]+["\']', "severity": "high", "category": "ci"},
            {"name": "Generic Secret", "pattern": r'(?:secret|token|key|password|passwd|pwd)\s*[:=]\s*["\'][A-Za-z0-9_\-\.!@#$%^&*()]{16,}["\']', "severity": "medium", "category": "credentials"},
        ]

        self.risky_patterns = [
            {"name": "eval() usage", "pattern": r'\beval\s*\('},
            {"name": "document.write()", "pattern": r'document\.write\s*\('},
            {"name": "innerHTML assignment", "pattern": r'\.innerHTML\s*='},
            {"name": "setTimeout with string", "pattern": r'setTimeout\s*\(\s*["\']'},
            {"name": "setInterval with string", "pattern": r'setInterval\s*\(\s*["\']'},
            {"name": "new Function()", "pattern": r'new\s+Function\s*\('},
            {"name": "Function constructor", "pattern": r'Function\s*\(["\']'},
            {"name": "Window location assignment", "pattern": r'window\.location\s*='},
            {"name": "Document cookie access", "pattern": r'document\.cookie'},
            {"name": "localStorage access", "pattern": r'localStorage\.'},
            {"name": "IndexedDB access", "pattern": r'indexedDB\.'},
            {"name": "CORS misconfiguration", "pattern": r'Access-Control-Allow-Origin:\s*\*'},
            {"name": "Insecure WebSocket", "pattern": r'ws://'},
            {"name": "Hardcoded IP address", "pattern": r'(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)'},
            {"name": "Internal hostname", "pattern": r'\.local\b|\.internal\b|10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(1[6-9]|2\d|3[01])\.|192\.168\.'},
            {"name": "Debugger statement", "pattern": r'\bdebugger\b'},
            {"name": "console.log()", "pattern": r'console\.(log|debug|info|warn|error)\s*\('},
            {"name": "SQL-like injection risk", "pattern": r'(?:SELECT|INSERT|UPDATE|DELETE|DROP|CREATE)\s'},
            {"name": "AJAX request to different domain", "pattern": r'\bajax\b.*\burl\b.*https?://'},
            {"name": "XMLHttpRequest", "pattern": r'XMLHttpRequest|new\s+ActiveXObject'},
            {"name": "Fetch API with credentials", "pattern": r'fetch\s*\(.*credentials\s*:\s*["\']include["\']'},
        ]

    async def scan(self, domain: str) -> dict:
        js_files = await self._discover_js_files(domain)
        results = []

        for js_file in js_files:
            content = await self._fetch_js(js_file["url"])
            if content:
                analysis = self._analyze_js(content, js_file["url"])
                results.append(analysis)

        return {
            "domain": domain,
            "js_files": js_files,
            "file_count": len(js_files),
            "analyses": results,
            "total_secrets": sum(r["secrets_count"] for r in results),
            "total_endpoints": sum(r["endpoints_count"] for r in results),
            "total_risky": sum(r["risky_patterns_count"] for r in results),
        }

    async def analyze_url(self, url: str, content: Optional[str] = None) -> dict:
        if content is None:
            content = await self._fetch_content(url)
        if content:
            return self._analyze_js(content, url)
        return {
            "url": url,
            "error": "Could not fetch content",
            "secrets": [],
            "endpoints": [],
            "risky_patterns": [],
            "secrets_count": 0,
            "endpoints_count": 0,
            "risky_patterns_count": 0,
        }

    async def _discover_js_files(self, domain: str) -> list[dict]:
        js_files = []
        base_urls = [f"https://{domain}", f"http://{domain}"]

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
            for base_url in base_urls:
                try:
                    async with session.get(base_url, ssl=False, timeout=10) as response:
                        html = await response.text()
                        for match in re.finditer(r'<script[^>]*src=["\'](.*?)["\']', html, re.IGNORECASE):
                            src = match.group(1)
                            if src.endswith(".js") or "javascript" in src.lower():
                                if src.startswith("//"):
                                    full_url = f"https:{src}"
                                elif src.startswith("/"):
                                    full_url = urljoin(base_url, src.lstrip("/"))
                                elif src.startswith(("http://", "https://")):
                                    full_url = src
                                else:
                                    full_url = urljoin(base_url + "/", src)

                                js_files.append({
                                    "url": full_url,
                                    "source": base_url,
                                    "type": "inline" if "inline" in src else "external",
                                })
                except Exception:
                    continue

        return js_files

    async def _fetch_js(self, url: str) -> Optional[str]:
        return await self._fetch_content(url)

    async def _fetch_content(self, url: str) -> Optional[str]:
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
                async with session.get(url, ssl=False, headers={"Accept": "text/javascript,application/javascript,*/*"}) as response:
                    if response.status == 200:
                        return await response.text()
        except Exception:
            pass
        return None

    def _analyze_js(self, content: str, url: str) -> dict:
        secrets = []
        endpoints = set()
        risky = []

        for pattern_def in self.secret_patterns:
            matches = re.findall(pattern_def["pattern"], content)
            for match in matches:
                if isinstance(match, tuple):
                    match = "".join(match)
                context = self._get_context(content, match)
                secrets.append({
                    "type": pattern_def["name"],
                    "severity": pattern_def["severity"],
                    "category": pattern_def["category"],
                    "match": match[:50] + "..." if len(str(match)) > 50 else match,
                    "context": context,
                    "position": content.find(str(match)) if isinstance(match, str) else -1,
                })

        for match in re.finditer(r'["\'](https?://[^"\']+)["\']', content):
            endpoint = match.group(1)
            if not any(ep in endpoint for ep in [".css", ".png", ".jpg", ".gif", ".ico", ".svg", ".woff", ".eot", ".ttf"]):
                endpoints.add(endpoint)

        for match in re.finditer(r'["\'](/[^"\']+)["\']', content):
            path = match.group(1)
            if path.startswith(("/api/", "/v1/", "/v2/", "/graphql", "/rest/", "/service/")):
                endpoints.add(path)

        for pattern_def in self.risky_patterns:
            matches = re.findall(pattern_def["pattern"], content)
            for match in matches:
                context = self._get_context(content, str(match) if match else pattern_def["pattern"])
                risky.append({
                    "type": pattern_def["name"],
                    "context": context,
                })

        return {
            "url": url,
            "size": len(content),
            "secrets": secrets,
            "endpoints": sorted(list(endpoints)),
            "risky_patterns": risky,
            "secrets_count": len(secrets),
            "endpoints_count": len(endpoints),
            "risky_patterns_count": len(risky),
        }

    def _get_context(self, content: str, match: str, context_chars: int = 60) -> str:
        try:
            idx = content.find(match) if len(match) <= 100 else content.find(match[:50])
            if idx >= 0:
                start = max(0, idx - context_chars)
                end = min(len(content), idx + len(match) + context_chars)
                return content[start:end]
        except Exception:
            pass
        return match[:100]
