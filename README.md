# AI Job Agent 🤖

An intelligent automation system that scrapes job postings, tailors resumes using AI, and automates job application submissions.

## 📋 Overview

AI Job Agent is a FastAPI-based application that leverages LangChain, OpenAI, and Playwright to streamline the job application process. It consists of three core services that work together to automate job hunting:

1. **Job Scraper**: Extracts job details from various platforms (LinkedIn, Indeed, etc.)
2. **Resume Tailoring**: Uses LLM to customize resumes for specific job descriptions
3. **Application Submitter**: Automates form filling and submission (LinkedIn Easy Apply)

## ✨ Features

- 🔍 **Intelligent Job Scraping**: Playwright-based scrapers for dynamic content
- 🤖 **AI-Powered Resume Customization**: LangChain + OpenAI GPT-3.5 integration
- 📝 **Automatic Application Submission**: Browser automation with Playwright
- 💾 **Database Persistence**: SQLAlchemy with PostgreSQL/SQLite support
- 🚀 **RESTful API**: FastAPI with automatic interactive documentation
- 🛡️ **Robust Error Handling**: Graceful degradation when services unavailable
- 🧪 **Comprehensive Testing**: Unit and integration tests with pytest

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern async web framework
- **LangChain**: LLM orchestration framework
- **OpenAI API**: GPT-3.5-turbo for resume tailoring
- **Playwright**: Browser automation for scraping/submission
- **SQLAlchemy**: ORM for database operations

### Database
- **PostgreSQL**: Production database (recommended)
- **SQLite**: Development/testing database

### Libraries
- **BeautifulSoup4**: HTML parsing
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

## 📦 Installation

### Prerequisites
- Python 3.10+
- PostgreSQL (optional, SQLite works for development)
- OpenAI API key

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai-job-agent
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Playwright browsers**
```bash
playwright install chromium
```

5. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

Required environment variables:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
OPENAI_API_KEY=sk-your-openai-api-key
```

6. **Initialize database**
```bash
# Database tables are created automatically on first run
# Or manually with:
python -c "from app.database import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine)"
```

## 🚀 Usage

### Start the server

**Development:**
```bash
uvicorn app.main:app --reload
```

**Production:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### API Documentation

Once running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### 1. Scrape Job Posting
```bash
POST /jobs/scrape
Content-Type: application/json

{
  "url": "https://www.linkedin.com/jobs/view/123456"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Senior Software Engineer",
  "company": "Tech Corp",
  "description": "Job description...",
  "url": "https://...",
  "source": "linkedin",
  "created_at": "2025-11-24T12:00:00"
}
```

#### 2. Tailor Resume
```bash
POST /resumes/tailor
Content-Type: application/json

{
  "base_resume": "Your base resume content...",
  "job_description": "Target job description..."
}
```

**Response:**
```json
{
  "id": 1,
  "content": "Tailored resume content optimized for the job...",
  "base_resume": false,
  "created_at": "2025-11-24T12:00:00"
}
```

#### 3. Submit Application
```bash
POST /applications/submit
Content-Type: application/json

{
  "job_id": 1,
  "resume_id": 1
}
```

**Response:**
```json
{
  "id": 1,
  "job_id": 1,
  "resume_id": 1,
  "status": "submitted",
  "created_at": "2025-11-24T12:00:00"
}
```

## 📁 Project Structure

```
ai-job-agent/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application & endpoints
│   ├── database.py             # Database configuration
│   ├── models.py               # SQLAlchemy models
│   ├── agent.py                # LangChain agent setup
│   └── services/
│       ├── __init__.py
│       ├── scraper.py          # Base scraper & factory
│       ├── resume.py           # LLM resume builder
│       ├── submitter.py        # Application submitter
│       └── scrapers/
│           ├── __init__.py
│           └── linkedin.py     # LinkedIn-specific scraper
├── tests/
│   ├── test_basic.py           # Service unit tests
│   ├── test_scraper.py         # Scraper tests
│   ├── test_resume_llm.py      # LLM integration tests
│   └── test_api.py             # API endpoint tests
├── requirements.txt
├── .env.example
└── README.md
```

## 🔄 Implementation Workflow

### 1. Job Scraping Flow
```
User provides URL
    ↓
ScraperFactory selects appropriate scraper
    ↓
Playwright launches browser → Navigates to URL
    ↓
BeautifulSoup parses HTML → Extracts data
    ↓
Job saved to database → Returns Job object
```

### 2. Resume Tailoring Flow
```
User provides base resume + job description
    ↓
ResumeBuilder initializes ChatOpenAI
    ↓
Prompt template formats input
    ↓
LLM generates tailored resume
    ↓
Resume saved to database → Returns Resume object
```

### 3. Application Submission Flow
```
User provides job_id + resume_id
    ↓
Application record created (status: PENDING)
    ↓
ApplicationSubmitter routes to correct submitter
    ↓
LinkedIn: Launch browser → Login → Navigate to job → Click Easy Apply
    ↓
Fill form fields → Submit → Update status
```

## 🧪 Testing

Run all tests:
```bash
DATABASE_URL=sqlite:///./test.db pytest tests/
```

Run specific test file:
```bash
DATABASE_URL=sqlite:///./test.db pytest tests/test_api.py -v
```

With coverage:
```bash
DATABASE_URL=sqlite:///./test.db pytest --cov=app tests/
```

## ⚙️ Configuration

### Database Options

**PostgreSQL (Production):**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/jobagent
```

**SQLite (Development):**
```env
DATABASE_URL=sqlite:///./dev.db
```

### Scraper Configuration

The `ScraperFactory` automatically selects scrapers based on URL:
- Contains `linkedin.com` → `LinkedInScraper`
- Default → `MockScraper`

### LLM Configuration

Edit `app/services/resume.py` to customize:
```python
self.llm = ChatOpenAI(
    temperature=0.7,        # Creativity (0-1)
    model="gpt-3.5-turbo"  # Model selection
)
```

Available models:
- `gpt-3.5-turbo` (faster, cheaper)
- `gpt-4` (higher quality, slower)

## 🔒 Security Notes

- Never commit `.env` file or API keys to version control
- Use environment variables for all sensitive data
- Implement rate limiting for production deployments
- Consider using background tasks (Celery/Arq) for long-running operations
- Add authentication/authorization for production API

## 🚧 Current Limitations

1. **LinkedIn Scraper**: Only handles public job pages (no authentication)
2. **Application Submitter**: Skeleton implementation (requires manual login setup)
3. **Error Recovery**: Limited retry logic for network failures
4. **Rate Limiting**: No built-in request throttling

## 🎯 Future Enhancements

- [ ] Complete LinkedIn Easy Apply automation with cookie-based auth
- [ ] Add Indeed, Glassdoor scrapers
- [ ] Implement background task queue (Celery)
- [ ] Add job matching/filtering based on criteria
- [ ] Email notifications for application status
- [ ] Web UI dashboard for monitoring
- [ ] Export applications to CSV/PDF
- [ ] Multi-tenant support with user authentication

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [LangChain](https://python.langchain.com/) - LLM orchestration
- [Playwright](https://playwright.dev/) - Browser automation
- [OpenAI](https://openai.com/) - GPT models

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Contact: [your-email@example.com]

---

**Note**: This tool is for educational purposes. Always respect websites' Terms of Service and robots.txt when scraping. Use responsibly and ethically.
