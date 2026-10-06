# AI Usage Disclosure

## Overview

AI assistance was used during the development of this web scraping assignment as a coding and review aid.

The final implementation was executed, tested, and reviewed locally in the project environment.

---

## Areas Where AI Assistance Was Used

AI assistance was used for:

- Planning the project structure.
- Breaking the assignment into scraping, cleaning, validation, and deduplication components.
- Drafting initial Python implementations.
- Suggesting reusable HTTP and retry handling.
- Suggesting HTML parsing approaches using Requests and BeautifulSoup.
- Developing cleaning and validation functions.
- Developing the duplicate detection logic.
- Creating unit tests.
- Reviewing the pipeline design and output reconciliation.
- Improving documentation and README structure.
- Reviewing the implementation against the assignment evaluation criteria.

---

## Human Verification

AI-generated suggestions were not treated as automatically correct.

The implementation was manually executed and verified in the local Python virtual environment.

The following checks were performed:

### Books Scraper

The scraper successfully collected:

```text
1000 books
```

Pagination was verified by following the website's `next` link dynamically.

### Quotes Scraper

The scraper successfully collected:

```text
100 quotes
```

Pagination was also verified using the website's `next` link.

### Full Pipeline

The complete pipeline produced:

```text
Raw records:        1100
Valid records:      1100
Rejected records:   0
Duplicates removed: 1
Final records:      1099
```

The reconciliation was verified:

```text
1100 - 0 - 1 = 1099
```

### Automated Tests

The project tests were executed using:

```bash
python -m pytest
```

Result:

```text
13 passed
```

---

## AI-Generated Code Review

Generated code was reviewed and adjusted before being used.

Particular attention was given to:

- Correct pagination behavior.
- URL normalization.
- Missing HTML elements.
- Request failures and retries.
- Validation rules.
- Duplicate detection rules.
- CSV schema.
- Summary report calculations.
- Logging behavior.
- Test coverage.

The generated implementation was tested against the actual practice websites rather than being accepted based only on static inspection.

---

## AI Limitations and Corrections

AI suggestions were treated as starting points rather than final answers.

During development, some implementation details required verification and correction, particularly around:

- Test execution using the correct virtual-environment Python interpreter.
- Summary-report metric calculations.
- Per-source reconciliation.
- Ensuring duplicate counts were calculated before deduplication removed the records.
- Keeping the implementation aligned with the actual assignment requirements.

These issues were identified through local execution and testing.

---

## Final Responsibility

The final code and documentation were reviewed and executed by the candidate.

AI assistance was used to accelerate development and review, but the candidate is responsible for understanding the implementation and being able to explain:

- Why Requests and BeautifulSoup were selected.
- How pagination works.
- How cleaning and validation are separated.
- How duplicate fingerprints are generated.
- How retries and failures are handled.
- Why missing fields are preserved.
- How the final record count is reconciled.
- How the tests verify the processing logic.