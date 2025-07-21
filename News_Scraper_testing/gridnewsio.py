import requests
import json

GRID_NEWS_API_KEY = "fac889f8c481bfa3a2e7cc42a6d48763"
GRID_NEWS_API_URL = "https://api.gridnews.io/v1/query"

def get_uk_funds_news(query='"UK funds" OR "investment trusts"'):
    """
    Fetches news for a given query, tailored for UK funds.
    
    Refer to the Grid News API documentation for more query options:
    https://www.gridnews.io/docs/query-api/endpoint
    """
    params = {
        'apiKey': GRID_NEWS_API_KEY,
        'q': query,
        'country': 'gb',
        'category': 'business,finance',
        'limit': 10
    }

    print(f"Querying Grid News with: {query}")

    try:
        response = requests.get(GRID_NEWS_API_URL, params=params)
        response.raise_for_status()  # Raises a HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err}")
    
    return None

if __name__ == '__main__':
    news = get_uk_funds_news()
    if news:
        print("Successfully fetched news:")
        print(json.dumps(news, indent=4))
    else:
        print("Failed to fetch news.")
