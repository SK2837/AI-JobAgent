# AI Job Agent Implementation Plan

## Goal
Build an AI agent that scrapes jobs, modifies resumes, and auto-submits applications using Postgres, FastAPI, LangChain, and Tool Calling.

## User Review Required
- **LLM Provider**: Which LLM provider to use? (Assuming OpenAI or Anthropic for now, configurable via env vars).
- **Scraping Targets**: Which sites to scrape? (Note: scraping major sites like LinkedIn is complex and often blocked; will implement a generic structure).
- **Submission Method**: How to submit? (Email, Form filling, API?).

## Proposed Changes

### Project Structure
```
ai-job-agent/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point
│   ├── core/                # Config, Database
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── api/                 # API routes
│   └── services/
│       ├── scraper.py       # Scraping logic
│       ├── resume_agent.py  # LangChain agent for resume
│       └── submitter.py     # Submission logic
├── alembic/                 # DB Migrations
├── requirements.txt         # Dependencies
├── .env.example             # Environment variables template
└── task.md                  # Task tracking
```

### Tech Stack
- **Language**: Python 3.11
- **Web Framework**: FastAPI
- **Database**: PostgreSQL (using `psycopg2` and `SQLAlchemy`)
- **AI/LLM**: LangChain (for orchestration and tool calling)
- **Scraping**: BeautifulSoup4 / Playwright (if needed for dynamic content)

### Database Schema (Preliminary)
- **Job**: `id`, `title`, `description`, `source_url`, `status` (new, processing, applied)
- **Resume**: `id`, `content` (text/json), `version_name`
- **Application**: `id`, `job_id`, `resume_id`, `status`, `submitted_at`

## Verification Plan
### Automated Tests
- Unit tests for Resume Agent logic (mocking LLM).
- API endpoint tests using `TestClient`.

### Manual Verification
- Run the scraper on a sample target.
- Trigger the resume customization for a specific job.
- Verify the output resume.
