import argparse
import os
from pathlib import Path

from src.ingestion.sec_client import SECClient
from src.ingestion.sec_parser import SECParser
from src.ingestion.company_lookup import CompanyLookup
from src.ingestion.financial_metrics import METRIC_TAGS

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def ingest_company(company_name: str, user_agent: str) -> Path:

    lookup = CompanyLookup(user_agent)
    company = lookup.find_company(company_name)

    print(f"Fetching SEC data for {company['name']} ({company['ticker']})...")

    client = SECClient()
    company_facts = client.get_company_facts(company["cik"])

    parser = SECParser()
    financial_data = {}

    for metric in METRIC_TAGS:
        try:
            result = parser.extract_annual_metric(company_facts, metric)
            financial_data[metric] = result
        except Exception as e:
            print(f"Could not extract {metric}: {e}")

    if not financial_data:
        raise ValueError(
            f"No financial data could be extracted for {company_name}."
        )

    combined = None

    for metric, df in financial_data.items():
        metric_df = df[["fiscal_year", "value_billions"]].copy()
        metric_df = metric_df.rename(columns={"value_billions": metric})
        if combined is None:
            combined = metric_df
        else:
            combined = combined.merge(metric_df, on="fiscal_year", how="outer")

    combined = combined.sort_values("fiscal_year").reset_index(drop=True)

    output_dir = PROJECT_ROOT / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{company['ticker'].lower()}_financials.csv"
    combined.to_csv(output_file, index=False)

    print(f"Data saved to: {output_file}")
    return output_file


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Financial data ingestion pipeline"
    )
    parser.add_argument("--company", required=True, help="Company name to analyze")
    return parser.parse_args()


def main():
    args = parse_arguments()
    user_agent = os.getenv("SEC_USER_AGENT")
    if not user_agent:
        raise ValueError("SEC_USER_AGENT is not configured in the environment.")
    ingest_company(args.company, user_agent)


if __name__ == "__main__":
    main()
