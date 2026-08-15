from src.ingestion.company_lookup import CompanyLookup


def test_find_company():
    lookup = CompanyLookup.__new__(CompanyLookup)

    lookup.companies = {
        "0": {
            "title": "Apple Inc.",
            "ticker": "AAPL",
            "cik_str": 320193,
        }
    }

    result = lookup.find_company("Apple")

    assert result["name"] == "Apple Inc."
    assert result["ticker"] == "AAPL"
    assert result["cik"] == "0000320193"