import aiohttp
import asyncio
import re
from typing import Optional


class TechScanner:
    def __init__(self):
        self.signatures = [
            {"name": "React", "category": "JavaScript Framework", "regex": r'react(\.min)?\.js|__REACT_DEVTOOLS_GLOBAL_HOOK__|data-reactroot|data-reactid'},
            {"name": "Angular", "category": "JavaScript Framework", "regex": r'angular(\.min)?\.js|ng-app|ng-version|@angular'},
            {"name": "Vue.js", "category": "JavaScript Framework", "regex": r'vue(\.min)?\.js|__VUE_DEVTOOLS_GLOBAL_HOOK__|data-v-|v-bind|v-model|v-if|v-for'},
            {"name": "Next.js", "category": "JavaScript Framework", "regex": r'__NEXT_DATA__|/_next/static|next\.js'},
            {"name": "Nuxt.js", "category": "JavaScript Framework", "regex": r'__NUXT__|_nuxt/'},
            {"name": "Svelte", "category": "JavaScript Framework", "regex": r'svelte(\.min)?\.js|__svelte'},
            {"name": "jQuery", "category": "JavaScript Library", "regex": r'jquery(\.min)?\.js|jQuery'},
            {"name": "Bootstrap", "category": "CSS Framework", "regex": r'bootstrap(\.min)?\.(css|js)|data-bs-'},
            {"name": "Tailwind CSS", "category": "CSS Framework", "regex": r'tailwind(\.min)?\.(css|js)|@tailwind'},
            {"name": "Node.js", "category": "Runtime", "regex": r'node(\.min)?\.js|express'},
            {"name": "Django", "category": "Web Framework", "regex": r'django|csrfmiddlewaretoken|__csrfmagic'},
            {"name": "Flask", "category": "Web Framework", "regex": r'flask|__FLASK__'},
            {"name": "Laravel", "category": "Web Framework", "regex": r'laravel|Laravel|__laravel|Livewire'},
            {"name": "Symfony", "category": "Web Framework", "regex": r'symfony|__SYMFONY__|_sf2_attributes'},
            {"name": "Rails", "category": "Web Framework", "regex": r'rails|ruby\s*on\s*rails|_rails|csrf-param'},
            {"name": "ASP.NET", "category": "Web Framework", "regex": r'__VIEWSTATE|__EVENTVALIDATION|aspnetForm|\.aspx|\.ashx'},
            {"name": "WordPress", "category": "CMS", "regex": r'wp-content|wp-includes|wp-json|wordpress'},
            {"name": "Drupal", "category": "CMS", "regex": r'drupal|Drupal\.settings|Drupal\.ajax'},
            {"name": "Joomla", "category": "CMS", "regex": r'joomla|com_content|com_modules'},
            {"name": "Magento", "category": "CMS", "regex": r'magento|Mage\.|varienForm'},
            {"name": "Shopify", "category": "E-commerce", "regex": r'Shopify\.|shopify\.com|myshopify\.com'},
            {"name": "WooCommerce", "category": "E-commerce", "regex": r'woocommerce|WooCommerce|add-to-cart'},
            {"name": "Nginx", "category": "Web Server", "regex": r'nginx'},
            {"name": "Apache", "category": "Web Server", "regex": r'Apache|\.htaccess'},
            {"name": "IIS", "category": "Web Server", "regex": r'IIS|Microsoft-IIS'},
            {"name": "Cloudflare", "category": "CDN", "regex": r'cloudflare|__cfduid|cf-ray'},
            {"name": "Fastly", "category": "CDN", "regex": r'Fastly|X-Served-By'},
            {"name": "Akamai", "category": "CDN", "regex": r'Akamai|akamai'},
            {"name": "AWS", "category": "Cloud", "regex": r'aws|amazonaws\.com|AWSALB|AWSELB'},
            {"name": "Google Cloud", "category": "Cloud", "regex": r'googleapis\.com|gstatic\.com|cloud\.google'},
            {"name": "Azure", "category": "Cloud", "regex": r'azure\.com|azureedge\.net|azurefd\.net'},
            {"name": "Google Analytics", "category": "Analytics", "regex": r'google-analytics\.com|gtag|ga\.js'},
            {"name": "Hotjar", "category": "Analytics", "regex": r'hotjar\.com|hj\.js'},
            {"name": "Mixpanel", "category": "Analytics", "regex": r'mixpanel\.com|mixpanel'},
            {"name": "Stripe", "category": "Payment", "regex": r'stripe\.com|Stripe\.js|pk_live|pk_test'},
            {"name": "PayPal", "category": "Payment", "regex": r'paypal\.com|paypalobjects\.com'},
            {"name": "Redis", "category": "Cache", "regex": r'redis|CRedis'},
            {"name": "Memcached", "category": "Cache", "regex": r'memcached'},
            {"name": "Varnish", "category": "Cache", "regex": r'varnish|X-Varnish'},
            {"name": "Sentry", "category": "Error Tracking", "regex": r'sentry\.io|Raven\.config|Sentry\.init'},
            {"name": "New Relic", "category": "APM", "regex": r'newrelic\.com|NREUM'},
            {"name": "Datadog", "category": "Monitoring", "regex": r'datadog|DD_'},
            {"name": "Elasticsearch", "category": "Search", "regex": r'elasticsearch|_search\?|_cat'},
            {"name": "Algolia", "category": "Search", "regex": r'algolia\.net|algoliasearch'},
            {"name": "Swagger", "category": "API Documentation", "regex": r'swagger|swagger-ui|openapi'},
            {"name": "GraphQL", "category": "API", "regex": r'graphql|__graphql|graphiql'},
            {"name": "WebSocket", "category": "Protocol", "regex": r'websocket|socket\.io|sockjs|pusher'},
            {"name": "Docker", "category": "Container", "regex": r'docker|Docker\-'},
            {"name": "Kubernetes", "category": "Orchestration", "regex": r'kubernetes|kube|k8s'},
            {"name": "Terraform", "category": "Infrastructure", "regex": r'terraform|\.tf\b'},
            {"name": "Jenkins", "category": "CI/CD", "regex": r'jenkins|Jenkins\-'},
            {"name": "GitLab", "category": "CI/CD", "regex": r'gitlab|GitLab\-'},
            {"name": "GitHub Pages", "category": "Hosting", "regex": r'github\.io|github\.com'},
            {"name": "Netlify", "category": "Hosting", "regex": r'netlify\.com|netlify'},
            {"name": "Vercel", "category": "Hosting", "regex": r'vercel\.com|vercel'},
            {"name": "Heroku", "category": "Hosting", "regex": r'heroku\.com|herokuapp\.com'},
            {"name": "DigitalOcean", "category": "Hosting", "regex": r'digitalocean\.com|DO\-'},
            {"name": "Linode", "category": "Hosting", "regex": r'linode\.com'},
            {"name": "LoadBalancer", "category": "Infrastructure", "regex": r'ELB|ALB|CLB|NLB|LoadBalancer'},
            {"name": "WAF", "category": "Security", "regex": r'ModSecurity|_waf|waf_'},
            {"name": "reCAPTCHA", "category": "Security", "regex": r'recaptcha|g-recaptcha|hcaptcha'},
            {"name": "Auth0", "category": "Authentication", "regex": r'auth0\.com|auth0'},
            {"name": "Okta", "category": "Authentication", "regex": r'okta\.com|okta'},
            {"name": "Firebase", "category": "Backend", "regex": r'firebase\.com|firebaseio\.com|firebaseapp\.com'},
            {"name": "Supabase", "category": "Backend", "regex": r'supabase\.co|supabase'},
            {"name": "Pusher", "category": "Realtime", "regex": r'pusher\.com|Pusher\.js'},
            {"name": "Mapbox", "category": "Maps", "regex": r'mapbox\.com|mapbox\.gl'},
            {"name": "Google Maps", "category": "Maps", "regex": r'maps\.googleapis\.com|google\.maps'},
            {"name": "Intercom", "category": "Chat", "regex": r'intercom\.io|Intercom'},
            {"name": "Zendesk", "category": "Support", "regex": r'zendesk\.com|zopim'},
            {"name": "Gatsby", "category": "Static Site", "regex": r'gatsby|__GATSBY'},
            {"name": "Hugo", "category": "Static Site", "regex": r'hugo|\.hugo'},
            {"name": "Jekyll", "category": "Static Site", "regex": r'jekyll|github\.io'},
            {"name": "PHP", "category": "Language", "regex": r'\.php|PHP|X-Powered-By:\s*PHP'},
            {"name": "Python", "category": "Language", "regex": r'\.py|Python|flask|django|fastapi|starlette'},
            {"name": "Ruby", "category": "Language", "regex": r'\.rb|ruby|Rack|Passenger'},
            {"name": "Java", "category": "Language", "regex": r'\.jsp|\.jar|Java|Spring|Tomcat|Jetty'},
            {"name": "Go", "category": "Language", "regex": r'go\s*version|golang|gin-gonic|gorilla'},
            {"name": "Rust", "category": "Language", "regex": r'rust|actix|rocket|warp|axum'},
            {"name": "Haskell", "category": "Language", "regex": r'haskell|yesod|servant'},
            {"name": "Perl", "category": "Language", "regex": r'\.pl|perl|CGI\.pm'},
        ]

    async def scan(self, domain: str) -> dict:
        technologies = []
        headers_text = ""
        body_text = ""

        urls = [
            f"https://{domain}",
            f"http://{domain}",
        ]

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
            for url in urls:
                try:
                    async with session.get(url, ssl=False, allow_redirects=True) as response:
                        headers_text = str(response.headers)
                        body = await response.text()
                        body_text = body

                        server = response.headers.get("Server", "")
                        if server:
                            technologies.append({
                                "name": server.split("/")[0],
                                "version": server.split("/")[1] if "/" in server else "",
                                "category": "Web Server",
                                "confidence": "high",
                                "source": "header",
                            })

                        powered_by = response.headers.get("X-Powered-By", "")
                        if powered_by:
                            pb_parts = powered_by.split("/")
                            technologies.append({
                                "name": pb_parts[0],
                                "version": pb_parts[1] if len(pb_parts) > 1 else "",
                                "category": "Technology",
                                "confidence": "high",
                                "source": "header",
                            })

                        for key, val in response.headers.items():
                            if key.startswith("X-"):
                                if val and val not in ["", "1"]:
                                    technologies.append({
                                        "name": f"{key}: {val}",
                                        "version": "",
                                        "category": "Custom Header",
                                        "confidence": "medium",
                                        "source": "header",
                                    })

                        break
                except Exception:
                    continue

        search_text = headers_text + " " + body_text
        for sig in self.signatures:
            if re.search(sig["regex"], search_text, re.IGNORECASE):
                name = sig["name"]
                existing = next((t for t in technologies if t["name"] == name), None)
                if not existing:
                    technologies.append({
                        "name": name,
                        "version": "",
                        "category": sig["category"],
                        "confidence": "medium",
                        "source": "signature",
                    })

        return {
            "domain": domain,
            "technologies": technologies,
            "count": len(technologies),
        }
