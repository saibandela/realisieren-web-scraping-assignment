import hashlib
import re
import string


def normalize_for_matching(value: str | None) -> str:
    """Normalize text for duplicate comparison."""
    if not value:
        return ""

    value = value.lower()
    value = value.translate(str.maketrans("", "", string.punctuation))
    value = re.sub(r"\s+", " ", value).strip()

    return value


def create_fingerprint(record: dict) -> str:
    """
    Create a deterministic fingerprint based on the source-specific
    duplicate rules from the assignment.
    """
    source = record.get("source", "")

    if source == "Books to Scrape":
        key = normalize_for_matching(
            record.get("name_or_title")
        )

    elif source == "Quotes to Scrape":
        quote = normalize_for_matching(
            record.get("name_or_title")
        )
        author = normalize_for_matching(
            record.get("author")
        )

        key = f"{author}|{quote[:50]}"

    else:
        key = normalize_for_matching(
            record.get("name_or_title")
        )

    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def deduplicate_records(
    records: list[dict],
) -> tuple[list[dict], int]:
    """
    Remove duplicate records while preserving original order.

    Returns:
        (unique_records, duplicate_count)
    """
    unique_records = []
    seen = set()
    duplicate_count = 0

    for record in records:
        fingerprint = create_fingerprint(record)

        if fingerprint in seen:
            duplicate_count += 1
            continue

        seen.add(fingerprint)
        unique_records.append(record)

    return unique_records, duplicate_count