import re
from urllib.parse import urljoin


def clean_text(value: str | None) -> str | None:
    """Normalize whitespace and return None for missing values."""
    if value is None:
        return None

    cleaned = re.sub(r"\s+", " ", value).strip()
    return cleaned or None


def strip_quotes(value: str | None) -> str | None:
    """Remove surrounding quote characters from text."""
    if value is None:
        return None

    cleaned = value.strip()

    quote_chars = "\"'“”‘’«»"
    cleaned = cleaned.strip(quote_chars).strip()

    return cleaned or None


def clean_price(value: str | None) -> float | None:
    """Convert a price string such as '£51.77' to a float."""
    if value is None:
        return None

    cleaned = clean_text(value)

    if cleaned is None:
        return None

    match = re.search(r"\d+(?:\.\d+)?", cleaned)

    if not match:
        return None

    return float(match.group())


def clean_rating(value: str | None) -> int | None:
    """Convert a rating class such as 'star-rating Three' to 1-5."""
    if value is None:
        return None

    rating_map = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
    }

    cleaned = clean_text(value)

    if cleaned is None:
        return None

    words = cleaned.lower().split()

    for word in words:
        if word in rating_map:
            return rating_map[word]

    return None


def clean_tags(value: list[str] | str | None) -> list[str] | None:
    """Clean tags and remove empty values."""
    if value is None:
        return None

    if isinstance(value, str):
        values = [value]
    else:
        values = value

    cleaned_tags = []

    for tag in values:
        cleaned = clean_text(tag)

        if cleaned:
            cleaned_tags.append(cleaned)

    return cleaned_tags or None


def normalize_url(url: str | None, base_url: str | None = None) -> str | None:
    """Convert relative URLs to absolute URLs and remove fragments."""
    if url is None:
        return None

    cleaned = clean_text(url)

    if cleaned is None:
        return None

    if base_url:
        cleaned = urljoin(base_url, cleaned)

    return cleaned.split("#", 1)[0]