import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper


logger = logging.getLogger(__name__)


class BooksScraper(BaseScraper):
    """Scraper for Books to Scrape."""

    START_URL = "https://books.toscrape.com/"

    def scrape(self) -> list[dict]:
        """Scrape all book pages using dynamic pagination."""

        records = []
        url = self.START_URL
        page_number = 1

        while url:
            logger.info("Books page %d: %s", page_number, url)

            response = self.fetch(url)

            if response is None:
                logger.error(
                    "Stopping Books scraper after page %d failed.",
                    page_number,
                )
                break

            soup = BeautifulSoup(response.text, "lxml")

            page_records = self._parse_page(soup, url)

            records.extend(page_records)

            logger.info(
                "Books page %d: collected %d records.",
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
            "Books scraping completed. Total records: %d",
            len(records),
        )

        return records

    def _parse_page(
        self,
        soup: BeautifulSoup,
        page_url: str,
    ) -> list[dict]:
        """Extract raw book records from one page."""

        records = []

        for article in soup.select("article.product_pod"):
            try:
                record = self._parse_book(article, page_url)
                records.append(record)

            except Exception as exc:
                logger.warning(
                    "Failed to parse a book on %s: %s",
                    page_url,
                    exc,
                )

        return records

    @staticmethod
    def _parse_book(
        article,
        page_url: str,
    ) -> dict:
        """Extract one raw book record."""

        link = article.select_one("h3 > a")
        price = article.select_one("p.price_color")
        rating = article.select_one("p.star-rating")

        if link is None:
            raise ValueError("Book title/link element is missing")

        title = link.get("title")
        href = link.get("href")

        if not title:
            raise ValueError("Book title is missing")

        if not href:
            raise ValueError("Book URL is missing")

        return {
            "source": "Books to Scrape",
            "source_url": urljoin(page_url, href),
            "name_or_title": title,
            "category": None,
            "price": price.get_text(strip=True) if price else None,
            "rating": (
                " ".join(rating.get("class", []))
                if rating
                else None
            ),
            "author": None,
            "tags": None,
            "description": None,
        }