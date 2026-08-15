import requests
from dotenv import load_dotenv
import os

load_dotenv()

class SECClient:
    #Client for interacting with SEC EDGAR data

    BASE_URL = "https://data.sec.gov"

    def __init__(self):
        self.user_agent = os.getenv("SEC_USER_AGENT")

        if not self.user_agent:
            raise ValueError(
                "SEC_USER_AGENT is not configured in the environment."
            )

        self.headers = {
            "User-Agent": self.user_agent
        }

    def get_company_facts(self, cik: str) -> dict:
        #Retrieve company facts from SEC.

        cik = cik.zfill(10) #adds zeros to the beginning until the string has 10 characters 

        url = f"{self.BASE_URL}/api/xbrl/companyfacts/CIK{cik}.json"

        response = requests.get(
            url,
            headers=self.headers,
            timeout=30
        )

        response.raise_for_status()

        return response.json()