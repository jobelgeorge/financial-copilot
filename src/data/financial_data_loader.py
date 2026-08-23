from pathlib import Path
from src.ingestion.company_lookup import CompanyLookup
import pandas as pd

class FinancialDataLoader:
    #Loads processed financial data for a company.

    def __init__(
        self,
        user_agent: str,
        processed_dir=None
    ):

        self.user_agent = user_agent

        self.project_root = (
            Path(__file__).resolve().parents[2]
        )

        if processed_dir is None:

            self.processed_dir = (
                self.project_root
                / "data"
                / "processed"
            )

        else:

            self.processed_dir = Path(
                processed_dir
            )

        self.lookup = CompanyLookup(
            self.user_agent
        )

    def load(self, company_name: str) -> pd.DataFrame:
        """
        Find a company and load its processed
        financial CSV.
        """

        company = self.lookup.find_company(
            company_name
        )

        ticker = company["ticker"].lower()

        file_path = (
            self.processed_dir
            / f"{ticker}_financials.csv"
        )

        if not file_path.exists():
            raise FileNotFoundError(
                f"No processed financial data found "
                f"for {company_name} "
                f"({ticker}). "
                f"Run the ingestion pipeline first."
            )

        financials = pd.read_csv(
            file_path
        )

        return financials