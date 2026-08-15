from src.llm.tool_definitions import TOOLS

def test_tools_exist():

    assert "get_latest_summary" in TOOLS
    assert "get_revenue_growth" in TOOLS
    assert "get_revenue_cagr" in TOOLS
    assert "get_profit_margin" in TOOLS
    assert "get_net_income_cagr" in TOOLS
    assert "get_operating_cash_flow_margin" in TOOLS
    assert "get_asset_growth" in TOOLS
    assert "get_liability_to_asset_ratio" in TOOLS
    assert "get_revenue_vs_income_growth" in TOOLS
    assert "get_trend_summary" in TOOLS


def test_revenue_growth_definition():

    tool = TOOLS["get_revenue_growth"]

    assert "description" in tool
    assert "input" in tool
    assert "output" in tool

    assert tool["input"]["company"] == "string"

    assert (
        "revenue_growth_pct"
        in tool["output"]
    )