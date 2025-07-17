import config
import urllib.parse
import requests
from datetime import date, timedelta
from typing import List, Dict


def construct_query_from_keywords(keywords: List[str]) -> str:
    query_joined = ' OR '.join([f'"{kw}"' for kw in keywords])
    return urllib.parse.quote(query_joined)


def fetch_articles(keywords: List[str], from_days_ago: int) -> List[Dict]:
    query_encoded = construct_query_from_keywords(keywords)
    from_date = (date.today() - timedelta(days=from_days_ago)).isoformat()

    url = (
        'https://newsapi.org/v2/everything?'
        f'q={query_encoded}&'
        f'from={from_date}&'
        'language=en&'
        'sortBy=publishedAt&'
        f'apiKey={config.NEWS_API_KEY}'
    )

    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"NewsAPI error: {response.status_code} - {response.text}")
    
    data = response.json()
    if data.get("status") != "ok":
        raise ValueError(f"Error in API response: {data.get('message')}")

    return data.get("articles", [])


