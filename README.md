# Automated News Briefing

## Overview

Automated News Briefing is a powerful, dual-pipeline platform for fetching, analyzing, and summarizing news articles, designed for institutional investors and financial professionals. It provides concise, actionable insights through briefings in Markdown, HTML, and PDF formats. The system integrates multiple news APIs, advanced web scraping, machine learning, and custom logic to deliver high-quality summaries, sentiment analysis, and categorization, with both automated and human-in-the-loop workflows.

---

## Features

### News Fetching & Processing
- **Dual News Pipelines**:
    - **General News**: Fetches articles from NewsAPI using customizable keywords and date ranges, ideal for tracking broad market trends and topics.
    - **Fund-Specific News**: Fetches targeted news for a predefined list of investment funds using the MarketAux API, providing focused intelligence on specific assets.
- **Advanced Web Scraping**: Utilizes Playwright and Trafilatura to extract full article content from URLs where APIs only provide snippets, ensuring complete data for analysis.
- **Human Screening**: Before summarization, users can review, approve, or reject each fetched article through an interactive web interface. This critical step ensures only the highest-quality, most relevant articles are included in the final briefing.
- **Article Deduplication**: Employs string similarity checks to automatically remove duplicate or near-duplicate articles, keeping the briefing concise and non-redundant.
- **Sentiment Analysis**: Analyzes the sentiment of each article using NLTK's VADER, classifying them as positive, neutral, or negative for a quick snapshot of market tone.
- **AI-Powered Summarization**: Leverages Google's Gemini AI to generate concise summaries, extract key bullet points, categorize articles by topic (e.g., "Regulatory & Policy," "Corporate Action"), and identify mentioned companies.

### Output Generation
- **Multi-format Briefings**: Generates polished, professional briefings in Markdown (`.md`), HTML (`.html`), and PDF (`.pdf`) formats, suitable for sharing, archiving, or further editing.
- **Dynamic Introductory Summary**: Each briefing includes an AI-generated introduction that synthesizes the key themes and trends from the selected articles.
- **Fund Performance Module**: Automatically incorporates and displays up-to-date performance data for relevant funds, adding critical context to the news.

### Web Interface (Flask)
- **Dashboard**: A central hub displaying recent briefings and a snapshot of fund performance data.
- **Generate Briefings**: A modern, responsive web form to trigger the news pipeline. Select look-back days, enter custom keywords, and initiate the fetching process.
- **Interactive Human Screening**: A step-by-step UI to review and approve/reject articles before they are processed, giving you full control over the briefing's content.
- **Fund News Center**: View all recently fetched articles related to your tracked funds and create custom briefings directly from this curated list.
- **View & Manage Briefings**: Browse a comprehensive list of all generated briefings. Preview, download, or delete any briefing file (Markdown, HTML, or PDF) with a single click.
- **Configuration Management**: Edit API keys and other settings via a secure web form. Reset to default settings with one click.

### Configuration & Customization
- **Centralized Settings**: All API keys, keywords, and funds are stored in `config.json` and can be managed via the web UI.
- **Default & Custom Configs**: The system uses a `config_default.json` as a fallback, ensuring robust operation.

### Error Handling & Robustness
- **Graceful Error Handling**: Resilient to API failures, empty responses, and unexpected data formats, providing clear feedback to the user.
- **Comprehensive Testing**: A suite of `pytest` unit tests for all major components ensures reliability and maintainability.

---

## Project Structure

```
├── app.py                  # Flask app entry point
├── main.py                 # CLI entry point for the core pipeline
├── config.py               # Loads configuration from files and environment
├── config.json             # User-editable configuration (API keys, funds, keywords)
├── config_default.json     # Default configuration fallback
├── requirements.txt        # Python dependencies
├── news_fetcher.py         # Fetches general articles from NewsAPI
├── fund_news_fetcher.py    # Fetches fund-specific news from MarketAux
├── fund_news_scraper.py    # Coordinates scraping of full article content
├── news_scraper/           # Web scraping module
│   ├── playwright_layer.py # Manages browser automation with Playwright
│   └── extractor.py        # Extracts content using Trafilatura
├── deduplicator.py         # Deduplicates articles based on similarity
├── human_screen.py         # Logic for the human screening process
├── scorer.py               # Sentiment and keyword scoring
├── summariser.py           # Summarization and metadata extraction (Gemini)
├── reporter.py             # Assembles the structured briefing data
├── formatter.py            # Generates Markdown, HTML, and PDF outputs
├── fund_info.py            # Manages fetching and updating fund data
├── app/                    # Flask web application package
│   ├── __init__.py         # Flask app factory
│   ├── routes.py           # Defines all web routes and API endpoints
│   ├── forms.py            # WTForms definitions for the web UI
│   ├── utils.py            # Utility functions for the web app
│   ├── templates/          # Jinja2 HTML templates for the front end
│   └── static/             # Static assets (CSS, JS, images)
├── output/                 # Default directory for generated briefings
├── data/                   # Data files (fund lists, cached news, etc.)
├── tests/                  # Unit and integration tests
└── README.md               # This file
```

---

## Installation

1.  **Clone the repository**:
    ```sh
    git clone https://github.com/your-repo/automated-news-briefing.git
    cd automated-news-briefing
    ```

2.  **Create and activate a virtual environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Python dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4.  **Install Playwright browsers**:
    After installing the pip packages, you must install the browser binaries for Playwright:
    ```sh
    playwright install
    ```

5.  **Set up configuration**:
    - Rename `config_default.json` to `config.json`.
    - Edit `config.json` to add your API keys:
        - `NEWS_API_KEY`: Your key from [NewsAPI](https://newsapi.org/).
        - `GOOGLE_API_KEY`: Your key for [Google Generative AI](https://cloud.google.com/).
        - `MARKETAUX_API_TOKEN`: Your token from [MarketAux](https://www.marketaux.com/).
    - It is recommended to use environment variables for keys in production. The app will prioritize environment variables over `config.json`.

---

## Usage

### 1. Web App (Recommended)

The web interface provides access to all features, including the interactive human screening process.

Start the web server:
```sh
python app.py
```

Navigate to `http://127.0.0.1:5000` in your browser.

- **Generate Briefing**: Use the form on the "Generate" page to fetch news by keywords. You will then be guided through the human screening process.
- **Update Fund News**: Go to the "Fund News" page and click the "Update" button to fetch the latest articles for your tracked funds.
- **Create Custom Briefing**: From the "Fund News" page, select specific articles and generate a custom briefing.
- **Manage Configuration**: Use the "Configure" page to manage API keys.

### 2. Command-Line

The CLI is suitable for automated runs of the general news pipeline. Note that the CLI does not support the human screening step.

**Run the pipeline**:
```sh
# Generate a briefing with news from the last 7 days
python main.py ./output 7
```

**Update fund news**:
```sh
# Fetch the latest fund news from MarketAux
python main.py --update-fund-news
```

---

## Testing

Run all unit tests using `pytest`:
```sh
pytest
```
Or use the provided script:
```sh
python run_tests.py
```

---

## Dependencies

- **Flask**: Web framework
- **Playwright**: Advanced web scraping and browser automation
- **google-generativeai**: Google Gemini API for summarization
- **requests**, **httpx**: HTTP clients for API communication
- **trafilatura**, **BeautifulSoup4**: Web content extraction
- **NLTK**, **textblob**: Sentiment analysis
- **WeasyPrint**: PDF generation from HTML
- **pandas**: Data manipulation, used for fund data
- **pytest**: Testing framework

See `requirements.txt` for the full list of dependencies.

---

## Contact

For questions, feature requests, or contributions, please open an issue or contact [alexios0905@gmail.com](mailto:alexios0905@gmail.com).
