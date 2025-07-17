import pytest
from datetime import date
from reporter import build_briefing


def test_build_briefing_structure():
    # Sample input: 2 enriched articles
    enriched_articles = [
        {
            "title": "Green bonds surge in popularity",
            "summary": "• Investors are increasing exposure to green bonds...",
            "url": "https://example.com/green-bonds",
            "date": "2025-06-17",
            "source": "ESG Newswire"
        },
        {
            "title": "EU sets new net zero rules",
            "summary": "• New policy introduces strict ESG disclosure requirements...",
            "url": "https://example.com/net-zero",
            "date": "2025-06-17",
            "source": "Sustainable Finance Weekly"
        }
    ]

    result = build_briefing(enriched_articles)

    # Core keys
    assert isinstance(result, dict)
    assert "date" in result and isinstance(result["date"], date)
    assert "intro" in result and isinstance(result["intro"], str)
    assert "articles" in result and len(result["articles"]) == 2




def test_build_briefing_empty_input():
    result = build_briefing([])
    assert isinstance(result, dict)
    assert result["articles"] == []
    
