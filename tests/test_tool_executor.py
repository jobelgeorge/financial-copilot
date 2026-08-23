import pandas as pd

from src.tools.tool_executor import ToolExecutor


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


def test_execute_revenue_growth():

    data = create_test_data()

    executor = ToolExecutor(data)

    result = executor.execute(
        "get_revenue_growth"
    )

    assert "revenue_growth_pct" in result.columns

    assert round(
        result.loc[1, "revenue_growth_pct"], 2
    ) == 20.00


def test_execute_profit_margin():

    data = create_test_data()

    executor = ToolExecutor(data)

    result = executor.execute(
        "get_profit_margin"
    )

    assert "net_profit_margin_pct" in result.columns

    assert round(
        result.loc[0, "net_profit_margin_pct"], 2
    ) == 10.00


def test_execute_asset_growth():

    data = create_test_data()

    executor = ToolExecutor(data)

    result = executor.execute(
        "get_asset_growth"
    )

    assert "asset_growth_pct" in result.columns

    assert round(
        result.loc[1, "asset_growth_pct"], 2
    ) == 10.00


def test_execute_latest_summary():

    data = create_test_data()

    executor = ToolExecutor(data)

    result = executor.execute(
        "get_latest_summary"
    )

    assert result["fiscal_year"] == 2024

    assert result["revenue_billions"] == 150.0


def test_unknown_tool():

    data = create_test_data()

    executor = ToolExecutor(data)

    try:
        executor.execute(
            "invalid_tool"
        )

        assert False

    except ValueError:
        assert True