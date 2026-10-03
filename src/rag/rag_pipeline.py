import os
from src.ingestion.company_lookup import CompanyLookup
from src.rag.text_fetcher import TenKTextFetcher
from src.rag.chunker import TextChunker
from src.rag.vector_store import VectorStore


class RAGPipeline:

    def __init__(self):
        user_agent = os.getenv("SEC_USER_AGENT")
        self.lookup = CompanyLookup(user_agent)
        self.fetcher = TenKTextFetcher()
        self.chunker = TextChunker(chunk_size=500, overlap=50)
        self.store = VectorStore()

    def ensure_ingested(self, company: str):

        if self.store.is_ingested(company):
            return

        print(f"Fetching 10-K text for {company} from SEC EDGAR...")
        company_info = self.lookup.find_company(company)
        text = self.fetcher.get_latest_10k_text(company_info["cik"])
        chunks = self.chunker.chunk(text)
        self.store.store(company, chunks)

    def answer(self, company: str, question: str, llm) -> str:

        self.ensure_ingested(company)

        chunks = self.store.query(company, question, top_k=5)
        context = "\n\n---\n\n".join(chunks)

        prompt = f"""You are a financial analysis assistant.

Answer the user's question using ONLY the context below from {company}'s SEC 10-K filing.

If the context does not contain enough information, say:
"The 10-K filing does not contain sufficient information to answer this question."

Do not add any information from outside the context.
Keep the answer to 2-4 sentences.

Company: {company}

Context from 10-K filing:
{context}

User question: {question}

Answer:"""

        return llm.generate(prompt), context

