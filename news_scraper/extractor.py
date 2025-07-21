"""
Multi-layer article extraction pipeline for news scraping.

Layers:
- L1: newspaper3k (fast, lightweight)
- L2: requests + BeautifulSoup + readability-lxml (fallback)
- L3: Playwright (headless Chromium, stealth, JS rendering)
- L4: (stub) fallback_api.fetch(url)

Setup:
    pip install -r requirements.txt
    playwright install

Legal: Only use on sites where you have permission. Respect publisher ToS.
"""

import asyncio
from typing import Optional, Dict, Any
import structlog
from time import time
from newspaper import Article, Config
import requests
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
from news_scraper.playwright_layer import fetch_article_html

logger = structlog.get_logger()

async def get_full_article(url: str) -> Optional[Dict[str, Any]]:
    """
    Try multiple extraction layers for a news article. Returns dict with 'title', 'text', 'layer', 'elapsed_ms', 'url'.
    Returns None if all layers fail.
    """
    start = time()
    # L1: newspaper3k
    try:
        config = Config()
        config.browser_user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
        art = Article(url, config=config)
        art.download()
        art.parse()
        text = art.text or ""
        if len(text) >= 1000:
            elapsed = int((time() - start) * 1000)
            logger.info("extract_success", layer="newspaper3k", url=url, elapsed_ms=elapsed)
            return {"title": art.title, "text": text, "layer": "newspaper3k", "elapsed_ms": elapsed, "url": url}
    except Exception as e:
        logger.warning("extract_failed", layer="newspaper3k", url=url, error=str(e))

    # L2: requests + BeautifulSoup + readability-lxml
    try:
        headers = {"User-Agent": config.browser_user_agent}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        doc = Document(resp.text)
        summary_html = doc.summary()
        soup = BeautifulSoup(summary_html, "lxml")
        text = soup.get_text(separator="\n", strip=True)
        if len(text) >= 1000:
            elapsed = int((time() - start) * 1000)
            logger.info("extract_success", layer="readability-lxml", url=url, elapsed_ms=elapsed)
            return {"title": doc.title(), "text": text, "layer": "readability-lxml", "elapsed_ms": elapsed, "url": url}
    except Exception as e:
        logger.warning("extract_failed", layer="readability-lxml", url=url, error=str(e))

    # L3: Playwright (headless, stealth)
    try:
        html = await fetch_article_html(url)
        if html:
            doc = Document(html)
            text = doc.summary(html_partial=False)
            if not text or len(text) < 500:
                text = trafilatura.extract(html, favor_precision=True) or ""
            if text and len(text) >= 1000:
                elapsed = int((time() - start) * 1000)
                logger.info("extract_success", layer="playwright", url=url, elapsed_ms=elapsed)
                return {"title": doc.title(), "text": text, "layer": "playwright", "elapsed_ms": elapsed, "url": url}
    except Exception as e:
        logger.warning("extract_failed", layer="playwright", url=url, error=str(e))

    # L4: (future) fallback_api.fetch(url) stub
    logger.info("extract_failed_all_layers", url=url)
    return None 