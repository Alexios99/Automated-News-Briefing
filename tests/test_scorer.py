import pytest
from scorer import contains_relevant_keywords
# from scorer import contains_relevant_keywords


def test_contains_relevant_keywords_found():
    text = "The green bond market is booming"
    keywords = ["green bond", "climate", "ESG"]
    assert contains_relevant_keywords(text, keywords) is True


def test_contains_relevant_keywords_not_found():
    text = "Tech stocks led the market today"
    keywords = ["sustainable", "climate"]
    assert contains_relevant_keywords(text, keywords) is False


def test_contains_relevant_keywords_empty_text():
    assert contains_relevant_keywords("", ["climate"]) is False


def test_contains_relevant_keywords_empty_keywords():
    assert contains_relevant_keywords("Green bond news", []) is False

'''
def test_score_article_positive():
    article = {
        "title": "Investors embrace sustainable finance with optimism",
        "description": "Green bonds and ESG funds see strong demand"
    }
    result = score_article(article)
    assert result in ["pos", "neg", "neutral"]
    assert result == "pos"


def test_score_article_negative():
    article = {
        "title": "ESG investing faces backlash from major funds",
        "description": "Critics argue greenwashing undermines credibility. Greenwashing is going to end the world, this is a horrible method"
    }
    result = score_article(article)
    assert result in ["pos", "neg", "neutral"]
    assert result == "neg"


def test_score_article_missing_fields():
    article = {}
    result = score_article(article)
    assert result == "neutral"
'''