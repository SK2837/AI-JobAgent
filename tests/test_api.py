import os

# Mock OpenAI key to prevent startup errors if not present
# MUST be done before importing app.main
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "sk-mock-key"

from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app
from app.models import ApplicationStatus

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the AI Job Agent API"}

@patch("app.main.ScraperFactory.get_scraper")
def test_scrape_job(mock_get_scraper):
    # Mock the scraper instance and its scrape_job method
    mock_scraper_instance = AsyncMock()
    # Ensure scrape_job return value has the attributes we need
    mock_job = AsyncMock()
    mock_job.title = "Mock Job"
    mock_job.company = "Mock Corp"
    mock_job.description = "Mock Desc"
    mock_job.url = "http://mock.url"
    mock_job.source = "mock"
    
    # When scrape_job is awaited, it should return mock_job
    mock_scraper_instance.scrape_job.return_value = mock_job
    
    mock_get_scraper.return_value = mock_scraper_instance

    response = client.post("/jobs/scrape", json={"url": "http://mock.url"})
    assert response.status_code == 200, f"Response: {response.text}"
    data = response.json()
    assert data["title"] == "Mock Job"
    assert data["company"] == "Mock Corp"

@patch("app.main.resume_builder.tailor_resume", new_callable=AsyncMock)
def test_tailor_resume(mock_tailor):
    mock_tailor.return_value = "Tailored Resume Content"
    
    response = client.post("/resumes/tailor", json={
        "base_resume": "Base Resume",
        "job_description": "Job Desc"
    })
    assert response.status_code == 200, f"Response: {response.text}"
    data = response.json()
    assert data["content"] == "Tailored Resume Content"

@patch("app.main.submitter.submit_application", new_callable=AsyncMock)
def test_submit_application(mock_submit):
    mock_submit.return_value = ApplicationStatus.SUBMITTED
    
    # 1. Create Job (Mocked Scraper)
    with patch("app.main.ScraperFactory.get_scraper") as mock_get_scraper:
        mock_scraper_instance = AsyncMock()
        mock_job = AsyncMock()
        mock_job.title = "Job for App"
        mock_job.company = "Corp"
        mock_job.description = "Desc"
        mock_job.url = "http://app.url"
        mock_job.source = "mock"
        mock_scraper_instance.scrape_job.return_value = mock_job
        mock_get_scraper.return_value = mock_scraper_instance
        
        job_resp = client.post("/jobs/scrape", json={"url": "http://app.url"})
        assert job_resp.status_code == 200, f"Job Create Failed: {job_resp.text}"
        job_id = job_resp.json()["id"]

    # 2. Create Resume (Mocked Builder)
    with patch("app.main.resume_builder.tailor_resume", new_callable=AsyncMock) as mock_tailor:
        mock_tailor.return_value = "Resume for App"
        resume_resp = client.post("/resumes/tailor", json={"base_resume": "Base", "job_description": "Desc"})
        resume_id = resume_resp.json()["id"]

    # 3. Submit Application
    response = client.post("/applications/submit", json={"job_id": job_id, "resume_id": resume_id})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "submitted"
