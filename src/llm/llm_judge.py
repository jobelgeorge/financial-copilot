class LLMJudge:
    """
    Evaluates whether a generated answer is accurately
    supported by the underlying financial data or context.
    """

    def __init__(self, llm):
        self.llm = llm

    def evaluate(self, question: str, formatted_data: str, answer: str) -> dict:

        prompt = f"""You are a financial fact-checker.

Evaluate whether the answer below is accurately supported by the financial data provided.

Financial data:
{formatted_data}

Answer to evaluate:
{answer}

Evaluate strictly on these criteria:
1. Every number in the answer must appear in the data
2. Trend claims must match the data exactly (e.g. "consistently increasing" is wrong if any year shows a decline)
3. The answer must not introduce facts, causes, or context not present in the data

Respond in EXACTLY this format with no extra text:
SCORE: <integer from 1 to 5>
REASONING: <one sentence explaining the score>
ISSUES: <specific unsupported claims, or "None">

Scoring guide:
5 = Every claim is directly supported by the data
4 = Mostly accurate, very minor imprecision in wording
3 = One claim is unsupported or slightly inaccurate
2 = Multiple unsupported or incorrect claims
1 = Answer is largely not supported by the data
"""

        response = self.llm.generate(prompt)
        return self._parse(response)

    def _parse(self, response: str) -> dict:

        score = 3
        reasoning = ""
        issues = ""

        for line in response.strip().split("\n"):
            line = line.strip()
            if line.startswith("SCORE:"):
                try:
                    score = int(line.replace("SCORE:", "").strip())
                    score = max(1, min(5, score))
                except ValueError:
                    score = 3
            elif line.startswith("REASONING:"):
                reasoning = line.replace("REASONING:", "").strip()
            elif line.startswith("ISSUES:"):
                issues = line.replace("ISSUES:", "").strip()

        return {
            "score": score,
            "reasoning": reasoning,
            "issues": issues,
            "passed": score >= 4,
        }
