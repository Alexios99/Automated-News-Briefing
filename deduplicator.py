from difflib import SequenceMatcher
from typing import List, Dict

def is_similar(a, b, threshold=0.85):
    """Checks if two strings are similar above a certain threshold."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() > threshold

def deduplicate_articles(articles: List[Dict]) -> List[Dict]:
    seen_titles = []
    deduplicated = []
    for article in articles:
        if not article.get('title'):
            continue

        if all(not is_similar(article['title'], seen_title) for seen_title in seen_titles):
            deduplicated.append(article)
            seen_titles.append(article['title'])
    return deduplicated
