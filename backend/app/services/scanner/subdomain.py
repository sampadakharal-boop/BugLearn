import asyncio
import aiohttp
import dns.resolver
from typing import Optional


class SubdomainScanner:
    def __init__(self):
        self.common_subdomains = [
            "www", "mail", "remote", "blog", "webmail", "server", "ns1", "ns2",
            "smtp", "secure", "vpn", "api", "dev", "test", "admin", "portal",
            "cdn", "static", "img", "assets", "app", "mobile", "m", "shop",
            "support", "help", "forum", "community", "docs", "status", "status",
            "staging", "demo", "beta", "release", "stage", "prod", "production",
            "internal", "jenkins", "gitlab", "jira", "confluence", "wiki",
            "dashboard", "console", "manager", "monitor", "monitoring", "logs",
            "analytics", "tracking", "metrics", "stats", "graphql",
            "auth", "login", "signup", "register", "account", "accounts",
            "billing", "payment", "checkout", "orders", "cart",
            "ws", "wss", "socket", "stream", "media", "uploads", "files",
            "backup", "backups", "db", "database", "mysql", "postgres",
            "redis", "kibana", "elastic", "elasticsearch", "logstash",
            "grafana", "prometheus", "alertmanager", "thanos",
            "s3", "storage", "object", "bucket", "assets",
            "firewall", "proxy", "gateway", "router", "switch",
            "ldap", "radius", "vpn", "wireguard", "openvpn",
            "chat", "discourse", "mattermost", "slack", "teams",
            "calendar", "mail", "exchange", "outlook", "owa",
            "webapp", "service", "services", "microservices",
            "api-gateway", "api-gw", "gw", "edge",
            "cdn", "cloudfront", "cloud", "aws", "azure", "gcp",
            "sandbox", "playground", "lab", "labs",
            "corp", "corporate", "enterprise", "partner", "partners",
            "vendor", "vendors", "supplier", "suppliers",
            "recruit", "careers", "jobs", "apply", "talent",
            "newsletter", "notify", "notification", "notifications",
            "webhook", "webhooks", "callback", "callbacks",
        ]

    async def scan(self, domain: str) -> dict:
        subdomains = set()
        resolver = dns.resolver.Resolver()
        resolver.timeout = 3
        resolver.lifetime = 5

        tasks = [self._check_subdomain(domain, sub, resolver) for sub in self.common_subdomains]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if result and isinstance(result, str):
                subdomains.add(result)

        subdomains_dict = []
        for sub in sorted(subdomains):
            try:
                ips = []
                try:
                    answers = resolver.resolve(sub, "A")
                    ips = [str(r) for r in answers]
                except Exception:
                    pass
                subdomains_dict.append({
                    "subdomain": sub,
                    "domain": domain,
                    "ip_addresses": ips,
                    "source": "dns_bruteforce",
                })
            except Exception:
                pass

        return {
            "subdomains": subdomains_dict,
            "count": len(subdomains_dict),
            "domain": domain,
        }

    async def _check_subdomain(self, domain: str, subdomain: str, resolver) -> Optional[str]:
        fqdn = f"{subdomain}.{domain}"
        try:
            answers = resolver.resolve(fqdn, "A")
            if answers:
                return fqdn
        except Exception:
            pass

        try:
            answers = resolver.resolve(fqdn, "AAAA")
            if answers:
                return fqdn
        except Exception:
            pass

        try:
            answers = resolver.resolve(fqdn, "CNAME")
            if answers:
                return fqdn
        except Exception:
            pass

        return None
