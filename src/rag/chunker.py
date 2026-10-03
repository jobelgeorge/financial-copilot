from typing import List


class TextChunker:

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[str]:

        words = text.split()
        chunks = []
        start = 0

        while start < len(words):
            end = start + self.chunk_size
            chunk_text = " ".join(words[start:end])

            if len(chunk_text.strip()) > 100:
                chunks.append(chunk_text)

            start += self.chunk_size - self.overlap

        return chunks
