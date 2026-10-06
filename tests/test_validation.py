from processing.validation import (
    validate_source,
    validate_name,
    validate_url,
    validate_price,
    validate_rating,
    validate_record,
)


def test_validate_source():
    assert validate_source("Books to Scrape")
    assert validate_source("Quotes to Scrape")
    assert not validate_source("Unknown Source")


def test_validate_name():
    assert validate_name("A Light in the Attic")
    assert not validate_name("")
    assert not validate_name(None)


def test_validate_url():
    assert validate_url("https://books.toscrape.com/")
    assert validate_url("http://example.com/")
    assert not validate_url("not-a-url")
    assert not validate_url(None)


def test_validate_price():
    assert validate_price(None)
    assert validate_price(51.77)
    assert validate_price(0)
    assert not validate_price(-1)


def test_validate_rating():
    assert validate_rating(None)
    assert validate_rating(1)
    assert validate_rating(5)
    assert not validate_rating(0)
    assert not validate_rating(6)


def test_validate_record():
    valid_record = {
        "source": "Books to Scrape",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "A Light in the Attic",
        "price": 51.77,
        "rating": 3,
    }

    assert validate_record(valid_record) == (True, None)


def test_invalid_record():
    invalid_record = {
        "source": "Unknown Source",
        "source_url": "https://example.com/",
        "name_or_title": "Test",
        "price": 10,
        "rating": 3,
    }

    assert validate_record(invalid_record) == (
        False,
        "invalid_source",
    )