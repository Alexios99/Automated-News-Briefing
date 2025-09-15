# Automated News Briefing

A dual-pipeline news system for small investment teams. Fetch, scrape, dedupe, score, **human review**, then publish concise briefs in Markdown, HTML, or PDF.

> Built for sustainable finance use cases, but generic enough for any domain with well chosen sources and keywords.

---

## TL;DR

- Two pipelines: (1) general market keywords, (2) fund specific tracking  
- Full text: Playwright + Trafilatura to extract article bodies when APIs return snippets  
- Quality control: human screening UI and automatic de-duplication  
- Analysis: sentiment, topic tags, company mentions, optional LLM summariser  
- Outputs: ready to share briefings in `.md`, `.html`, `.pdf`  
- Run modes: web app (Flask) or CLI  
- Config: **environment variables first**, optional `config.json` fallback

---

## Screens

- Dashboard with latest briefs and fund snapshot  
- Human screening flow to approve or reject articles  
- Briefing viewer plus download (MD, HTML, PDF)

_Add screenshots or a short GIF to `./images/` and reference them here._

---

## Architecture

``` mermaid
flowchart TD
  A["Sources (NewsAPI, MarketAux, URLs)"] --> B["Fetch"]
  B --> C["Scrape full text (Playwright & Trafilatura)"]
  C --> D["Deduplicate"]
  D --> E["Score (sentiment, topics, entities)"]
  E --> F["LLM summariser (optional)"]
  F --> G["Reporter (structured brief)"]
  G --> H["Formatter (Markdown / HTML / PDF)"]
  H --> I["Web UI (review & download)"]
  D -->|human in the loop| I
```

**Key modules**: `news_fetcher.py`, `fund_news_fetcher.py`, `news_scraper/`, `deduplicator.py`, `scorer.py`, `summariser.py`, `reporter.py`, `formatter.py`, `app/` (Flask).

---

## Quickstart

### Option A: Docker (recommended)

1. Create a `.env` file in the project root:

```bash
NEWSAPI_KEY=your_key
GEMINI_API_KEY=your_key   # optional
MARKETAUX_KEY=your_key    # optional, used for fund specific news
SECRET_KEY=change-me
BRIEF_LOOKBACK_DAYS=1
OUTPUT_DIR=./output
```

2. Build and run:

```bash
docker build -t automated-news-briefing .
docker run --rm -p 5000:5000 --env-file .env -v "$PWD/output:/app/output" automated-news-briefing
```

3. Open `http://127.0.0.1:5000` and generate a briefing.

### Option B: Local Python

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

> First run may download Playwright browsers. If needed run `playwright install` after activating the venv.

---

## Configuration

**Environment variables (preferred):**

* `NEWSAPI_KEY` – API key
* `GEMINI_API_KEY` – API key for summaries (optional)
* `MARKETAUX_KEY` – API key for fund specific news (optional)
* `SECRET_KEY` – Flask session key
* `BRIEF_LOOKBACK_DAYS` – integer days to search back. Default 1
* `OUTPUT_DIR` – where generated briefs are written. Default `./output`

**File fallback**: `config.json` with the same fields.
At runtime, **environment variables override file values**. A `config_default.json` provides safe defaults.

> Do not commit real keys. Keep secrets in your local `.env`. Commit an `.env.example` only.

---

## Usage

### Web app (human in the loop)

* **Generate Briefing**: choose look back window and keywords → fetch → screen → summarise → export
* **Fund News Centre**: view recent fund linked articles and create a fund only brief
* **Briefings**: list, preview, and download all generated files

### CLI

```bash
python main.py --keywords "green hydrogen, offshore wind" --days 1 --no-summariser
```

Outputs land in `./output/` by default.

---

## Outputs

* `brief_YYYYMMDD_HHMM.md`
* `brief_YYYYMMDD_HHMM.html`
* `brief_YYYYMMDD_HHMM.pdf`

Each brief includes:

* Intro summary
* Per article bullets with sentiment, topics, entities, and source links
* A short closing section with counts and coverage

---

## Project layout

```
app.py                 # Flask entry
main.py                # CLI entry
config.py              # loads from env + file
config_default.json    # defaults only
news_fetcher.py        # general NewsAPI pipeline
fund_news_fetcher.py   # fund specific pipeline (e.g. MarketAux)
news_scraper/          # Playwright + Trafilatura
deduplicator.py        # URL canonicalisation + similarity
scorer.py              # sentiment, topics, entities
summariser.py          # Gemini summariser (optional)
reporter.py            # structured brief object
formatter.py           # Markdown, HTML, PDF
app/                   # Flask routes, templates, static
data/                  # cached metadata (local only)
output/                # generated briefs (local only)
tests/                 # pytest
```

---

## Testing

```bash
pytest -q
```

Consider adding:

* Contract tests for NewsAPI and MarketAux with mocks
* Golden file test for HTML formatting
* `pip-audit` or `safety` and `bandit` in CI

---

## Security and compliance

* Respect `robots.txt` and set per domain rate limits and back off
* Keep `SECRET_KEY` and API keys in environment variables
* Redact secrets in logs and avoid storing full article bodies beyond what is needed
* The LLM summariser is optional. Disable it in regulated environments or when offline reproducibility is required

---

## Roadmap

* Async fetch with retry using `httpx` and `tenacity`
* Improved dedupe using URL canonicalisation plus embeddings or MinHash
* SQLite cache for articles and briefs
* Scheduler for daily brief generation
* Basic metrics page in the UI
* Docker image and GitHub Release `v0.1.0`

---

## For reviewers and recruiters

* Clear separation of concerns: fetch → scrape → dedupe → score → summarise → report → format
* Human in the loop before publishing, which reduces false positives
* Deterministic runs without LLM via `--no-summariser`
* Shareable artefacts in MD, HTML, and PDF


