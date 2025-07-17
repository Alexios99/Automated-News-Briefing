import os
import sys
from datetime import datetime, timedelta
from typing import List, Optional

from config import NEWS_API_KEY, GOOGLE_API_KEY, KEYWORDS, GEMINI_MODEL, RELEVANT_KEYWORDS, FUNDS
from news_fetcher import fetch_articles
from human_screen import human_screen_articles
from scorer import contains_relevant_keywords, score_article
from deduplicator import deduplicate_articles
from summariser import configure_model, generate_summary, generate_intro
from reporter import build_briefing
from formatter import generate_markdown, generate_html, generate_pdf, generate_fund_performance_section
from flask import send_from_directory
from fund_info import refresh_fund_data
from fund_news_fetcher import fetch_news_for_funds


def run_pipeline(
    output_dir: str = "./output",
    from_days_ago: int = 3,
    keywords: Optional[List[str]] = None,
    funds: Optional[List[str]] = None
):
    """
    Run the sustainable finance news summarization pipeline.
    Args:
        output_dir (str): Directory to save the output files.
        from_days_ago (int): Number of days ago to fetch articles from.
        keywords (List[str], optional): Custom keywords to search for.
        funds (List[str], optional): Custom funds to include (currently not used in logic).
    """
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Fetch articles from NewsAPI
    print("Fetching articles...")
    search_keywords = keywords if keywords else KEYWORDS
    all_accepted = []

    articles = fetch_articles(search_keywords, from_days_ago=from_days_ago)
    screened = human_screen_articles(articles)
    all_accepted.extend(screened)

    if not all_accepted:
        print("No articles accepted. Exiting.")
        return None
    if not articles:
        print("No articles found. Exiting.")
        return None
    articles = all_accepted

    # Step 2: Filter articles (scoring temporarily disabled)
    print("Filtering articles...")
    filtered_articles = []
    for article in articles:
        if not article.get("title") or not article.get("content"):
            continue
        filtered_articles.append(article)

    # Step 3: Deduplicate articles
    print("Deduplicating articles...")
    unique_articles = deduplicate_articles(filtered_articles)

    # Step 4: Configure Gemini model for summarization
    print("Configuring Gemini model...")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is missing or None.")
    model, chat = configure_model(str(GOOGLE_API_KEY))

    # Step 5: Generate summaries, topics, and mentioned companies
    print("Generating summaries and extracting metadata...")
    enriched_articles = []
    limited_articles = unique_articles[:10]
    for article in limited_articles:
        try:
            summary = generate_summary(model, article["content"])
            enriched_articles.append({
                "title": article["title"],
                "url": article["url"],
                "date": article["publishedAt"],
                "source": article["source"]["name"],
                "summary": summary,
                "sentiment": score_article(article),
            })
        except Exception as e:
            print(f"Error summarizing article '{article['title']}': {e}")

    # Step 5.5: Updata and add fund performance data
    print("Checking fund performance data...")
    refresh_fund_data()  # Will only refresh if data is stale

    print("Updating/loading fund performance data...")

    fund_performance = None
    fund_data_path = "data/fund_analysis_results.csv"
    if os.path.exists(fund_data_path):
        fund_performance = generate_fund_performance_section(fund_data_path)

    # Step 6: Build the final briefing
    print("Building the briefing...")
    summaries = [article["summary"] for article in enriched_articles]
    briefing = build_briefing(enriched_articles)
    briefing["fund_performance"] = fund_performance
    briefing["intro"] = generate_intro(model, summaries)

    # Step 7: Output to Markdown, HTML, and PDF
    print("Generating output files...")
    date_str = datetime.now().strftime("%Y-%m-%d")
    markdown_path = os.path.join(output_dir, f"briefing_{date_str}.md")
    html_path = os.path.join(output_dir, f"briefing_{date_str}.html")
    pdf_path = os.path.join(output_dir, f"briefing_{date_str}.pdf")

    generate_markdown(briefing, markdown_path)
    html_content = generate_html(briefing, logo_path='images/logo.png')
    with open(html_path, "w") as html_file:
        html_file.write(html_content)
    generate_pdf(briefing, pdf_path, logo_path='images/logo.png')

    print(f"Briefing generated successfully!")
    print(f"- Markdown: {markdown_path}")
    print(f"- HTML: {html_path}")
    print(f"- PDF: {pdf_path}")

    return {
        "markdown": markdown_path,
        "html": html_path,
        "pdf": pdf_path
    }


def main(output_dir: str = "./output", from_days_ago: int = 3):
    # For backward compatibility with CLI usage
    run_pipeline(output_dir=output_dir, from_days_ago=from_days_ago)


if __name__ == "__main__":
    if '--update-fund-news' in sys.argv:
        print("Updating news for funds using MarketAux...")
        fetch_news_for_funds()
    else:
        output_dir = sys.argv[1] if len(sys.argv) > 1 else "./output"
        from_days_ago = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        main(output_dir=output_dir, from_days_ago=from_days_ago)