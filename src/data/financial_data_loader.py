from pathlib import Path
from src.ingestion.company_lookup import CompanyLookup
from src.ingestion.pipeline import ingest_company
from src.utils.logger import get_logger
import json
import pandas as pd

logger = get_logger("financial_copilot.data")

class FinancialDataLoader:

    _cache: dict = {}

    def __init__(self, user_agent: str, processed_dir=None):

        self.user_agent = user_agent
        self.project_root = Path(__file__).resolve().parents[2]

        if processed_dir is None:
            self.processed_dir = self.project_root / "data" / "processed"
        else:
            self.processed_dir = Path(processed_dir)

        self.lookup = CompanyLookup(self.user_agent)

    def load(self, company_name: str) -> pd.DataFrame:

        company = self.lookup.find_company(company_name)
        ticker = company["ticker"].lower()

        if ticker in self._cache:
            logger.info(json.dumps({
                "event": "data_cache_hit",
                "company": company_name,
                "ticker": ticker
            }))
            return self._cache[ticker].copy()

        logger.info(json.dumps({
            "event": "data_cache_miss",
            "company": company_name,
            "ticker": ticker
        }))

        file_path = self.processed_dir / f"{ticker}_financials.csv"

        if not file_path.exists():
            logger.info(json.dumps({
                "event": "ingestion_started",
                "company": company_name
            }))
            ingest_company(company_name, self.user_agent)

        df = pd.read_csv(file_path)
        self._cache[ticker] = df

        logger.info(json.dumps({
            "event": "data_loaded",
            "company": company_name,
            "ticker": ticker,
            "rows": len(df)
        }))

        return df.copy()
