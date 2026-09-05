import pandas as pd
import numpy as np


class AnswerGenerator:
    """
    Generates grounded natural-language answers
    from financial analysis tool results.
    """

    def __init__(self, llm):
        self.llm = llm

    def format_result(self, tool_name, result):
        """
        Convert tool results into a clean,
        LLM-friendly representation.
        """

        # Single numeric result
        if isinstance(result, (float, int, np.number)):

            if tool_name == "get_revenue_cagr":
                return (
                    f"Metric: Revenue CAGR\n"
                    f"Value: {float(result):.2f}%\n"
                    f"Meaning: Compound annual growth rate "
                    f"of revenue over the available period."
                )

            if tool_name == "get_net_income_cagr":
                return (
                    f"Metric: Net Income CAGR\n"
                    f"Value: {float(result):.2f}%\n"
                    f"Meaning: Compound annual growth rate "
                    f"of net income over the available period."
                )

            return f"Value: {float(result):.2f}"

        # Dictionary result
        if isinstance(result, dict):

            lines = []

            for key, value in result.items():

                if isinstance(value, float):
                    lines.append(
                        f"{key}: {value:.2f}"
                    )
                else:
                    lines.append(
                        f"{key}: {value}"
                    )

            return "\n".join(lines)

        # DataFrame result
        if isinstance(result, pd.DataFrame):

            df = result.copy()

            # Remove rows that contain no useful
            # financial information.
            df = df.dropna(
                how="all"
            )

            # Convert DataFrame into explicit
            # year-by-year observations.
            lines = []

            for _, row in df.iterrows():

                year = row.get("fiscal_year")

                values = []

                for column in df.columns:

                    if column == "fiscal_year":
                        continue

                    value = row[column]

                    if pd.isna(value):
                        continue

                    if isinstance(value, (float, int, np.number)):
                        values.append(
                            f"{column}={value:.2f}"
                        )
                    else:
                        values.append(
                            f"{column}={value}"
                        )

                if values:

                    lines.append(
                        f"{int(year)}: "
                        + ", ".join(values)
                    )

            return "\n".join(lines)

        return str(result)

    def build_prompt(
        self,
        question,
        company,
        tool_name,
        result
    ):
        """
        Build a grounded prompt.
        """

        formatted_result = self.format_result(
            tool_name,
            result
        )

        prompt = f"""
You are a financial analysis assistant.

Your job is to convert the financial tool result
into a concise answer to the user's question.

Company:
{company}

User question:
{question}

Financial tool used:
{tool_name}

Financial data:
{formatted_result}


STRICT GROUNDING RULES:

1. The financial data above is the ONLY source of truth.

2. Use ONLY numbers, years, and metrics explicitly
   present in the financial data.

3. NEVER calculate a new financial metric.

4. NEVER calculate an average, CAGR, percentage,
   difference, growth rate, or trend that is not
   already provided by the tool.

5. NEVER substitute one metric for another.

6. get_revenue_growth means YEAR-OVER-YEAR revenue
   growth. Do not describe it as CAGR.

7. get_revenue_cagr means LONG-TERM compound annual
   revenue growth. Do not describe it as yearly
   revenue growth.

8. get_net_income_cagr means LONG-TERM compound
   annual net income growth.

9. get_profit_margin means NET PROFIT MARGIN,
   calculated from net income and revenue.

10. get_asset_growth means YEAR-OVER-YEAR growth
    in total assets.

11. get_liability_to_asset_ratio means liabilities
    as a percentage of total assets.

12. get_operating_cash_flow_margin means operating
    cash flow as a percentage of revenue.

13. get_revenue_vs_income_growth compares revenue
    growth with net income growth.

14. get_latest_summary describes the latest available
    financial year only.

15. get_trend_summary describes the long-term trends
    explicitly provided by the tool.

16. NEVER mention EPS unless EPS appears in the
    financial data.

17. NEVER mention competitors.

18. NEVER mention causes, explanations, business
    events, products, markets, management decisions,
    economic conditions, or other external factors
    unless they appear explicitly in the financial data.

19. NEVER invent numbers.

20. NEVER invent years.

21. NEVER claim something is "consistently increasing"
    if the supplied data contains decreases.

22. If the data shows increases and decreases,
    describe the pattern as "fluctuating" or "mixed".

23. If the question asks whether something is improving,
    use only the supplied observations to answer.

24. If the supplied data does not contain enough
    information to answer the question, say:
    "The available financial data is insufficient
    to answer this question."

25. Do not add information simply to make the answer
    more detailed.

26. Keep the answer to 1-3 sentences.

27. Return ONLY the final answer.

IMPORTANT:
The tool has already performed the financial analysis.
Do not redo the analysis yourself.
Your task is ONLY to explain the supplied result.
"""

        return prompt

    def generate(
        self,
        question,
        company,
        tool_name,
        result,
        previous_answer=None
    ):
        """
        Generate the final grounded answer.
        """

        if previous_answer:

            prompt = self.build_prompt(
                question=question,
                company=company,
                tool_name=tool_name,
                result=result
            )

            prompt += f"""

        IMPORTANT:

        The previous answer failed financial validation.

        Previous answer:
        {previous_answer}

        Generate a new answer that is strictly supported
        by the financial data provided above.

        Do not repeat unsupported claims.
        """

        else:

            prompt = self.build_prompt(
                question=question,
                company=company,
                tool_name=tool_name,
                result=result
            )
    
        return self.llm.generate(prompt)