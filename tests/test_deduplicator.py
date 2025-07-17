import pytest
from deduplicator import deduplicate_articles

def test_deduplicate_articles():
    articles = [
        {"title": "Green bonds are booming"},
        {"title": "Green bonds are booming"},
        {"title": "ESG investing is on the rise"},
    ]
    result = deduplicate_articles(articles)
    assert len(result) == 2
    assert result[0]["title"] == "Green bonds are booming"
    assert result[1]["title"] == "ESG investing is on the rise"