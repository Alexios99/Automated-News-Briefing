import requests
import datetime
import pandas as pd
import json
from time import sleep
from config import MARKETAUX_API_TOKEN


API_TOKEN = MARKETAUX_API_TOKEN
BASE_URL = "https://api.marketaux.com/v1/entity/search"

def symbol_exists(symbol: str) -> bool:
    """
    Return True if *symbol* is recognised by MarketAux, else False.
    """
    if not API_TOKEN:
        raise RuntimeError("Set MARKETAUX_TOKEN env-var or hard-code your token")
    params = {
        "api_token": API_TOKEN,
        "symbols": symbol.upper(),
        "limit": 1
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        return bool(resp.json().get("data"))
    except Exception:
        return False

def check_funds_in_marketaux(csv_path: str = "data/listed_funds_symbols_news.csv") -> dict:
    """
    Check which fund tickers from the CSV exist in MarketAux.
    Returns a dict with 'found', 'not_found', and 'errors' lists.
    """
    results = {'found': [], 'not_found': [], 'errors': []}
    try:
        funds_df = pd.read_csv(csv_path)
        print(f"Checking {len(funds_df)} funds in MarketAux...")
        for _, row in funds_df.iterrows():
            fund_name = str(row["Investment trust name"])
            ticker = str(row["Ticker"]).strip()
            if not ticker or ticker.lower() == 'nan':
                results['errors'].append({'name': fund_name, 'ticker': ticker, 'error': 'Missing ticker'})
                print(f"! {fund_name} - Missing ticker")
                continue
            try:
                if symbol_exists(ticker):
                    results['found'].append({'name': fund_name, 'ticker': ticker})
                    print(f"✓ {ticker} ({fund_name}) - Found")
                else:
                    results['not_found'].append({'name': fund_name, 'ticker': ticker})
                    print(f"✗ {ticker} ({fund_name}) - Not found")
            except Exception as e:
                results['errors'].append({'name': fund_name, 'ticker': ticker, 'error': str(e)})
                print(f"! {ticker} ({fund_name}) - Error: {e}")
        print(f"\nResults: Found: {len(results['found'])}, Not found: {len(results['not_found'])}, Errors: {len(results['errors'])}")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return results

def save_results_to_csv(results: dict, output_path: str = "data/marketaux_check_results.csv"):
    """
    Save the MarketAux check results to a CSV file.
    """
    try:
        all_results = []
        for fund in results.get('found', []):
            all_results.append({'Fund Name': fund['name'], 'Ticker': fund['ticker'], 'Status': 'Found', 'Error': ''})
        for fund in results.get('not_found', []):
            all_results.append({'Fund Name': fund['name'], 'Ticker': fund['ticker'], 'Status': 'Not Found', 'Error': ''})
        for fund in results.get('errors', []):
            all_results.append({'Fund Name': fund['name'], 'Ticker': fund['ticker'], 'Status': 'Error', 'Error': fund.get('error', '')})
        pd.DataFrame(all_results).to_csv(output_path, index=False)
        print(f"Results saved to {output_path}")
    except Exception as e:
        print(f"Error saving results: {e}")

def fetch_news_for_funds(csv_path: str = "data/listed_funds_symbols_news.csv", output_path: str = "data/marketaux_news_results.json", batch_size: int = 3, delay: float = 1.0):
    """
    Fetch news for all tickers in the CSV using the MarketAux API and save to a JSON file.
    Only new articles (by uuid or url) are added if the file already exists.
    Each article is labeled with the matching fund(s) by ticker or name.
    Args:
        csv_path: Path to the CSV file containing fund tickers
        output_path: Path to save the news results JSON
        batch_size: Number of tickers per API request (default 50)
        delay: Seconds to wait between requests to avoid rate limits
    """
    try:
        # Load existing news if present
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                existing_news = json.load(f)
            print(f"Loaded {len(existing_news)} existing articles.")
        except Exception:
            existing_news = []
        # Build set of existing uuids and urls
        existing_uuids = set()
        existing_urls = set()
        for art in existing_news:
            if 'uuid' in art:
                existing_uuids.add(art['uuid'])
            if 'url' in art:
                existing_urls.add(art['url'])

        funds_df = pd.read_csv(csv_path)
        fund_map = {}
        for _, row in funds_df.iterrows():
            fund_name = str(row["Investment trust name"]).strip()
            ticker = str(row["Ticker"]).strip()
            if ticker and ticker.lower() != 'nan':
                fund_map[ticker.upper()] = fund_name

        tickers = list(fund_map.keys())
        print(f"Fetching news for {len(tickers)} tickers in batches of {batch_size}...")
        new_articles = []
        for i in range(0, len(tickers), batch_size):
            batch = tickers[i:i+batch_size]
            params = {
                "api_token": API_TOKEN,
                "symbols": ','.join(batch),
                "filter_entities": "true",
                "limit": 50
            }
            try:
                resp = requests.get("https://api.marketaux.com/v1/news/all", params=params, timeout=15)
                resp.raise_for_status()
                news_batch = resp.json().get("data", [])
                print(f"Batch {i//batch_size+1}: {len(news_batch)} articles fetched.")
                for art in news_batch:
                    uid = art.get('uuid')
                    url = art.get('url')
                    if (uid and uid in existing_uuids) or (url and url in existing_urls):
                        continue  # skip existing
                    # Label with matching funds
                    matched_funds = set()
                    # Check MarketAux entities for tickers
                    for entity in art.get('entities', []):
                        symbol = entity.get('symbol', '').upper()
                        if symbol in fund_map:
                            matched_funds.add(fund_map[symbol])
                    # Fallback: check in title for fund names
                    title = art.get('title', '').lower()
                    for fund_name in fund_map.values():
                        if fund_name.lower() in title:
                            matched_funds.add(fund_name)
                    art['funds'] = sorted(matched_funds)
                    new_articles.append(art)
                    if uid:
                        existing_uuids.add(uid)
                    if url:
                        existing_urls.add(url)
            except Exception as e:
                print(f"Error fetching batch {i//batch_size+1}: {e}")
            sleep(delay)  # avoid hitting rate limits
        print(f"Adding {len(new_articles)} new articles.")
        all_news = existing_news + new_articles
        # Save all news to JSON
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_news, f, ensure_ascii=False, indent=2)
        print(f"All news saved to {output_path}")
    except Exception as e:
        print(f"Error fetching news: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--check-funds":
            results = check_funds_in_marketaux()
            save_results_to_csv(results)
        elif sys.argv[1] == "--fetch-news":
            fetch_news_for_funds()