from processing.cleaning import (
    clean_text,
    strip_quotes,
    clean_price,
    clean_rating,
    clean_tags,
    normalize_url,
)


def test_clean_text():
    assert clean_text("  Hello   World  ") == "Hello World"
    assert clean_text(None) is None
    assert clean_text("   ") is None


def test_strip_quotes():
    assert strip_quotes('“Hello World”') == "Hello World"
    assert strip_quotes('"Hello World"') == "Hello World"
    assert strip_quotes(None) is None


def test_clean_price():
    assert clean_price("£51.77") == 51.77
    assert clean_price("£0.00") == 0.0
    assert clean_price(None) is None


def test_clean_rating():
    assert clean_rating("star-rating Three") == 3
    assert clean_rating("star-rating Five") == 5
    assert clean_rating(None) is None


def test_clean_tags():
    assert clean_tags([" books ", "mind", ""]) == ["books", "mind"]
    assert clean_tags(None) is None


def test_normalize_url():
    assert (
        normalize_url(
            "../page.html",
            "https://example.com/catalogue/",
        )
        == "https://example.com/page.html"
    )

    assert (
        normalize_url("https://example.com/page#section")
        == "https://example.com/page"
    )