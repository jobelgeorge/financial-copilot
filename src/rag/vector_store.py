from pathlib import Path
from typing import List
from sentence_transformers import SentenceTransformer
import chromadb
import re

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_PATH = PROJECT_ROOT / "data" / "chroma"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


class VectorStore:

    def __init__(self):
        CHROMA_PATH.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)

    def _collection_name(self, company: str) -> str:
        name = company.lower()
        name = re.sub(r'[^a-zA-Z0-9]', '_', name)   # replace & . , etc with underscore
        name = re.sub(r'_+', '_', name)               # collapse multiple underscores
        name = name.strip('_')                         # remove leading/trailing underscores
        return f"{name}_10k"


    def is_ingested(self, company: str) -> bool:
        try:
            col = self.client.get_collection(self._collection_name(company))
            return col.count() > 0
        except Exception:
            return False

    def store(self, company: str, chunks: List[str]):

        col_name = self._collection_name(company)

        try:
            self.client.delete_collection(col_name)
        except Exception:
            pass

        collection = self.client.create_collection(col_name)
        embeddings = self.embedder.encode(chunks).tolist()

        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=[f"{col_name}_{i}" for i in range(len(chunks))],
            metadatas=[{"company": company, "chunk_index": i} for i in range(len(chunks))]
        )

        print(f"Stored {len(chunks)} chunks for {company} in ChromaDB.")

    def query(self, company: str, question: str, top_k: int = 5) -> List[str]:

        collection = self.client.get_collection(self._collection_name(company))
        question_embedding = self.embedder.encode([question]).tolist()

        results = collection.query(
            query_embeddings=question_embedding,
            n_results=top_k
        )

        return results["documents"][0]
