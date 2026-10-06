import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class QuotesScraper(BaseScraper):
    """Scraper for Quotes to Scrape."""

    START_URL = "https://quotes.toscrape.com/"

    def scrape(self) -> list[dict]:
        """Scrape all quote pages using dynamic pagination."""
        records = []
        url = self.START_URL
        page_number = 1

        while url:
            logger.info("Quotes page %d: %s", page_number, url)

            response = self.fetch(url)

            if response is None:
                logger.error(
                    "Stopping Quotes scraper after page %d failed.",
                    page_number,
                )
                break

            soup = BeautifulSoup(response.text, "lxml")

            page_records = self._parse_page(soup, url)
            records.extend(page_records)

            logger.info(
                "Quotes page %d: collected %d records.",
                page_number,
                len(page_records),
            )

            next_link = soup.select_one("li.next > a")

            if next_link and next_link.get("href"):
                url = urljoin(url, next_link["href"])
                page_number += 1
            else:
                url = None

        logger.info(
            "Quotes scraping completed. Total records: %d",
            len(records),
        )

        return records

    def _parse_page(
        self,
        soup: BeautifulSoup,
        page_url: str,
    ) -> list[dict]:
        """Extract raw quote records from one page."""
        records = []

        for quote in soup.select("div.quote"):
            try:
                record = self._parse_quote(quote, page_url)
                records.append(record)
            except Exception as exc:
                logger.warning(
                    "Failed to parse a quote on %s: %s",
                    page_url,
                    exc,
                )

        return records

    @staticmethod
    def _parse_quote(quote, page_url: str) -> dict:
        """Extract one raw quote record."""
        text = quote.select_one("span.text")
        author = quote.select_one("small.author")
        tags = quote.select("a.tag")
        author_link = quote.select_one('a[href^="/author/"]')

        if text is None:
            raise ValueError("Quote text is missing")

        if author is None:
            raise ValueError("Quote author is missing")

        author_url = (
            urljoin(page_url, author_link["href"])
            if author_link and author_link.get("href")
            else None
        )

        return {
            "source": "Quotes to Scrape",
            "source_url": author_url or page_url,
            "name_or_title": text.get_text(strip=True),
            "category": None,
            "price": None,
            "rating": None,
            "author": author.get_text(strip=True),
            "tags": [
                tag.get_text(strip=True)
                for tag in tags
            ] or None,
            "description": None,
        }