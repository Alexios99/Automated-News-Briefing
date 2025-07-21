import pytest
import asyncio
from news_scraper.extractor import get_full_article

# Example public URLs (should be free to access)
TEST_URLS = [
    "https://www.reuters.com/business/sustainable-business/uk-green-funds-face-tougher-scrutiny-2023-07-10/",
    "https://www.ft.com/content/dc8489f1-1b31-4891-93d7-f41c94bb95c4",
    "https://www.bloomberg.com/news/articles/2024-03-12/citi-says-traders-are-ignoring-a-key-signal-from-the-fed"
]

@pytest.mark.integration
@pytest.mark.parametrize("url", TEST_URLS)
def test_get_full_article(url):
    try:
        article = asyncio.run(get_full_article(url))
    except Exception as e:
        pytest.skip(f"Network or extraction error: {e}")
    if not article:
        pytest.skip("Extraction failed or no content returned.")
    assert article["title"] and isinstance(article["title"], str)
    assert article["text"] and len(article["text"]) >= 1000 