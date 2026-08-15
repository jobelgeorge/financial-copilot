import pandas as pd

from src.analysis.financial_analysis import FinancialAnalyzer


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
    
def test_revenue_growth():
    data = create_test_data()

    analyzer = FinancialAnalyzer(data)

    result = analyzer.revenue_growth()

    assert pd.isna(
        result.loc[0, "revenue_growth_pct"]
    )

    assert round(result.loc[1, "revenue_growth_pct"], 2) == 20.00

    assert round(
        result.loc[2, "revenue_growth_pct"], 2
    ) == 25.00
    
def test_net_profit_margin():
    data = create_test_data()

    analyzer = FinancialAnalyzer(data)

    result = analyzer.net_profit_margin()

    assert round(
        result.loc[0, "net_profit_margin_pct"], 2
    ) == 10.00

    assert round(
        result.loc[1, "net_profit_margin_pct"], 2
    ) == 12.50

    assert round(
        result.loc[2, "net_profit_margin_pct"], 2
    ) == 14.00
    
def test_operating_cash_flow_margin():
    data = create_test_data()

    analyzer = FinancialAnalyzer(data)

    result = analyzer.operating_cash_flow_margin()

    assert round(
        result.loc[0, "operating_cash_flow_margin_pct"], 2
    ) == 15.00

    assert round(
        result.loc[1, "operating_cash_flow_margin_pct"], 2
    ) == 16.67

    assert round(
        result.loc[2, "operating_cash_flow_margin_pct"], 2
    ) == 16.67
    
def test_asset_growth():
    data = create_test_data()

    analyzer = FinancialAnalyzer(data)

    result = analyzer.asset_growth()

    assert pd.isna(
        result.loc[0, "asset_growth_pct"]
    )

    assert round(
        result.loc[1, "asset_growth_pct"], 2
    ) == 10.00

    assert round(
        result.loc[2, "asset_growth_pct"], 2
    ) == 13.64
    
def test_revenue_cagr():
    data = create_test_data()

    analyzer = FinancialAnalyzer(data)

    result = analyzer.revenue_cagr()

    expected = (
        (150 / 100) ** (1 / 2) - 1
    ) * 100

    assert round(result, 2) == round(expected, 2)
    
def test_liability_to_asset_ratio():
    data = create_test_data()

    analyzer = FinancialAnalyzer(data)

    result = analyzer.liability_to_asset_ratio()

    assert round(
        result.loc[0, "liability_to_asset_pct"], 2
    ) == 50.00

    assert round(
        result.loc[1, "liability_to_asset_pct"], 2
    ) == 50.00

    assert round(
        result.loc[2, "liability_to_asset_pct"], 2
    ) == 50.00
    
def test_revenue_vs_income_growth():
    data = create_test_data()

    analyzer = FinancialAnalyzer(data)

    result = analyzer.revenue_vs_income_growth()

    assert pd.isna(
        result.loc[0, "revenue_growth_pct"]
    )

    assert pd.isna(
        result.loc[0, "net_income_growth_pct"]
    )

    assert round(
        result.loc[1, "revenue_growth_pct"], 2
    ) == 20.00

    assert round(
        result.loc[1, "net_income_growth_pct"], 2
    ) == 50.00

    assert round(
        result.loc[1, "growth_difference_pct"], 2
    ) == 30.00
    
def test_latest_year_summary():
    data = create_test_data()

    analyzer = FinancialAnalyzer(data)

    result = analyzer.latest_year_summary()

    assert result["fiscal_year"] == 2024

    assert result["revenue_billions"] == 150.0

    assert result["net_income_billions"] == 21.0

    assert round(
        result["net_profit_margin_pct"], 2
    ) == 14.00
    
def test_trend_summary():
    data = create_test_data()

    analyzer = FinancialAnalyzer(data)

    result = analyzer.trend_summary()

    assert "revenue_cagr_pct" in result
    assert "net_income_cagr_pct" in result
    assert "average_revenue_growth_pct" in result
    assert "average_net_income_growth_pct" in result
    assert "starting_profit_margin_pct" in result
    assert "latest_profit_margin_pct" in result