import pandas as pd
import numpy as np

class FinancialAnalyzer:
    #Perform financial analysis on company financial data

    def __init__(self, financials: pd.DataFrame):
        self.financials = financials.copy()

        self.financials = self.financials.sort_values(
            "fiscal_year"
        ).reset_index(drop=True)

    def revenue_growth(self) -> pd.DataFrame:
        #Calculate year-over-year revenue growth

        df = self.financials[
            ["fiscal_year", "revenue"]
        ].copy()

        df["revenue_growth_pct"] = (
            df["revenue"]
            .pct_change()
            * 100
        )

        return df

    def net_profit_margin(self) -> pd.DataFrame:
        #Calculate net profit margin.

        df = self.financials[
            ["fiscal_year", "revenue", "net_income"]
        ].copy()

        df["net_profit_margin_pct"] = (
            df["net_income"]
            / df["revenue"]
            * 100
        )

        return df
    
    def operating_cash_flow_margin(self) -> pd.DataFrame:
        #Calculate operating cash flow margin

        df = self.financials[
            [
                "fiscal_year",
                "revenue",
                "operating_cash_flow",
            ]
        ].copy()

        df["operating_cash_flow_margin_pct"] = (
            df["operating_cash_flow"]
            / df["revenue"]
            * 100
        )

        return df
    
    def asset_growth(self) -> pd.DataFrame:
        #Calculate year-over-year asset growth

        df = self.financials[
            ["fiscal_year", "assets"]
        ].copy()

        df["asset_growth_pct"] = (
            df["assets"]
            .pct_change()
            * 100
        )

        return df
    
    def revenue_cagr(self) -> float:
        #Calculate average annual compounded growth rate (CAGR) of revenue over the available period.
        #How quickly did revenue grow on average over a period?
        df = self.financials[
            ["fiscal_year", "revenue"]
        ].dropna(subset=["revenue"]).copy()

        if len(df) < 2:
            return np.nan

        start_value = df.iloc[0]["revenue"]
        end_value = df.iloc[-1]["revenue"]

        start_year = df.iloc[0]["fiscal_year"]
        end_year = df.iloc[-1]["fiscal_year"]

        years = end_year - start_year

        if years <= 0 or start_value <= 0:
            return np.nan

        cagr = (
            (end_value / start_value) ** (1 / years) - 1
        ) * 100

        return cagr
    
    def net_income_cagr(self) -> float:
    # Calculate net income CAGR over the available period.

        df = self.financials[
            ["fiscal_year", "net_income"]
        ].dropna(
            subset=["net_income"]
        ).copy()

        if len(df) < 2:
            return np.nan

        first_income = df.iloc[0]["net_income"]
        last_income = df.iloc[-1]["net_income"]

        first_year = df.iloc[0]["fiscal_year"]
        last_year = df.iloc[-1]["fiscal_year"]

        years = last_year - first_year

        if years <= 0 or first_income <= 0:
            return np.nan

        cagr = (
            (last_income / first_income) ** (1 / years)
            - 1
        ) * 100

        return cagr
    
    def liability_to_asset_ratio(self) -> pd.DataFrame:
        #Calculate liabilities as a percentage of assets.

        df = self.financials[
            [
                "fiscal_year",
                "assets",
                "liabilities",
            ]
        ].copy()

        df["liability_to_asset_pct"] = (
            df["liabilities"]
            / df["assets"]
            * 100
        )

        return df
    
    def revenue_vs_income_growth(self) -> pd.DataFrame:
        #Compare revenue growth with net income growth.

        df = self.financials[
            [
                "fiscal_year",
                "revenue",
                "net_income",
            ]
        ].copy()

        df["revenue_growth_pct"] = (
            df["revenue"]
            .pct_change()
            * 100
        )

        df["net_income_growth_pct"] = (
            df["net_income"]
            .pct_change()
            * 100
        )

        df["growth_difference_pct"] = (
            df["net_income_growth_pct"]
            - df["revenue_growth_pct"]
        )

        return df
    
    def latest_year_summary(self) -> dict:
        #Return key financial metrics for the latest fiscal year.

        latest = self.financials.iloc[-1]

        revenue_growth = (
            self.financials["revenue"]
            .pct_change()
            .iloc[-1]
            * 100
        )

        profit_margin = (
            latest["net_income"]
            / latest["revenue"]
            * 100
        )

        cash_flow_margin = (
            latest["operating_cash_flow"]
            / latest["revenue"]
            * 100
        )

        liability_to_asset = (
            latest["liabilities"]
            / latest["assets"]
            * 100
        )

        return {
            "fiscal_year": int(latest["fiscal_year"]),
            "revenue_billions": float(latest["revenue"]),
            "net_income_billions": float(latest["net_income"]),
            "assets_billions": float(latest["assets"]),
            "liabilities_billions": float(latest["liabilities"]),
            "cash_billions": float(latest["cash"]),
            "operating_cash_flow_billions": float(
                latest["operating_cash_flow"]
            ),
            "revenue_growth_pct": float(revenue_growth),
            "net_profit_margin_pct": float(profit_margin),
            "operating_cash_flow_margin_pct": float(
                cash_flow_margin
            ),
            "liability_to_asset_pct": float(
                liability_to_asset
            ),
        }
        
    def trend_summary(self) -> dict:
        #Generate high-level financial trends.

        revenue_growth = self.financials["revenue"].pct_change() * 100

        net_income_growth = (
            self.financials["net_income"].pct_change() * 100
        )

        profit_margin = (
            self.financials["net_income"]
            / self.financials["revenue"]
            * 100
        )

        return {
            "revenue_cagr_pct": float(self.revenue_cagr()),
            "net_income_cagr_pct": float(
                self.net_income_cagr()
            ),
            "average_revenue_growth_pct": float(
                revenue_growth.dropna().mean()
            ),
            "average_net_income_growth_pct": float(
                net_income_growth.dropna().mean()
            ),
            "starting_profit_margin_pct": float(
                profit_margin.iloc[0]
            ),
            "latest_profit_margin_pct": float(
                profit_margin.iloc[-1]
            ),
            "profit_margin_change_pct": float(
                profit_margin.iloc[-1]
                - profit_margin.iloc[0]
            ),
        }