import asyncio
from app.services.scraper import MockScraper
from app.services.resume import ResumeBuilder
from app.services.submitter import ApplicationSubmitter
from app.models import Job, Application

async def test_services():
    print("Testing Scraper...")
    scraper = MockScraper()
    job = await scraper.scrape_job("http://example.com/job")
    print(f"Scraped: {job.title}")

    print("Testing Resume Builder...")
    resume = ResumeBuilder()
    tailored = await resume.tailor_resume("My Resume", job.description)
    print(f"Tailored: {tailored}")

    print("Testing Submitter...")
    submitter = ApplicationSubmitter()
    app = Application(job_id=1, resume_id=1)
    status = await submitter.submit_application(app)
    print(f"Status: {status}")

if __name__ == "__main__":
    asyncio.run(test_services())
