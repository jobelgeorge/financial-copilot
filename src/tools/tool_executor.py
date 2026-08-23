from src.analysis.financial_analysis import FinancialAnalyzer


class ToolExecutor:
    """
    Executes financial analysis tools using
    a company's financial data.
    """

    def __init__(self, financials):
        self.analyzer = FinancialAnalyzer(financials)

    def execute(self, tool_name):
        """
        Execute the requested financial tool.
        """

        if tool_name == "get_revenue_growth":
            return self.analyzer.revenue_growth()

        elif tool_name == "get_profit_margin":
            return self.analyzer.net_profit_margin()

        elif tool_name == "get_operating_cash_flow_margin":
            return self.analyzer.operating_cash_flow_margin()

        elif tool_name == "get_asset_growth":
            return self.analyzer.asset_growth()

        elif tool_name == "get_revenue_cagr":
            return self.analyzer.revenue_cagr()

        elif tool_name == "get_net_income_cagr":
            return self.analyzer.net_income_cagr()

        elif tool_name == "get_liability_to_asset_ratio":
            return self.analyzer.liability_to_asset_ratio()

        elif tool_name == "get_revenue_vs_income_growth":
            return self.analyzer.revenue_vs_income_growth()

        elif tool_name == "get_latest_summary":
            return self.analyzer.latest_year_summary()

        elif tool_name == "get_trend_summary":
            return self.analyzer.trend_summary()

        else:
            raise ValueError(
                f"Unknown financial tool: {tool_name}"
            )