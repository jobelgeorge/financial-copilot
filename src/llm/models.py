import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "qwen/qwen3.8-27b"


class FinancialLLM:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured in the environment."
            )

        self.client = Groq(api_key=api_key)
        self.model = MODEL_NAME

    def generate(self, prompt: str) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content
