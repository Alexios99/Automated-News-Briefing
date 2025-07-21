import json
import os
import asyncio
from news_scraper.extractor import get_full_article

INPUT_PATH = 'data/marketaux_news_results.json'
OUTPUT_PATH = 'data/marketaux_news_with_content.json'


async def process_article(article_data, index, total):
    url = article_data.get('url')
    if not url:
        article_data['content'] = None
        return article_data

    print(f"[{index + 1}/{total}] Fetching: {url}")
    result = await get_full_article(url)
    
    article_data['content'] = result['text'] if result else None
    
    return article_data


async def main():
    if not os.path.exists(INPUT_PATH):
        print(f"Input file not found: {INPUT_PATH}")
        return
        
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    print(f"Loaded {len(articles)} articles.")

    tasks = [process_article(art, i, len(articles)) for i, art in enumerate(articles)]
    
    enriched_articles = await asyncio.gather(*tasks)

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(enriched_articles, f, ensure_ascii=False, indent=2)
        
    print(f"Saved {len(enriched_articles)} articles with content to {OUTPUT_PATH}")


if __name__ == "__main__":
    # Ensure you have installed the browser drivers: playwright install
    asyncio.run(main())
