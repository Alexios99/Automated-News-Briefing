# Automated News Briefing

## Overview

Automated News Briefing is a platform for fetching, analyzing, and summarizing news articles, designed for institutional investors and professionals. It provides concise, actionable insights through briefings in Markdown, HTML, and PDF formats. The system integrates APIs, machine learning, and custom logic to deliver high-quality summaries, sentiment analysis, and categorization, with both automated and human-in-the-loop workflows.

---

## Features

### News Fetching & Processing
- **Automated Article Collection**: Fetches news articles from NewsAPI using customizable keywords and date ranges, ensuring coverage of relevant topics in sustainable finance and related fields.
- **Human Screening**: Before summarization, users can review, approve, or reject each fetched article. This step ensures only high-quality, relevant articles are included in the final briefing. Screening can be performed via the command line or the web interface.
- **Article Deduplication**: Uses string similarity checks to automatically remove duplicate or near-duplicate articles, keeping the briefing concise and non-redundant.
- **Sentiment Analysis**: Analyzes the sentiment of each article using VADER (via NLTK), classifying them as positive, neutral, or negative for quick insight into market tone.
- **Summarization & Metadata Extraction**: Utilizes Google Generative AI (Gemini) to generate concise summaries, extract three key bullet points, categorize articles by topic (e.g., "Regulatory & Policy", "Corporate Action"), and identify mentioned companies.

### Output Generation
- **Multi-format Briefings**: Generates briefings in Markdown (`.md`), HTML (`.html`), and PDF (`.pdf`) formats, suitable for sharing, archiving, or further editing.
- **Introductory Summary**: Each briefing includes an automatically generated introduction summarizing the week's trends and key themes.

### Web Interface (Front End)
- **Generate Briefings**: Use a modern, responsive web form to select look-back days, choose funds, and enter custom keywords. Trigger the full news pipeline and receive instant feedback on the generation process.
- **View & Manage Briefings**: Browse a list of all generated briefings. Preview the first lines of Markdown or HTML files directly in the browser. Download or delete any briefing file (Markdown, HTML, or PDF) with a single click.
- **Configuration Management**: Edit the list of funds and keywords via an interactive table. Upload a new configuration file, download the current configuration, or reset to default—all from the web UI.
- **User Experience**: Built with Bootstrap for a clean, professional look. Includes loading spinners, success/error alerts, and form validation for a smooth user experience.

### Configuration & Customization
- **Flexible Settings**: All keywords, funds, and other settings are stored in `config.json` and can be edited via the web UI or by directly modifying the file.
- **Default & Custom Configs**: Easily reset to default settings or upload/download custom configurations for different use cases.

### Error Handling & Robustness
- **Graceful Error Handling**: Handles API failures, empty responses, and unexpected data formats, providing clear feedback to the user.
- **Testing**: Comprehensive unit tests for all major components ensure reliability and maintainability.

---

## Project Structure

```
├── app.py                  # Flask app entry point
├── main.py                 # CLI entry point for the pipeline
├── config.py               # Loads configuration and API keys
├── config.json             # User-editable configuration (funds, keywords)
├── config_default.json     # Default configuration
├── news_fetcher.py         # Fetches articles from NewsAPI
├── deduplicator.py         # Deduplicates articles
├── human_screen.py         # Human screening logic
├── scorer.py               # Sentiment and keyword scoring
├── summariser.py           # Summarization logic (Gemini)
├── reporter.py             # Builds the structured briefing
├── formatter.py            # Generates Markdown, HTML, PDF outputs
├── run_tests.py            # Test runner
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── app/                    # Flask web app
│   ├── __init__.py         # Flask app factory
│   ├── routes.py           # Web routes and API endpoints
│   ├── forms.py            # WTForms for web UI
│   ├── utils.py            # Web utility functions
│   ├── templates/          # Jinja2 HTML templates
│   └── static/             # Static files (generated briefings)
├── output/                 # Output directory for generated briefings
├── data/                   # Data files (funds, etc.)
├── images/                 # Images (e.g., logo)
├── tests/                  # Unit tests
└── ...
```

---

## Installation

### Option 1: Docker (Recommended)

1. **Install Docker Desktop**: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
2. **Get API Keys**:
   - NewsAPI: [https://newsapi.org/](https://newsapi.org/)
   - Google Generative AI: [https://cloud.google.com/](https://cloud.google.com/)
3. **Clone and Run**:
   ```sh
   git clone https://github.com/your-repo/automated-news-briefing.git
   cd automated-news-briefing
   ./run.sh
   ```
4. **Follow prompts** to set up API keys and run the app.

See [README-Docker.md](README-Docker.md) for details.

### Option 2: Local Python Setup

1. **Install Python 3.8+**
2. **Clone the repository**
   ```sh
   git clone https://github.com/your-repo/automated-news-briefing.git
   cd automated-news-briefing
   ```
3. **Create and activate a virtual environment**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
4. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
5. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   NEWS_API_KEY=your_news_api_key
   GOOGLE_API_KEY=your_google_api_key
   FLASK_SECRET_KEY=your_flask_secret
   ```

---

## Usage

### 1. Command-Line Pipeline

Run the pipeline to generate a briefing:
```sh
python main.py [output_dir] [from_days_ago]
```
- `output_dir`: Directory for output files (default: `./output`)
- `from_days_ago`: How many days back to fetch news (default: `3`)

Example:
```sh
python main.py ./output 7
```

### 2. Flask Web App

Start the web server:
```sh
python app.py
```

- Visit [http://localhost:5000](http://localhost:5000) in your browser.
- **Generate Briefing**: Use the form to select look-back days, funds, and custom keywords.
- **View Briefings**: Browse, preview, download, or delete generated briefings.
- **Configure**: Edit, upload, download, or reset configuration (funds, keywords, etc.).

---

## Configuration

- **config.json**: Stores user-editable settings (funds, keywords, etc.).
- **config_default.json**: Default settings (restored via web UI or CLI).
- **Web UI**: Edit, upload, or download config from the "Configure" page.

---

## Output

- **Markdown**: `output/briefing_<date>.md`
- **HTML**: `output/briefing_<date>.html`
- **PDF**: `output/briefing_<date>.pdf`

---

## Testing

Run all unit tests:
```sh
pytest
```
Or use the provided script:
```sh
python run_tests.py
```

Test coverage includes:
- Article deduplication
- News fetching
- Human screening
- Summarization
- Output generation
- Briefing structure

---

## Dependencies

- `Flask`, `Flask-WTF`, `WTForms` — Web app and forms
- `requests` — HTTP requests
- `textblob`, `nltk` — Sentiment analysis
- `google-generativeai` — Article summarization
- `markdown2` — Markdown to HTML
- `weasyprint` — HTML to PDF
- `pytest` — Unit testing
- `beautifulsoup4`, `lxml`, `selenium` — (Optional, for advanced scraping)

See `requirements.txt` for the full list.

---

## Contact

For questions or contributions, contact [alexios0905@gmail.com](mailto:alexios0905@gmail.com).
