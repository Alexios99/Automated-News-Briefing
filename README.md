# Automated News Briefing

A dual-pipeline news system for small investment teams: fetch, scrape, dedupe, score, **human-review**, and publish concise briefs (Markdown, HTML, PDF).

> Built for sustainable-finance use cases, but generic enough for any domain with well-chosen sources/keywords.

---

## TL;DR

- **Two pipelines:** (1) general market keywords, (2) fund-specific tracking  
- **Full-text:** Playwright + Trafilatura to extract article bodies when APIs return snippets  
- **Quality control:** human screening UI + automatic de-duplication  
- **Analysis:** sentiment, topic tags, company mentions, optional LLM summary  
- **Outputs:** ready-to-share briefings in `.md`, `.html`, `.pdf`  
- **Run modes:** web app (Flask) or CLI  
- **Config:** **environment variables first**, optional `config.json` fallback

---

## Screens (at a glance)

- Dashboard with latest briefs and fund snapshot  
- Human screening flow (approve/reject)  
- Briefing viewer + download (MD/HTML/PDF)

_Add screenshots or a short GIF here (./images/)._

---

## Architecture

```mermaid
flowchart TD
  A[Sources: NewsAPI + MarketAux + URLs] --> B[Fetch]
  B --> C[Scrape full text (Playwright + Trafilatura)]
  C --> D[Deduplicate]
  D --> E[Score (sentiment, topics, entities)]
  E --> F[LLM summariser (optional)]
  F --> G[Reporter (structured brief data)]
  G --> H[Formatter (MD/HTML/PDF)]
  H --> I[Web UI: review + download]
  D <-->|human-in-the-loop| I
