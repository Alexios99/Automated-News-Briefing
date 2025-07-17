from typing import List, Dict
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from nltk.sentiment import SentimentIntensityAnalyzer

def score_article(article: dict) -> str:
    """
    Returns the sentiment classification ('pos', 'neg', or 'neutral') of the article
    using VADER sentiment analysis on the title + description.
    """
    import nltk
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        nltk.download('vader_lexicon', quiet=True)
    sia = SentimentIntensityAnalyzer()
    text = f"{article.get('title', '')} {article.get('description', '')}".strip()
    if not text:
        return "neutral"  # fallback if article is empty
    scores = sia.polarity_scores(text)
    compound = scores['compound']
    if compound > 0.1:
        return "Positive"
    elif compound < -0.1:
        return "Negative"
    else:
        return "Neutral"

def contains_relevant_keywords(text: str, keywords: List[str]) -> bool:
    """
    Checks whether any of the provided keywords appear in the given text (case-insensitive).
    """
    if not text or not keywords:
        return False
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)
