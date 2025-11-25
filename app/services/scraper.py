from abc import ABC, abstractmethod
from ..models import Job
from datetime import datetime

class BaseScraper(ABC):
    @abstractmethod
    async def scrape_job(self, url: str) -> Job:
        pass

class MockScraper(BaseScraper):
    async def scrape_job(self, url: str) -> Job:
        # Simulate network delay
        import asyncio
        await asyncio.sleep(1)
        
        return Job(
            title="Software Engineer",
            company="Tech Corp",
            description="We are looking for a software engineer...",
            url=url,
            source="mock",
            created_at=datetime.now()
        )

class ScraperFactory:
    @staticmethod
    def get_scraper(url: str) -> BaseScraper:
        if "linkedin.com" in url:
            from .scrapers.linkedin import LinkedInScraper
            return LinkedInScraper()
        return MockScraper()

