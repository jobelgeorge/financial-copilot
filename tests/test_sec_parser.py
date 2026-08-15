import pandas as pd

from src.ingestion.sec_parser import SECParser


def test_extract_annual_revenue():

    company_facts = {
        "facts": {
            "us-gaap": {
                "RevenueFromContractWithCustomerExcludingAssessedTax": {
                    "units": {
                        "USD": [
                            {
                                "start": "2023-10-01",
                                "end": "2024-09-28",
                                "val": 391035000000,
                                "form": "10-K",
                                "filed": "2024-11-01",
                            },
                            {
                                "start": "2024-09-29",
                                "end": "2025-09-27",
                                "val": 416161000000,
                                "form": "10-K",
                                "filed": "2025-10-31",
                            },
                        ]
                    }
                }
            }
        }
    }

    parser = SECParser()

    result = parser.extract_annual_revenue(company_facts)

    assert isinstance(result, pd.DataFrame)

    assert len(result) == 2

    assert result.iloc[0]["revenue_billions"] == 391.035
    assert result.iloc[1]["revenue_billions"] == 416.161