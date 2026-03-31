import pandas as pd

from pipeline.merge_to_csv import clean_dataframe


def test_clean_dataframe_basic():
    df = pd.DataFrame([
        {
            "chamber": "Senate",
            "legislator_name": " Ron L Wyden ",
            "transaction_date": "11/10/2020",
            "disclosure_date": "11/15/2020",
            "ticker": "aapl",
            "asset_description": "Apple Inc.",
            "asset_type": "Stock",
            "transaction_type": "Sale (Full)",
            "amount_range": "$50,001 - $100,000",
            "amount_min": "50001",
            "amount_max": "100000",
            "amount_avg": "75000.5",
            "owner": " spouse ",
            "ptr_link": "url",
            "office": "D-OR",
            "party": "D",
            "state": "OR",
            "transaction_year": 2020,
            "disclosure_year": 2020,
            "comment": "--",
        },
        {
            # duplicate row should be removed
            "chamber": "Senate",
            "legislator_name": "Ron L Wyden",
            "transaction_date": "11/10/2020",
            "disclosure_date": "11/15/2020",
            "ticker": "AAPL",
            "asset_description": "Apple Inc.",
            "asset_type": "Stock",
            "transaction_type": "Sale (Full)",
            "amount_range": "$50,001 - $100,000",
            "amount_min": "50001",
            "amount_max": "100000",
            "amount_avg": "75000.5",
            "owner": "Spouse",
            "ptr_link": "url",
            "office": "D-OR",
            "party": "D",
            "state": "OR",
            "transaction_year": 2020,
            "disclosure_year": 2020,
            "comment": "--",
        },
    ])

    cleaned = clean_dataframe(df)
    assert len(cleaned) == 1
    row = cleaned.iloc[0]
    assert row["legislator_name"] == "Ron L Wyden"
    assert row["ticker"] == "AAPL"
    assert row["transaction_type"] == "Sale"
    assert row["owner"] == "Spouse"
    assert row["amount_min"] == 50001.0
    assert row["amount_max"] == 100000.0
    assert row["amount_avg"] == 75000.5
