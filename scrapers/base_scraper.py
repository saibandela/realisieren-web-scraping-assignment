import logging
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


logger = logging.getLogger(__name__)


class BaseScraper:
    """Shared HTTP functionality for all source scrapers."""

    def __init__(self, delay: float = 0.5, timeout: int = 10):
        self.delay = delay
        self.timeout = timeout
        self.session = self._create_session()

    @staticmethod
    def _create_session() -> requests.Session:
        session = requests.Session()

        session.headers.update({
            "User-Agent": "ScrapingAssignment/1.0 (learning project)"
        })

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def fetch(self, url: str) -> requests.Response | None:
        """Fetch a URL with retries, timeout, logging, and rate limiting."""

        logger.info("Fetching page: %s", url)

        try:
            response = self.session.get(
                url,
                timeout=self.timeout
            )

            response.raise_for_status()
            response.encoding = "utf-8"

            logger.info(
                "Successfully fetched %s (status=%s)",
                url,
                response.status_code,
            )

            time.sleep(self.delay)

            return response

        except requests.RequestException as exc:
            logger.error(
                "Failed to fetch %s: %s",
                url,
                exc,
            )

            return None