import csv
import json
import logging
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from processing.cleaning import (
    clean_price,
    clean_rating,
    clean_tags,
    clean_text,
    normalize_url,
    strip_quotes,
)
from processing.deduplication import deduplicate_records
from processing.validation import validate_record
from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper


BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

CSV_PATH = OUTPUT_DIR / "final_dataset.csv"
SUMMARY_PATH = OUTPUT_DIR / "summary_report.json"
LOG_PATH = LOG_DIR / "scraper.log"

CSV_FIELDS = [
    "source",
    "source_url",
    "name_or_title",
    "category",
    "price",
    "rating",
    "author",
    "tags",
    "description",
    "scraped_at",
]


def configure_logging():
    """Configure logging to both console and log file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(
                LOG_PATH,
                mode="w",
                encoding="utf-8",
            ),
            logging.StreamHandler(),
        ],
        force=True,
    )


def clean_record(record):
    """Clean and standardize one raw record."""
    return {
        "source": clean_text(record.get("source")),
        "source_url": normalize_url(record.get("source_url")),
        "name_or_title": strip_quotes(
            clean_text(record.get("name_or_title"))
        ),
        "category": clean_text(record.get("category")),
        "price": clean_price(record.get("price")),
        "rating": clean_rating(record.get("rating")),
        "author": clean_text(record.get("author")),
        "tags": clean_tags(record.get("tags")),
        "description": clean_text(record.get("description")),
        "scraped_at": datetime.now(timezone.utc).isoformat(),
    }


def process_records(raw_records):
    """
    Clean, validate, and deduplicate records.

    Returns:
        valid_records:
            Records that passed validation before deduplication.

        final_records:
            Unique validated records.

        rejected_reasons:
            Counts of validation failures.

        duplicate_count:
            Number of duplicates removed.
    """
    valid_records = []
    rejected_reasons = Counter()

    for raw_record in raw_records:
        cleaned = clean_record(raw_record)

        is_valid, reason = validate_record(cleaned)

        if not is_valid:
            rejected_reasons[reason] += 1

            logging.warning(
                "Rejected record: reason=%s, title=%s",
                reason,
                cleaned.get("name_or_title"),
            )

            continue

        valid_records.append(cleaned)

    final_records, duplicate_count = deduplicate_records(
        valid_records
    )

    return (
        valid_records,
        final_records,
        rejected_reasons,
        duplicate_count,
    )


def write_csv(records):
    """Write final records to CSV."""
    with CSV_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=CSV_FIELDS,
        )

        writer.writeheader()

        for record in records:
            row = record.copy()

            if isinstance(row["tags"], list):
                row["tags"] = ", ".join(row["tags"])

            writer.writerow(row)


def write_summary(summary):
    """Write summary metrics to JSON."""
    with SUMMARY_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            summary,
            file,
            indent=2,
        )


def get_source_stats(
    source,
    raw_records,
    valid_records,
    final_records,
):
    """Calculate reconciliation metrics for one source."""

    raw_count = sum(
        1
        for record in raw_records
        if record.get("source") == source
    )

    valid_count = sum(
        1
        for record in valid_records
        if record.get("source") == source
    )

    final_count = sum(
        1
        for record in final_records
        if record.get("source") == source
    )

    rejected_count = raw_count - valid_count
    duplicate_count = valid_count - final_count

    return {
        "raw": raw_count,
        "valid": valid_count,
        "rejected": rejected_count,
        "duplicates_removed": duplicate_count,
        "final": final_count,
    }


def main():
    """Run the complete scraping pipeline."""

    configure_logging()

    start_time = time.perf_counter()
    start_timestamp = datetime.now(timezone.utc)

    logging.info("Scraping pipeline started.")

    # ---------------------------------------------------------
    # 1. Scrape Books
    # ---------------------------------------------------------

    books_scraper = BooksScraper()
    books_records = books_scraper.scrape()

    logging.info(
        "Books scraping finished: %d records.",
        len(books_records),
    )

    # ---------------------------------------------------------
    # 2. Scrape Quotes
    # ---------------------------------------------------------

    quotes_scraper = QuotesScraper()
    quotes_records = quotes_scraper.scrape()

    logging.info(
        "Quotes scraping finished: %d records.",
        len(quotes_records),
    )

    # Combine raw records
    raw_records = books_records + quotes_records

    logging.info(
        "Total raw records: %d",
        len(raw_records),
    )

    # ---------------------------------------------------------
    # 3. Clean, validate, and deduplicate
    # ---------------------------------------------------------

    (
        valid_records,
        final_records,
        rejected_reasons,
        duplicate_count,
    ) = process_records(raw_records)

    rejected_count = sum(rejected_reasons.values())

    logging.info(
        "Valid records: %d",
        len(valid_records),
    )

    logging.info(
        "Rejected records: %d",
        rejected_count,
    )

    logging.info(
        "Duplicates removed: %d",
        duplicate_count,
    )

    logging.info(
        "Final records: %d",
        len(final_records),
    )

    # ---------------------------------------------------------
    # 4. Write final CSV
    # ---------------------------------------------------------

    write_csv(final_records)

    logging.info(
        "Final dataset written to: %s",
        CSV_PATH,
    )

    # ---------------------------------------------------------
    # 5. Calculate per-source statistics
    # ---------------------------------------------------------

    books_stats = get_source_stats(
        "Books to Scrape",
        raw_records,
        valid_records,
        final_records,
    )

    quotes_stats = get_source_stats(
        "Quotes to Scrape",
        raw_records,
        valid_records,
        final_records,
    )

    # ---------------------------------------------------------
    # 6. Build summary report
    # ---------------------------------------------------------

    end_timestamp = datetime.now(timezone.utc)

    duration = round(
        time.perf_counter() - start_time,
        2,
    )

    summary = {
        "run": {
            "started_at": start_timestamp.isoformat(),
            "completed_at": end_timestamp.isoformat(),
            "duration_seconds": duration,
        },

        "records": {
            "raw_total": len(raw_records),
            "valid_total": len(valid_records),
            "rejected_total": rejected_count,
            "duplicates_removed": duplicate_count,
            "final_total": len(final_records),
        },

        "by_source": {
            "Books to Scrape": books_stats,
            "Quotes to Scrape": quotes_stats,
        },

        "rejected_by_reason": dict(rejected_reasons),

        "reconciliation": {
            "raw_minus_rejected": (
                len(raw_records) - rejected_count
            ),
            "valid_minus_duplicates": (
                len(valid_records) - duplicate_count
            ),
            "final_total": len(final_records),
        },

        "output_files": {
            "csv": str(CSV_PATH),
            "summary": str(SUMMARY_PATH),
            "log": str(LOG_PATH),
        },
    }

    # ---------------------------------------------------------
    # 7. Write summary JSON
    # ---------------------------------------------------------

    write_summary(summary)

    logging.info(
        "Summary report written to: %s",
        SUMMARY_PATH,
    )

    logging.info("Scraping pipeline completed.")

    # ---------------------------------------------------------
    # 8. Console summary
    # ---------------------------------------------------------

    print()
    print("========================================")
    print("SCRAPING PIPELINE COMPLETED")
    print("========================================")
    print(f"Raw records:        {len(raw_records)}")
    print(f"Valid records:      {len(valid_records)}")
    print(f"Rejected records:   {rejected_count}")
    print(f"Duplicates removed: {duplicate_count}")
    print(f"Final records:      {len(final_records)}")
    print()
    print(f"CSV:     {CSV_PATH}")
    print(f"Summary: {SUMMARY_PATH}")
    print(f"Log:     {LOG_PATH}")


if __name__ == "__main__":
    main()