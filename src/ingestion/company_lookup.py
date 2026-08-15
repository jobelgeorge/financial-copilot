import requests


class CompanyLookup:
    #Lookup SEC CIK numbers from company names

    SEC_TICKERS_URL = (
        "https://www.sec.gov/files/company_tickers.json"
    )

    def __init__(self, user_agent: str):
        self.user_agent = user_agent

        self.headers = {
            "User-Agent": self.user_agent
        }

        self.companies = self._load_companies()

    def _load_companies(self) -> dict:
        #Download company ticker information from the SEC

        response = requests.get(
            self.SEC_TICKERS_URL,
            headers=self.headers,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    def find_company(self, company_name: str) -> dict:
        #Find a company by name.

        company_name = company_name.lower().strip()

        for company in self.companies.values():

            name = company["title"].lower()

            if company_name in name:

                return {
                    "name": company["title"],
                    "ticker": company["ticker"],
                    "cik": str(company["cik_str"]).zfill(10),
                }

        raise ValueError(
            f"Company not found: {company_name}"
        )