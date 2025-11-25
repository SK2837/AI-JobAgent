import asyncio
from app.services.scraper import ScraperFactory

async def test_linkedin_scraper():
    # Use a known public job URL or a generic one (might fail if expired, but good for testing structure)
    # This is a sample URL, might need a fresh one for real success
    url = "https://www.linkedin.com/jobs/view/software-engineer-at-tech-corp-1234567890" 
    
    print(f"Testing Scraper for URL: {url}")
    scraper = ScraperFactory.get_scraper(url)
    print(f"Using Scraper: {type(scraper).__name__}")
    
    try:
        # Note: This might fail without a real URL or if LinkedIn blocks it. 
        # For this test, we just want to see it attempt to run.
        # Ideally we'd use a mock page or a very stable URL.
        job = await scraper.scrape_job(url)
        print(f"Scraped Job: {job.title} at {job.company}")
    except Exception as e:
        print(f"Scraping failed (expected if URL is invalid/blocked): {e}")

if __name__ == "__main__":
    asyncio.run(test_linkedin_scraper())
