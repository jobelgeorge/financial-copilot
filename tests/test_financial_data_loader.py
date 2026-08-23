import pandas as pd

from src.data.financial_data_loader import (
    FinancialDataLoader
)


def test_loader_reads_processed_csv(
    tmp_path
):

    processed_dir = (
        tmp_path / "data" / "processed"
    )

    processed_dir.mkdir(
        parents=True
    )

    test_data = pd.DataFrame(
        {
            "fiscal_year": [2023, 2024],
            "revenue": [100.0, 120.0],
            "net_income": [10.0, 15.0],
            "assets": [200.0, 220.0],
            "liabilities": [100.0, 110.0],
            "cash": [20.0, 25.0],
            "operating_cash_flow": [
                15.0,
                20.0
            ],
        }
    )

    csv_path = (
        processed_dir
        / "aapl_financials.csv"
    )

    test_data.to_csv(
        csv_path,
        index=False
    )