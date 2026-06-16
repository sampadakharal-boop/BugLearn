from app.services.scanner.subdomain import SubdomainScanner
from app.services.scanner.dns import DNSScanner
from app.services.scanner.port import PortScanner
from app.services.scanner.tech import TechScanner
from app.services.scanner.screenshot import ScreenshotCollector
from app.services.scanner.endpoint import EndpointDiscoverer
from app.services.scanner.js_analyzer import JSAnalyzer


class ScannerOrchestrator:
    def __init__(self):
        self.modules = {
            "subdomain": SubdomainScanner(),
            "dns": DNSScanner(),
            "port": PortScanner(),
            "tech": TechScanner(),
            "screenshot": ScreenshotCollector(),
            "endpoint": EndpointDiscoverer(),
            "js": JSAnalyzer(),
        }

    async def run_module(self, module_name: str, domain: str) -> dict:
        scanner = self.modules.get(module_name)
        if not scanner:
            raise ValueError(f"Unknown module: {module_name}")
        return await scanner.scan(domain)

    async def run_full_scan(self, domain: str) -> dict:
        results = {}
        for name, scanner in self.modules.items():
            try:
                results[name] = await scanner.scan(domain)
            except Exception as e:
                results[name] = {"error": str(e)}
        return results


orchestrator = ScannerOrchestrator()
