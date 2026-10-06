# Web Scraping & Data Consolidation Assignment

## Overview

This project is a Python-based web scraping and data consolidation pipeline that collects publicly available data from:

- Books to Scrape
- Quotes to Scrape

The pipeline scrapes all available pages using dynamic pagination, cleans and standardizes the extracted data, validates records, removes duplicates, and generates a consolidated CSV dataset, summary report, and execution log.

The complete pipeline can be executed with:

```bash
python main.py
```

---

## Project Structure

```text
scraping_assignment/
│
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
│
├── processing/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── validation.py
│   └── deduplication.py
│
├── tests/
│   ├── test_cleaning.py
│   ├── test_validation.py
│   └── test_deduplication.py
│
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
│
├── logs/
│   └── scraper.log
│
├── main.py
├── requirements.txt
├── README.md
└── AI_USAGE.md
```

---

## Requirements

- Python 3.10–3.12
- requests
- beautifulsoup4
- lxml
- pytest

---

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Scraper

Run the complete pipeline:

```bash
python main.py
```

The pipeline performs the following steps:

```text
Scrape
   ↓
Clean
   ↓
Validate
   ↓
Deduplicate
   ↓
Write CSV
   ↓
Write Summary JSON
   ↓
Write Log
```

---

## Data Sources

### Books to Scrape

URL:

```text
https://books.toscrape.com/
```

The scraper follows the `next` pagination link dynamically until there is no next page.

The implementation does not rely on hard-coded page numbers.

### Quotes to Scrape

URL:

```text
https://quotes.toscrape.com/
```

The scraper also follows the site's `next` pagination link dynamically.

---

## Scraping Approach

The project uses:

- `requests` for HTTP requests
- `BeautifulSoup` with `lxml` for HTML parsing
- A reusable `BaseScraper` for common HTTP functionality

The base scraper provides:

- HTTP sessions
- User-Agent configuration
- Request timeout
- Retry handling
- HTTP error handling
- Rate limiting between requests
- Logging

Temporary HTTP failures such as `429`, `500`, `502`, `503`, and `504` are retried.

A short delay is used between successful requests to avoid aggressive request rates.

---

## Data Schema

The final dataset contains the following common fields:

| Field | Description |
|---|---|
| `source` | Website from which the record was collected |
| `source_url` | Absolute source URL associated with the record |
| `name_or_title` | Book title or quote text |
| `category` | Category when available |
| `price` | Numeric price when available |
| `rating` | Numeric rating from 1 to 5 when available |
| `author` | Author when available |
| `tags` | Associated tags when available |
| `description` | Description when available |
| `scraped_at` | UTC timestamp when the record was processed |

Fields that are not available from the listing pages are retained as missing values rather than fabricated.

---

## Data Cleaning

Cleaning is implemented separately from scraping in `processing/cleaning.py`.

The pipeline performs:

- Whitespace normalization
- Quote removal
- Price conversion to numeric values
- Rating conversion from textual classes to integers
- Tag cleaning
- URL normalization

Examples:

```text
"  Hello    World  "
        ↓
"Hello World"
```

```text
"£51.77"
        ↓
51.77
```

```text
"star-rating Three"
        ↓
3
```

---

## Validation

Records are validated after cleaning.

The validation layer checks:

1. Source is one of the supported sources.
2. Name or title is not empty.
3. URL is a valid absolute HTTP/HTTPS URL.
4. Price is either missing or non-negative.
5. Rating is either missing or between 1 and 5.

Invalid records are rejected and the rejection reason is recorded.

---

## Duplicate Detection

Duplicate detection is implemented in `processing/deduplication.py`.

### Books

Books are matched using a normalized version of their title.

Normalization:

- Converts text to lowercase
- Removes punctuation
- Collapses whitespace

### Quotes

Quotes are matched using:

- Author
- First 50 characters of the normalized quote

A SHA-256 hash is used as the final fingerprint.

Duplicate records are removed while preserving the original record order.

---

## Error Handling and Reliability

The scraper handles:

- Request timeouts
- HTTP errors
- Temporary server failures
- Retryable HTTP status codes
- Missing HTML elements
- Invalid record data
- Individual record parsing failures

If a page request fails, the affected source is stopped safely rather than crashing the complete application.

The Books and Quotes scrapers are executed independently so that a failure in one source does not prevent the other source from running.

---

## Logging

Logs are written to:

```text
logs/scraper.log
```

The log records important events such as:

- Pipeline start and completion
- Page requests
- Successful responses
- Records collected per page
- Request failures
- Rejected records
- Output file creation

---

## Output Files

### Final Dataset

```text
output/final_dataset.csv
```

Contains the final cleaned and deduplicated records.

### Summary Report

```text
output/summary_report.json
```

Contains:

- Run timestamps
- Runtime duration
- Raw record count
- Valid record count
- Rejected record count
- Duplicate count
- Final record count
- Per-source statistics
- Rejection reasons
- Reconciliation metrics
- Output file locations

### Log

```text
logs/scraper.log
```

Contains execution logs from the scraping pipeline.

---

## Testing

Unit tests are provided for:

- Data cleaning
- Validation
- Duplicate detection

Run the tests with:

```bash
python -m pytest
```

The current implementation passes all automated tests.

---

## Current Execution Result

A successful execution produced:

```text
Raw records:        1100
Valid records:      1100
Rejected records:   0
Duplicates removed: 1
Final records:      1099
```

The reconciliation is:

```text
1100 raw
- 0 rejected
- 1 duplicate
= 1099 final
```

---

## Design Decisions and Assumptions

### Listing-page extraction

The implementation extracts the required fields directly available from the listing pages.

For fields such as book category and description that require visiting individual product detail pages, the implementation leaves the fields missing instead of generating approximately 1,000 additional requests.

This keeps the scraper efficient and avoids unnecessary traffic to the practice website.

### Source URL

For Books, `source_url` contains the individual book URL.

For Quotes, `source_url` contains the associated author URL when available.

### Missing values

Missing values are preserved as missing rather than replaced with fabricated or inferred data.

---

## Limitations

- The implementation focuses on the required practice websites.
- It does not bypass authentication, CAPTCHA, or access controls.
- Category and book description are not collected from individual detail pages.
- The pipeline is designed for the assignment rather than large-scale distributed scraping.
- No persistent database is required for this implementation.

---

## Reproducibility

To reproduce the project:

```bash
python -m venv venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

Run tests:

```bash
python -m pytest
```

No API keys, passwords, or other secrets are required.