import aiohttp
import asyncio
import re
from urllib.parse import urljoin, urlparse


class EndpointDiscoverer:
    def __init__(self):
        self.common_paths = [
            "/", "/robots.txt", "/sitemap.xml", "/sitemap_index.xml",
            "/.well-known/", "/.well-known/security.txt",
            "/.env", "/.git/config", "/.git/HEAD",
            "/admin", "/administrator", "/wp-admin", "/wp-login.php",
            "/api", "/api/v1", "/api/v2", "/api/v3",
            "/graphql", "/graphiql", "/playground",
            "/swagger.json", "/swagger-ui", "/api-docs", "/openapi.json",
            "/health", "/healthz", "/readyz", "/livez",
            "/metrics", "/prometheus", "/actuator",
            "/login", "/logout", "/register", "/signup",
            "/forgot-password", "/reset-password",
            "/dashboard", "/panel", "/console",
            "/static", "/assets", "/uploads", "/files", "/media",
            "/backup", "/backups", "/dump", "/export",
            "/config", "/configuration", "/settings", "/setup",
            "/install", "/installation", "/upgrade", "/migrate",
            "/test", "/tests", "/testing", "/debug",
            "/phpinfo.php", "/info.php", "/status",
            "/server-status", "/server-info",
            "/crossdomain.xml", "/clientaccesspolicy.xml",
            "/web.config", "/.htaccess", "/.htpasswd",
            "/package.json", "/package-lock.json",
            "/yarn.lock", "/requirements.txt",
            "/composer.json", "/Gemfile",
            "/Dockerfile", "/docker-compose.yml",
            "/.env.example", "/.env.local",
            "/README.md", "/CHANGELOG.md",
            "/sockjs-node", "/webpack-dev-server",
            "/actuator/health", "/actuator/info", "/actuator/env",
            "/.well-known/change-password",
            "/.well-known/assetlinks.json",
            "/.well-known/apple-app-site-association",
            "/sitemap.xml.gz", "/robots.txt.bak",
            "/error", "/404", "/500",
            "/proxy", "/proxy.php", "/cgi-bin/",
            "/shell", "/cmd", "/exec",
            "/websocket", "/ws", "/wss",
            "/api/health", "/api/swagger", "/api/graphql",
            "/v1", "/v2", "/v3", "/latest",
            "/internal", "/private", "/secret",
            "/logs", "/log", "/logging",
            "/monitor", "/monitoring", "/check",
            "/callback", "/webhook", "/hooks",
            "/staging", "/beta", "/alpha", "/dev", "/development",
            "/stage", "/prod", "/production",
            "/cdn-cgi", "/cdn-cgi/scripts",
            "/vendor", "/node_modules",
            "/storage", "/tmp", "/temp", "/cache",
            "/docs", "/documentation", "/wiki",
            "/about", "/contact", "/terms", "/privacy",
            "/search", "/search.json", "/opensearch.xml",
            "/rss", "/feed", "/atom.xml",
            "/manifest.json", "/service-worker.js",
            "/sw.js", "/workbox-",
            "/browserconfig.xml",
            "/app-ads.txt", "/ads.txt",
            "/security.txt", "/security",
            "/.vscode", "/.idea", "/.DS_Store",
            "/Thumbs.db", "/desktop.ini",
        ]

        self.api_patterns = [
            r'/api/[\w/-]+',
            r'/v\d+/[\w/-]+',
            r'/graphql',
            r'/rest/[\w/-]+',
            r'/service/[\w/-]+',
            r'/services/[\w/-]+',
            r'/endpoint/[\w/-]+',
            r'/method/[\w/-]+',
            r'/action/[\w/-]+',
            r'/command/[\w/-]+',
            r'/query/[\w/-]+',
            r'/mutate/[\w/-]+',
            r'/subscription/[\w/-]+',
        ]

    async def scan(self, domain: str) -> dict:
        found_endpoints = []
        base_urls = [
            f"https://{domain}",
            f"http://{domain}",
        ]

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            for base_url in base_urls:
                endpoints = await self._check_paths(session, base_url)
                found_endpoints.extend(endpoints)

                robots_content = await self._fetch_url(session, f"{base_url}/robots.txt")
                if robots_content:
                    extracted = self._extract_from_robots(robots_content, base_url)
                    found_endpoints.extend(extracted)

                sitemap_content = await self._fetch_url(session, f"{base_url}/sitemap.xml")
                if sitemap_content:
                    extracted = self._extract_from_sitemap(sitemap_content)
                    found_endpoints.extend(extracted)

                html_content = await self._fetch_url(session, base_url)
                if html_content:
                    extracted = self._extract_from_html(html_content, base_url)
                    found_endpoints.extend(extracted)

        seen = set()
        unique_endpoints = []
        for ep in found_endpoints:
            if ep["url"] not in seen:
                seen.add(ep["url"])
                unique_endpoints.append(ep)

        return {
            "domain": domain,
            "endpoints": unique_endpoints,
            "count": len(unique_endpoints),
        }

    async def _check_paths(self, session: aiohttp.ClientSession, base_url: str) -> list[dict]:
        found = []
        semaphore = asyncio.Semaphore(20)

        async def check_path(path: str) -> Optional[dict]:
            async with semaphore:
                url = urljoin(base_url, path.lstrip("/"))
                try:
                    async with session.get(url, ssl=False, allow_redirects=False) as response:
                        if response.status not in [404, 410]:
                            return {
                                "url": url,
                                "status_code": response.status,
                                "content_type": response.headers.get("Content-Type", ""),
                                "source": "path_bruteforce",
                            }
                except Exception:
                    pass
                return None

        tasks = [check_path(path) for path in self.common_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for r in results:
            if r and isinstance(r, dict):
                found.append(r)

        return found

    async def _fetch_url(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        try:
            async with session.get(url, ssl=False, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
        except Exception:
            pass
        return None

    def _extract_from_robots(self, content: str, base_url: str) -> list[dict]:
        endpoints = []
        for line in content.splitlines():
            if line.lower().startswith(("allow:", "disallow:")):
                path = line.split(":", 1)[1].strip()
                if path and path != "/":
                    endpoints.append({
                        "url": urljoin(base_url, path.lstrip("/")),
                        "status_code": None,
                        "content_type": None,
                        "source": "robots.txt",
                    })
        return endpoints

    def _extract_from_sitemap(self, content: str) -> list[dict]:
        endpoints = []
        for match in re.finditer(r'<loc>(.*?)</loc>', content):
            url = match.group(1).strip()
            if url:
                endpoints.append({
                    "url": url,
                    "status_code": None,
                    "content_type": None,
                    "source": "sitemap.xml",
                })
        return endpoints

    def _extract_from_html(self, content: str, base_url: str) -> list[dict]:
        endpoints = []
        seen_urls = set()

        for pattern in self.api_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                path = match.group(0)
                full_url = urljoin(base_url, path.lstrip("/"))
                if full_url not in seen_urls:
                    seen_urls.add(full_url)
                    endpoints.append({
                        "url": full_url,
                        "status_code": None,
                        "content_type": None,
                        "source": "html_analysis",
                    })

        for match in re.finditer(r'(?:action|href|src|data-url|data-endpoint)\s*=\s*["\'](.*?)["\']', content, re.IGNORECASE):
            url = match.group(1)
            if url.startswith(("http://", "https://", "//", "/")):
                if url.startswith("//"):
                    full_url = f"https:{url}"
                elif url.startswith("/"):
                    full_url = urljoin(base_url, url.lstrip("/"))
                else:
                    full_url = url

                if full_url not in seen_urls and urlparse(full_url).netloc:
                    seen_urls.add(full_url)
                    endpoints.append({
                        "url": full_url,
                        "status_code": None,
                        "content_type": None,
                        "source": "html_analysis",
                    })

        return endpoints
