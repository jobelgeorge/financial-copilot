import os
import requests
from bs4 import BeautifulSoup


class TenKTextFetcher:

    SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
    ARCHIVE_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{doc}"

    def __init__(self):
        self.user_agent = os.getenv("SEC_USER_AGENT")
        self.headers = {"User-Agent": self.user_agent}

    def get_latest_10k_text(self, cik: str) -> str:

        cik_padded = cik.zfill(10)
        url = self.SUBMISSIONS_URL.format(cik=cik_padded)

        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        filings = data["filings"]["recent"]
        forms = filings["form"]
        accession_numbers = filings["accessionNumber"]
        primary_documents = filings["primaryDocument"]

        for i, form in enumerate(forms):
            if form == "10-K":
                accession = accession_numbers[i].replace("-", "")
                primary_doc = primary_documents[i]
                cik_plain = str(int(cik))

                doc_url = self.ARCHIVE_URL.format(
                    cik=cik_plain,
                    accession=accession,
                    doc=primary_doc
                )

                doc_response = requests.get(
                    doc_url, headers=self.headers, timeout=60
                )
                doc_response.raise_for_status()

                soup = BeautifulSoup(doc_response.content, "html.parser")

                for tag in soup(["script", "style", "table"]):
                    tag.decompose()

                text = soup.get_text(separator="\n")

                lines = [line.strip() for line in text.splitlines()]
                lines = [line for line in lines if len(line) > 30]

                return "\n".join(lines)

        raise ValueError(f"No 10-K filing found for CIK {cik}")
