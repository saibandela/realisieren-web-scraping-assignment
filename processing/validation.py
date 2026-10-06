from urllib.parse import urlparse


VALID_SOURCES = {
    "Books to Scrape",
    "Quotes to Scrape",
}


def validate_source(source: str | None) -> bool:
    """Check whether the source is one of the supported sources."""
    return source in VALID_SOURCES


def validate_name(name_or_title: str | None) -> bool:
    """Check that the record has a non-empty name or title."""
    return bool(name_or_title and name_or_title.strip())


def validate_url(url: str | None) -> bool:
    """Check that a URL is absolute and uses HTTP or HTTPS."""
    if not url:
        return False

    try:
        parsed = urlparse(url)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except ValueError:
        return False


def validate_price(price: float | int | None) -> bool:
    """Check that price is missing or a non-negative number."""
    if price is None:
        return True

    return isinstance(price, (int, float)) and price >= 0


def validate_rating(rating: int | None) -> bool:
    """Check that rating is missing or an integer from 1 to 5."""
    if rating is None:
        return True

    return isinstance(rating, int) and 1 <= rating <= 5


def validate_record(record: dict) -> tuple[bool, str | None]:
    """
    Validate a cleaned record.

    Returns:
        (True, None) when valid.
        (False, rejection_reason) when invalid.
    """
    if not validate_source(record.get("source")):
        return False, "invalid_source"

    if not validate_name(record.get("name_or_title")):
        return False, "missing_name_or_title"

    if not validate_url(record.get("source_url")):
        return False, "invalid_url"

    if not validate_price(record.get("price")):
        return False, "invalid_price"

    if not validate_rating(record.get("rating")):
        return False, "invalid_rating"

    return True, None