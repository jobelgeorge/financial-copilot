# financial data extraction engine.
import pandas as pd
from src.ingestion.financial_metrics import METRIC_TAGS


class SECParser:
    #Parser for SEC company facts.

    def _find_metric_tag(
        self,
        us_gaap: dict,
        metric: str
    ) -> str:
        """Find the first available SEC tag for a metric."""

        if metric not in METRIC_TAGS:
            raise ValueError(
                f"Unknown financial metric: {metric}"
            )

        for tag in METRIC_TAGS[metric]:
            if tag in us_gaap:
                return tag

        raise ValueError(
            f"No SEC tag found for metric: {metric}"
        )

    def extract_annual_metric(
        self,
        company_facts: dict,
        metric: str
    ) -> pd.DataFrame:
        """
        Extract annual financial data for a metric.

        Parameters:
        company_facts : dict
            Raw SEC company facts JSON.

        metric : str
            Financial metric such as revenue,
            net_income, assets, etc.

        Returns:
        pd.DataFrame
            Clean financial data.
        """

        us_gaap = company_facts["facts"]["us-gaap"]

        # Find appropriate SEC tag
        tag = self._find_metric_tag(
            us_gaap,
            metric
        )
        print(f"Using SEC tag for {metric}: {tag}")

        # Get USD data
        units = us_gaap[tag]["units"]

        if "USD" not in units:
            raise ValueError(
                f"USD data not available for {metric}"
            )

        data = units["USD"]

        df = pd.DataFrame(data)

        # Only use 10-K filings
        df = df[
            df["form"] == "10-K"
        ].copy()

        # Convert dates
        if "start" in df.columns:
            df["start"] = pd.to_datetime(df["start"])

        df["end"] = pd.to_datetime(df["end"])

        df["filed"] = pd.to_datetime(df["filed"])

        # Determine whether this is a duration metric
        duration_metric = metric in [
            "revenue",
            "net_income",
            "operating_cash_flow",
        ]
        if duration_metric:

            # Calculate period duration
            df["duration_days"] = (
                df["end"] - df["start"]
            ).dt.days

            # Keep approximately annual periods
            df = df[
                df["duration_days"].between(
                    350,
                    380
                )
            ].copy()

            # Remove repeated historical periods
            df = df.sort_values("filed")

            df = df.drop_duplicates(
                subset=["start", "end"],
                keep="last"
            )

        else:

            # Point-in-time metrics
            # Assets, liabilities, cash etc don't have a start date.Keep the latest 10-K value for each reporting date.
            df = df.sort_values("filed")
            df = df.drop_duplicates(
                subset=["end"],
                keep="last"
            )
        # Fiscal year = reporting period end year
        df["fiscal_year"] = (
            df["end"].dt.year
        )

        # Convert dollars to billions
        df["value_billions"] = (
            df["val"] / 1_000_000_000
        )

        # Sort chronologically
        df = df.sort_values(
            "fiscal_year"
        )

        # Calculate growth for duration metrics
        if duration_metric:

            df["growth_pct"] = (
                df["value_billions"]
                .pct_change()
                * 100
            )

        else:

            df["growth_pct"] = (
                df["value_billions"]
                .pct_change()
                * 100
            )

        # Select final columns
        columns = [
            "fiscal_year",
            "end",
            "value_billions",
            "growth_pct",
            "filed",
        ]

        # Duration metrics also have a start date
        if duration_metric:
            columns.insert(1, "start")

        return df[
            columns
        ].reset_index(drop=True)