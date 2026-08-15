import argparse
import os
from pathlib import Path

from src.ingestion.sec_client import SECClient
from src.ingestion.sec_parser import SECParser
from src.ingestion.company_lookup import CompanyLookup
from src.ingestion.financial_metrics import METRIC_TAGS

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Financial data ingestion pipeline"
    )

    parser.add_argument(
        "--company",
        required=True,
        help="Company name to analyze"
    )

    return parser.parse_args()

def main():

    args = parse_arguments()

    company_name = args.company

    print("Starting financial data pipeline")
    print(f"Company: {company_name}")

    user_agent = os.getenv("SEC_USER_AGENT")

    if not user_agent:
        raise ValueError(
            "SEC_USER_AGENT is not configured in the environment."
        )
        
    lookup = CompanyLookup(user_agent)
    company = lookup.find_company(company_name)

    print(
        f"Found company: {company['name']} "
        f"({company['ticker']})"
    )
    print(f"CIK: {company['cik']}")
    
    print("Fetching company data from SEC")
    client = SECClient()
    company_facts = client.get_company_facts(company['cik'])
    print("SEC data downloaded")

    parser = SECParser()

    financial_data = {}

    for metric in METRIC_TAGS:

        print(f"Extracting {metric}...")

        try:
            result = parser.extract_annual_metric(
                company_facts,
                metric
            )

            financial_data[metric] = result

            print(f"{metric} extracted")

        except Exception as e:
            print(f"Could not extract {metric}: {e}")
            
    combined = None

    for metric, df in financial_data.items():

        metric_df = df[
            ["fiscal_year", "value_billions"]
        ].copy()

        metric_df = metric_df.rename(
            columns={
                "value_billions": metric
            }
        )

        if combined is None:
            combined = metric_df

        else:
            combined = combined.merge(
                metric_df,
                on="fiscal_year",
                how="outer"
            )
    
    combined = combined.sort_values(
        "fiscal_year"
    ).reset_index(drop=True)
    
    output_dir = PROJECT_ROOT / "data" / "processed"

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_dir
        / f"{company['ticker'].lower()}_financials.csv"
    )

    combined.to_csv(
        output_file,
        index=False
    )

    print(f"Financial data saved to: {output_file}")

if __name__ == "__main__":
    main()