from typing import List, Dict
from collections import Counter
from datetime import date

def build_briefing(top_articles: List[Dict]) -> Dict:
    """
    Builds a structured briefing from enriched articles.

    Args:
        top_articles (List[Dict]): A list of enriched articles with metadata.

    Returns:
        Dict: A structured briefing containing intro, articles, topic counts, and company mentions.
    """
    # Initialize the briefing structure
    briefing = {
        "date": date.today(),  
        "intro": "This week's briefing (this is a placeholder intro)",  
        "articles": [],
        "topic_counts": {},
        "company_mentions": {}
    }

    # Process articles
    topics = []
    companies = []

    for article in top_articles:
        # Extract relevant fields
        briefing["articles"].append({
            "title": article.get("title"),
            "summary": article.get("summary"),
            "sentiment": article.get("sentiment"),
            "url": article.get("url"),
            "date": article.get("date"),
            "source": article.get("source"),
        })

    return briefing