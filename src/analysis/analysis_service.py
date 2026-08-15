#Expose the available analysis functions
import pandas as pd
from src.analysis.financial_analysis import FinancialAnalyzer


class FinancialAnalysisService:

    def __init__(self, financials: pd.DataFrame):

        self.analyzer = FinancialAnalyzer(
            financials
        )

    def get_revenue_growth(self):
        return self.analyzer.revenue_growth()

    def get_profit_margin(self):
        return self.analyzer.net_profit_margin()

    def get_operating_cash_flow_margin(self):
        return self.analyzer.operating_cash_flow_margin()

    def get_asset_growth(self):
        return self.analyzer.asset_growth()

    def get_revenue_cagr(self):
        return self.analyzer.revenue_cagr()

    def get_net_income_cagr(self):
        return self.analyzer.net_income_cagr()

    def get_liability_to_asset_ratio(self):
        return self.analyzer.liability_to_asset_ratio()

    def get_revenue_vs_income_growth(self):
        return self.analyzer.revenue_vs_income_growth()

    def get_latest_summary(self):
        return self.analyzer.latest_year_summary()

    def get_trend_summary(self):
        return self.analyzer.trend_summary()