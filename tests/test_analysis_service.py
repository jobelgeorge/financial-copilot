import pandas as pd
from src.analysis.analysis_service import FinancialAnalysisService

def create_test_data():

    return pd.DataFrame(
        {
            "fiscal_year": [2022, 2023, 2024],
            "revenue": [100.0, 120.0, 150.0],
            "net_income": [10.0, 15.0, 21.0],
            "assets": [200.0, 220.0, 250.0],
            "liabilities": [100.0, 110.0, 125.0],
            "cash": [20.0, 25.0, 30.0],
            "operating_cash_flow": [15.0, 20.0, 25.0],
        }
    )


def test_latest_summary():

    data = create_test_data()

    service = FinancialAnalysisService(data)

    result = service.get_latest_summary()

    assert result["fiscal_year"] == 2024
    assert result["revenue_billions"] == 150.0
    assert result["net_income_billions"] == 21.0


def test_revenue_cagr():

    data = create_test_data()

    service = FinancialAnalysisService(data)

    result = service.get_revenue_cagr()

    expected = (
        (150 / 100) ** (1 / 2) - 1
    ) * 100

    assert round(result, 2) == round(expected, 2)