# Automated News Briefing

## Quick Start

1. **Download the Project**
   - **Option A: Download ZIP**
     - Go to the [GitHub repository page](https://github.com/Alexios99/automated-news-briefing).
     - Click the green "Code" button, then "Download ZIP".
     - Unzip the downloaded file on your computer.
   - **Option B: Use Git (for advanced users)**
     ```sh
     git clone https://github.com/Alexios99/automated-news-briefing.git
     cd automated-news-briefing
     ```

2. **Run the App**
   - **Windows:** Double-click `start_app.bat` to launch the app. (It will set up everything for you.)
   - **Mac:** Open Terminal, run `chmod +x start_app.command` once to make it executable, then double-click `start_app.command` to launch the app.

The app will open in your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

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

## Getting Started

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

### Step 1: Download the Project

- **Option A: Download ZIP**
  - Go to the [GitHub repository page](https://github.com/Alexios99/automated-news-briefing).
  - Click the green "Code" button, then "Download ZIP".
  - Unzip the downloaded file on your computer.

- **Option B: Use Git (for advanced users)**
  ```sh
  git clone https://github.com/Alexios99/automated-news-briefing.git
  cd automated-news-briefing
  ```

### Step 2: Run the Setup Script

The only file you need to run is `setup.py`. This will handle everything for you.

- **On Windows**:
  - Find the `setup.py` file and double-click it.
  - If that doesn't work, open Command Prompt, navigate to the project folder, and run: `python setup.py`

- **On macOS / Linux**:
  - Open your Terminal.
  - Navigate to the project folder.
  - Run the command: `python3 setup.py`

The script will:
1.  Check if your Python version is compatible.
2.  Create a dedicated virtual environment for the project.
3.  Install all the necessary packages.
4.  Install the required web scraping browsers (this might take a moment).
5.  Ask you to enter your API keys, which it will save for you.

### Step 3: Use the Web App

Once the setup script is finished, it will automatically launch the web application.

- Your web browser should open to `http://127.0.0.1:5000`.
- If it doesn't, you can open your browser and navigate to that address manually.
- You can now use the web interface to generate and manage your news briefings!
- To stop the application, simply close the terminal or command prompt window that the script is running in.

---

## How to Run the App Again

Once you've completed the initial setup, you don't need to run `setup.py` again. To launch the application in the future, simply run the `app.py` script from within the virtual environment:

- **On Windows**:
  ```sh
  venv\\Scripts\\activate
  python app.py
  ```

- **On macOS / Linux**:
  ```sh
  source venv/bin/activate
  python app.py
  ```

---

## Troubleshooting

**Python not found:**
- Make sure Python 3.8 or higher is installed. Download from [python.org](https://www.python.org/downloads/).

**App won’t open in browser:**
- Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000) manually.

**Port 5000 already in use:**
- Close any other app using that port, or change the port in `app.py` (advanced users).

**API key errors:**
- Double-check your API keys in `config.json`. You can re-run the setup script to enter them again.

**Other issues:**
- Check for error messages in the terminal window. If you need help, see the Contact section below.

---

## FAQ

**Q: Do I need an internet connection?**
A: Yes, for setup and to fetch news.

**Q: Where do I get API keys?**
A: See the instructions in the README above for NewsAPI, Google Generative AI, and MarketAux.

**Q: How do I update the app?**
A: Download the latest version from GitHub and replace your files (except your `config.json` and `output/` folder).

**Q: How do I uninstall?**
A: Delete the project folder. Optionally, delete the `venv` folder to remove the virtual environment.

**Q: Can I use the app on another computer?**
A: Yes! Just copy the project folder and run the startup script on the new machine.

---

## Contact / Support

- For help, open an issue on [GitHub](https://github.com/Alexios99/automated-news-briefing/issues) or email [alexios0905@gmail.com](mailto:alexios0905@gmail.com).
- Please include any error messages or screenshots to help diagnose your issue.
