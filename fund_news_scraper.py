import json
import os
from newspaper import Article, Config
from time import sleep
import requests
from bs4 import BeautifulSoup
from readability import Document

INPUT_PATH = 'data/marketaux_news_results.json'
OUTPUT_PATH = 'data/marketaux_news_with_content.json'


def fetch_article_content(url):
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
    # First try newspaper3k
    try:
        config = Config()
        config.browser_user_agent = user_agent
        article = Article(url, config=config)
        article.download()
        article.parse()
        if article.text and len(article.text.strip()) > 200:
            print(f"[newspaper3k] Success: {url}")
            return article.text
        else:
            print(f"[newspaper3k] Empty or too short, will try fallback: {url}")
    except Exception as e:
        print(f"[newspaper3k] Error fetching article at {url}: {e}")
    # Fallback: requests + BeautifulSoup + readability-lxml
    try:
        headers = {"User-Agent": user_agent}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        doc = Document(resp.text)
        summary_html = doc.summary()
        soup = BeautifulSoup(summary_html, "lxml")
        text = soup.get_text(separator="\n", strip=True)
        if text and len(text.strip()) > 200:
            print(f"[readability-lxml] Success: {url}")
            return text
        else:
            print(f"[readability-lxml] Extracted text too short: {url}")
    except Exception as e:
        print(f"[readability-lxml] Error fetching article at {url}: {e}")
    return None

def main():
    if not os.path.exists(INPUT_PATH):
        print(f"Input file not found: {INPUT_PATH}")
        return
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    print(f"Loaded {len(articles)} articles.")
    enriched = []
    for i, art in enumerate(articles):
        url = art.get('url')
        if not url:
            art['content'] = None
            enriched.append(art)
            continue
        print(f"[{i+1}/{len(articles)}] Fetching: {url}")
        content = fetch_article_content(url)
        art['content'] = content
        enriched.append(art)
        sleep(1)  # be polite to servers
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(enriched)} articles with content to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
