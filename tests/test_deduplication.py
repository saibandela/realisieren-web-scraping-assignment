from processing.deduplication import (
    create_fingerprint,
    deduplicate_records,
)


def test_books_with_same_title_are_duplicates():
    first = {
        "source": "Books to Scrape",
        "name_or_title": "A Light in the Attic",
    }

    second = {
        "source": "Books to Scrape",
        "name_or_title": "a light in the attic",
    }

    assert create_fingerprint(first) == create_fingerprint(second)


def test_quotes_use_author_and_quote():
    first = {
        "source": "Quotes to Scrape",
        "author": "Albert Einstein",
        "name_or_title": "The world as we have created it",
    }

    second = {
        "source": "Quotes to Scrape",
        "author": "Albert Einstein",
        "name_or_title": "The world as we have created it",
    }

    assert create_fingerprint(first) == create_fingerprint(second)


def test_deduplicate_records():
    records = [
        {
            "source": "Books to Scrape",
            "name_or_title": "A Light in the Attic",
        },
        {
            "source": "Books to Scrape",
            "name_or_title": "a light in the attic",
        },
        {
            "source": "Books to Scrape",
            "name_or_title": "Tipping the Velvet",
        },
    ]

    unique_records, duplicate_count = deduplicate_records(records)

    assert len(unique_records) == 2
    assert duplicate_count == 1
