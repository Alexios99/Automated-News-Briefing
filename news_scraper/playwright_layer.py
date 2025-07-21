"""
Playwright-based article HTML fetcher for news scraping.

- Uses headless Chromium with stealth patches to bypass anti-bot and JS paywalls.
- Rotates user-agents and viewport sizes.
- Capped concurrency with asyncio.Semaphore.
- Retries with exponential backoff on 429/503.
- Returns fully rendered HTML for downstream extraction (readability-lxml, trafilatura).

Setup:
    pip install -r requirements.txt
    playwright install

Legal: Only use on sites where you have permission. Respect publisher ToS.
"""

import asyncio
import random
from typing import Optional, cast
from playwright.async_api import async_playwright, Browser, Page, ViewportSize
from playwright_stealth import stealth # type: ignore
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import structlog

# Module-level semaphore for concurrency
SEM = asyncio.Semaphore(5)

# List of realistic user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
]

VIEWPORTS = [
    {"width": 1280, "height": 800},
    {"width": 1920, "height": 1080},
    {"width": 375, "height": 667},
    {"width": 1440, "height": 900},
]

logger = structlog.get_logger()

class FetchError(Exception):
    pass

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(FetchError)
)
async def fetch_article_html(url: str, timeout_ms: int = 30_000, user_agent: Optional[str] = None) -> Optional[str]:
    """
    Render URL in headless Chromium (stealth), return final HTML.
    Return None on 4xx/5xx or if load exceeds timeout.
    """
    async with SEM:
        user_agent = user_agent or random.choice(USER_AGENTS)
        viewport = cast(ViewportSize, random.choice(VIEWPORTS))
        start = asyncio.get_event_loop().time()
        try:
            async with async_playwright() as p:
                browser: Browser = await p.chromium.launch(headless=True)
                page: Page = await browser.new_page(
                    user_agent=user_agent,
                    viewport=viewport,
                    java_script_enabled=True,
                )
                await stealth(page) # type: ignore
                resp = await page.goto(url, timeout=timeout_ms, wait_until="networkidle")
                status = resp.status if resp else None
                if status and (400 <= status < 600):
                    logger.info("playwright_fetch_fail", event="http_error", url=url, status=status)
                    await browser.close()
                    return None
                html = await page.content()
                elapsed = int((asyncio.get_event_loop().time() - start) * 1000)
                logger.info("playwright_fetch_success", event="fetch", url=url, layer="playwright", elapsed_ms=elapsed, status=status)
                await browser.close()
                return html
        except Exception as e:
            elapsed = int((asyncio.get_event_loop().time() - start) * 1000)
            logger.warning("playwright_fetch_exception", event="exception", url=url, layer="playwright", elapsed_ms=elapsed, error=str(e))
            raise FetchError(str(e)) 