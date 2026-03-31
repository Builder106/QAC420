from datetime import datetime
from typing import Any

import pandas as pd

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

from ..config import MIN_YEAR, MAX_YEAR

HOUSE_BASE = "https://disclosures-clerk.house.gov"
HOUSE_SEARCH_URL = "https://disclosures-clerk.house.gov/FinancialDisclosure#Search"


def _parse_date(s: str) -> int | None:
    if not s or not isinstance(s, str):
        return None
    try:
        return int(s.strip())
    except ValueError:
        pass
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s.strip(), fmt).year
        except ValueError:
            continue
    return None


def _normalize_house_disclosure_row(
    name: str,
    office: str,
    year: str,
    filing_type: str,
    pdf_url: str,
) -> dict:
    return {
        "chamber": "House",
        "legislator_name": name,
        "disclosure_date": "",
        "transaction_date": "",
        "ticker": None,
        "asset_description": None,
        "asset_type": None,
        "transaction_type": None,
        "amount_range": None,
        "owner": None,
        "ptr_link": pdf_url,
        "comment": f"Disclosure listing; parse PDF for trades. Type: {filing_type}",
        "transaction_year": _parse_date(year),
        "disclosure_year": _parse_date(year),
        "filing_type": filing_type,
        "office": office,
    }


class HouseOfficialScraper:
    def __init__(self, headless: bool = True):
        if not HAS_PLAYWRIGHT:
            raise RuntimeError("Playwright is required. Install with: pip install playwright && playwright install")
        self._headless = headless
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None

    def __enter__(self):
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self._headless, args=["--disable-dev-shm-usage"])
        self._context = self._browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
        )
        self._page = self._context.new_page()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._page:
            self._page.close()
        if self._context:
            self._context.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

    def _ensure_search_page(self) -> None:
        self._page.goto(HOUSE_SEARCH_URL)
        self._page.wait_for_load_state("networkidle")
        search_tab = self._page.query_selector('a[href="#Search"]')
        if search_tab and not search_tab.is_visible():
            search_tab.click()
        self._page.wait_for_selector(".search-filter, #searchForm, #LastName", state="visible", timeout=15000)

    def _search_year(self, year: str, last_name: str = "") -> list[dict]:
        self._page.select_option("#FilingYear", year)
        self._page.fill("#LastName", last_name)
        submit = self._page.query_selector("button[type='submit']")
        if submit:
            submit.click()
        self._page.wait_for_selector("#search-result h2, table.library-table.dataTable, td.dataTables_empty", state="visible", timeout=20000)
        empty = self._page.query_selector("td.dataTables_empty")
        if empty and "No activities found" in (empty.inner_text() or ""):
            return []
        table = self._page.query_selector("table.library-table.dataTable")
        if not table:
            return []
        rows = table.query_selector_all("tbody tr")
        results = []
        for row in rows:
            name_cell = row.query_selector('td[data-label="Name"]')
            office_cell = row.query_selector('td[data-label="Office"]')
            year_cell = row.query_selector('td[data-label="Filing Year"]')
            filing_cell = row.query_selector('td[data-label="Filing"]')
            if not name_cell:
                continue
            link = name_cell.query_selector("a")
            if not link:
                continue
            href = link.get_attribute("href")
            if not href:
                continue
            if href.startswith("/"):
                pdf_url = f"{HOUSE_BASE}{href}"
            else:
                pdf_url = f"{HOUSE_BASE}/{href}"
            name = name_cell.inner_text().strip()
            office = office_cell.inner_text().strip() if office_cell else ""
            yr = year_cell.inner_text().strip() if year_cell else year
            filing_type = filing_cell.inner_text().strip().lower() if filing_cell else ""
            if "ptr" in filing_type or "transaction" in filing_type or "periodic" in filing_type:
                results.append(_normalize_house_disclosure_row(name, office, yr, filing_type, pdf_url))
        return results

    def scrape(
        self,
        start_year: int | None = None,
        end_year: int | None = None,
        last_name: str = "",
    ) -> pd.DataFrame:
        start_year = start_year or MIN_YEAR
        end_year = end_year or MAX_YEAR
        self._ensure_search_page()
        all_rows = []
        for year in range(start_year, end_year + 1):
            try:
                rows = self._search_year(str(year), last_name)
                all_rows.extend(rows)
            except Exception:
                continue
        if not all_rows:
            return pd.DataFrame()
        df = pd.DataFrame(all_rows)
        for c in ("transaction_year", "disclosure_year"):
            if c not in df.columns:
                df[c] = None
        return df
