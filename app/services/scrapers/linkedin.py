from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from ..scraper import BaseScraper
from ...models import Job
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class LinkedInScraper(BaseScraper):
    async def scrape_job(self, url: str) -> Job:
        async with async_playwright() as p:
            # Launch browser (headless=True by default)
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            
            try:
                logger.info(f"Navigating to {url}")
                await page.goto(url, timeout=60000)
                
                # Wait for key elements to load. 
                # LinkedIn public job pages usually have a class like 'top-card-layout__title' or 'job-details-jobs-unified-top-card__job-title'
                # We'll try a generic wait or check for title
                await page.wait_for_selector("h1", timeout=10000)
                
                content = await page.content()
                soup = BeautifulSoup(content, "html.parser")
                
                # Extract details (Selectors need to be robust or updated frequently)
                # Strategy: Try multiple common selectors
                
                title = self._extract_title(soup)
                company = self._extract_company(soup)
                description = self._extract_description(soup)
                
                return Job(
                    title=title or "Unknown Title",
                    company=company or "Unknown Company",
                    description=description or "No description found",
                    url=url,
                    source="linkedin",
                    created_at=datetime.now()
                )
                
            except Exception as e:
                logger.error(f"Error scraping LinkedIn: {e}")
                raise e
            finally:
                await browser.close()

    def _extract_title(self, soup: BeautifulSoup) -> str:
        # Try common LinkedIn title classes
        title_tag = soup.find("h1", class_="top-card-layout__title")
        if not title_tag:
            title_tag = soup.find("h1", class_="job-details-jobs-unified-top-card__job-title")
        if not title_tag:
             title_tag = soup.find("h1") # Fallback
        return title_tag.get_text(strip=True) if title_tag else None

    def _extract_company(self, soup: BeautifulSoup) -> str:
        # Try common company classes
        company_tag = soup.find("a", class_="topcard__org-name-link")
        if not company_tag:
             company_tag = soup.find("div", class_="top-card-layout__card") # Sometimes in a div
        return company_tag.get_text(strip=True) if company_tag else None

    def _extract_description(self, soup: BeautifulSoup) -> str:
        # Try common description classes
        desc_tag = soup.find("div", class_="show-more-less-html__markup")
        if not desc_tag:
            desc_tag = soup.find("div", class_="description__text")
        return desc_tag.get_text(strip=True) if desc_tag else None
