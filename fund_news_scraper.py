import json
import os
from newspaper import Article
from time import sleep

INPUT_PATH = 'data/marketaux_news_results.json'
OUTPUT_PATH = 'data/marketaux_news_with_content.json'


def fetch_article_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Error fetching article at {url}: {e}")
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
