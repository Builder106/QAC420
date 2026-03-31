# Capitol Alpha – Data collection & pipeline

Pipeline for fetching and merging U.S. Congress (Senate and House) stock trade disclosures into a single CSV.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**For official-site scraping (recommended):** install Playwright browsers once:

```bash
playwright install chromium
```

## Run

**Option 1 – Scrape official government sites (efd.senate.gov and clerk.house.gov):**

```bash
python -m pipeline.run_pipeline --use-official
```

- **Senate:** Opens efdsearch.senate.gov, accepts the disclosure agreement, searches for PTRs by date range, visits each report URL, and parses the transaction table into rows.
- **House:** Opens disclosures-clerk.house.gov/FinancialDisclosure, searches by year, and collects PTR/transaction report PDF links. House trade-level data requires a separate PDF/OCR step; the pipeline outputs disclosure listings (name, year, pdf_url) for now.

**Option 2 – Use pre-aggregated APIs (no browser):**

```bash
python -m pipeline.run_pipeline
```

- Uses [Senate Stock Watcher data](https://github.com/timothycarambat/senate-stock-watcher-data) (GitHub/S3) for Senate. House S3 is attempted; if it fails, only Senate is written.
- First run saves raw JSON under `data/`. Later runs use cache unless `--fresh` is used.

Options:

- `--fresh` – Re-download API data (ignored when using `--use-official`).
- `--senate-only` – Only Senate (scrape or API).
- `--house-only` – Only House (scrape or API).
- `--use-official` – Scrape **efdsearch.senate.gov** and **disclosures-clerk.house.gov** (requires Playwright).

## Data sources

- **Official (--use-official):** Direct scraping of **efdsearch.senate.gov** (Senate) and **disclosures-clerk.house.gov/FinancialDisclosure** (House), as in your problem statement.
- **Fallback (default):** Pre-aggregated Senate JSON from [timothycarambat/senate-stock-watcher-data](https://github.com/timothycarambat/senate-stock-watcher-data); optional House S3 or other APIs.

## Output schema

`data/legislative_trades.csv` columns:
- chamber
- legislator_name
- transaction_date
- disclosure_date
- ticker
- asset_description
- asset_type
- transaction_type
- amount_range
- amount_min
- amount_max
- amount_avg
- owner
- ptr_link
- office
- party
- state
- transaction_year
- disclosure_year
- comment

## Tests

```bash
pip install pytest
pytest tests/ -v
```
