import pytest
import news_fetcher
import config

# Mock NewsAPI response
mock_response = {
    "status": "ok",
    "totalResults": 3,
    "articles": [
        {
            "source": {"name": "Green Finance Times"},
            "author": "Jane Doe",
            "title": "Sustainable Bonds See Record Inflows",
            "description": "Institutional investors are pouring into green bonds.",
            "url": "https://example.com/article1",
            "publishedAt": "2025-06-17T10:00:00Z"
        },
        {
            "source": {"name": "Climate News Daily"},
            "author": "John Smith",
            "title": "Blue Economy Policy in Southeast Asia Gains Steam",
            "description": "New regulations support sustainable fishing practices.",
            "url": "https://example.com/article2",
            "publishedAt": "2025-06-17T08:30:00Z"
        }
        {
            "source": {"name": "ColumbiaThreadneedle"}, #MakeTest
            "author": "Jane Doe",
            "title": "Sustainable Bonds See Record Inflows",
            "description": "Institutional investors are pouring into green bonds.",
            "url": "https://example.com/article1",
            "publishedAt": "2025-06-17T10:00:00Z"
        }
    ]
}

def test_construct_query_from_keywords():
    keywords = ["green bonds", "climate"]
    query = news_fetcher.construct_query_from_keywords(keywords)
    assert "%22green%20bonds%22" in query
    assert "%22climate%22" in query
    assert "%20OR%20" in query

def test_fetch_articles_success(monkeypatch):
    """Test successful fetch with mocked API response."""

    class MockResponse:
        def __init__(self):
            self.status_code = 200
        def json(self):
            return mock_response

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(news_fetcher.requests, "get", mock_get)

    articles = news_fetcher.fetch_articles(["climate", "sustainable"], from_days_ago=3)
    assert isinstance(articles, list)
    assert len(articles) == 2
    assert articles[0]["title"] == "Sustainable Bonds See Record Inflows"

def test_fetch_articles_failure(monkeypatch):
    """Test API failure handling."""

    class MockResponse:
        def __init__(self):
            self.status_code = 403
            self.text = "Forbidden"

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(news_fetcher.requests, "get", mock_get)

    with pytest.raises(RuntimeError) as excinfo:
        news_fetcher.fetch_articles(["badkey"], 3)
    
    assert "NewsAPI error" in str(excinfo.value)
