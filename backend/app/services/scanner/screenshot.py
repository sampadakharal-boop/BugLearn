import os
import asyncio
from pathlib import Path
from typing import Optional


class ScreenshotCollector:
    def __init__(self, output_dir: str = "screenshots"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    async def scan(self, domain: str) -> dict:
        screenshots = []
        urls = [
            f"https://{domain}",
            f"https://www.{domain}",
            f"http://{domain}",
            f"http://www.{domain}",
        ]

        try:
            from playwright.async_api import async_playwright

            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=["--no-sandbox", "--disable-setuid-sandbox"],
                )

                for url in urls:
                    try:
                        screenshot_path = os.path.join(
                            self.output_dir, f"{domain.replace('.', '_')}_{url.split('://')[0]}.png"
                        )

                        context = await browser.new_context(
                            viewport={"width": 1920, "height": 1080},
                            user_agent="ReconForgeAI/1.0",
                        )
                        page = await context.new_page()

                        await page.goto(url, wait_until="networkidle", timeout=30000)
                        await page.screenshot(path=screenshot_path, full_page=True)

                        title = await page.title()
                        status_code = None
                        try:
                            status_code = (await page.request(url)).response().status if False else 200
                        except Exception:
                            status_code = None

                        screenshots.append({
                            "url": url,
                            "title": title or "",
                            "screenshot_path": screenshot_path,
                            "status": "success",
                        })

                        await context.close()
                    except Exception as e:
                        screenshots.append({
                            "url": url,
                            "title": "",
                            "screenshot_path": "",
                            "status": "error",
                            "error": str(e),
                        })

                await browser.close()
        except ImportError:
            screenshots.append({
                "url": "N/A",
                "title": "",
                "screenshot_path": "",
                "status": "skipped",
                "error": "Playwright not installed. Install with: pip install playwright && playwright install chromium",
            })

        return {
            "domain": domain,
            "screenshots": screenshots,
            "count": len([s for s in screenshots if s["status"] == "success"]),
        }
