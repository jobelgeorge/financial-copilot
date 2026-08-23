import json

from src.llm.models import FinancialLLM
from src.llm.tool_definitions import TOOLS


class ToolRouter:
    """
    Routes a user's financial question
    to the most appropriate financial tool.
    """

    def __init__(self):
        self.llm = FinancialLLM()

        self.few_shot_examples = [
            {
                "question": "How has Apple's revenue grown?",
                "tool": "get_revenue_growth",
            },
            {
                "question": "Is Apple's profitability improving?",
                "tool": "get_profit_margin",
            },
            {
                "question": "How quickly are Apple's assets growing?",
                "tool": "get_asset_growth",
            },
            {
                "question": "How much of Apple's assets are financed by liabilities?",
                "tool": "get_liability_to_asset_ratio",
            },
            {
                "question": "How has Apple's operating cash flow performed relative to revenue?",
                "tool": "get_operating_cash_flow_margin",
            },
            {
                "question": "What are Apple's latest financial results?",
                "tool": "get_latest_summary",
            },
            {
                "question": "What is Apple's long-term revenue growth rate?",
                "tool": "get_revenue_cagr",
            },
            {
                "question": "How has Apple's net income grown over the long term?",
                "tool": "get_net_income_cagr",
            },
            {
                "question": "Is Apple's net income growing faster than its revenue?",
                "tool": "get_revenue_vs_income_growth",
            },
            {
                "question": "What are the overall financial trends for Apple?",
                "tool": "get_trend_summary",
            },
            {
                "question": "How has Apple's revenue changed year over year?",
                "tool": "get_revenue_growth",
            },
            {
                "question": "What is Apple's long-term revenue CAGR?",
                "tool": "get_revenue_cagr",
            },
            {
                "question": "How has Apple's profitability changed?",
                "tool": "get_profit_margin",
            },
            {
                "question": "How quickly has Apple's net income grown over the long term?",
                "tool": "get_net_income_cagr",
            },
            {
                "question": "Is Apple's profit growing faster than its revenue?",
                "tool": "get_revenue_vs_income_growth",
            },
        ]

    def build_prompt(self, question):
        """
        Build the few-shot prompt used for tool selection.
        """

        examples_text = ""

        for example in self.few_shot_examples:
            examples_text += f"""
Question:
{example["question"]}

Correct tool:
{example["tool"]}

---
"""

        tool_descriptions = []

        for name, tool in TOOLS.items():
            tool_descriptions.append(
                f"""
Tool: {name}

Description:
{tool["description"]}

Input:
{tool["input"]}

Output:
{tool["output"]}
"""
            )

        tools_text = "\n".join(tool_descriptions)
        
        decision_rules = """
        Tool selection rules:

        1. REVENUE YEAR-OVER-YEAR GROWTH:
        Use get_revenue_growth when the question asks whether
        revenue or sales increased, decreased, or changed over
        time, especially when referring to yearly or recent growth.

        Examples:
        - How has Apple's revenue grown?
        - Is Apple's revenue increasing?
        - What is Apple's revenue growth rate?
        - Has Apple's revenue been growing consistently?

        Do NOT automatically interpret the words "growth",
        "growing", or "growth rate" as CAGR.

        2. REVENUE CAGR:
        Use get_revenue_cagr ONLY when the question explicitly
        refers to long-term growth, CAGR, compound annual growth,
        or average annual growth over a multi-year period.

        Examples:
        - What is Apple's revenue CAGR?
        - What is Apple's long-term revenue growth?
        - What has Apple's average annual revenue growth been?

        3. PROFIT MARGIN:
        Use get_profit_margin when the question asks about
        profitability, profit margin, or net margin.

        4. NET INCOME CAGR:
        Use get_net_income_cagr when the question asks how quickly
        net income or profit has grown over the long term or asks
        for net income CAGR.

        5. REVENUE VS NET INCOME:
        Use get_revenue_vs_income_growth when the question
        explicitly compares revenue growth with net income or
        profit growth.

        IMPORTANT:
        If the question contains a comparison such as:
        "faster than revenue",
        "compared with revenue",
        "outpaced revenue",
        "kept up with revenue",
        then use get_revenue_vs_income_growth.

        6. ASSET GROWTH:
        Use get_asset_growth when the question asks about growth
        in total assets or whether the company's balance sheet
        is getting larger.

        7. LIABILITY TO ASSET RATIO:
        Use get_liability_to_asset_ratio when the question asks
        about liabilities relative to assets, leverage, or the
        percentage of assets financed by liabilities.

        8. OPERATING CASH FLOW:
        Use get_operating_cash_flow_margin when the question asks
        about operating cash flow relative to revenue, cash
        generation efficiency, or operating cash flow margin.

        9. LATEST SUMMARY:
        Use get_latest_summary when the question asks for the
        latest financial results, latest financial year, or latest
        financial metrics.

        10. TREND SUMMARY:
            Use get_trend_summary when the question asks for an
            overall summary of long-term financial trends.

        Never invent a tool.
        Only select one of the provided tools.
        """

        prompt = f"""
You are a financial analysis assistant.

Your task is to select the single best tool
to answer the user's question.

Available tools:

{tools_text}

Decision rules:

{decision_rules}

Here are examples showing how questions
map to tools:

{examples_text}

Now classify this new question.

User question:
{question}

Return ONLY a valid JSON object:

{{
    "tool": "tool_name",
    "arguments": {{
        "company": "company_name"
    }}
}}

You may ONLY select one of the provided tools. 
Never invent a tool name.
"""

        return prompt

    def extract_tool(self, response):
        #Extract the tool name from the LLM response.

        if not response:
            return None

        response = response.strip()

        try:
            parsed = json.loads(response)

            return parsed

        except json.JSONDecodeError:
            pass

        # Try to find JSON inside the response
        start = response.find("{")
        end = response.rfind("}")

        if start != -1 and end != -1:
            try:
                parsed = json.loads(
                    response[start:end + 1]
                )

                return parsed

            except json.JSONDecodeError:
                pass

        return None

    def route_question(self, question):
        """
        Route a user question to the most appropriate tool.
        """

        prompt = self.build_prompt(question)

        response = self.llm.generate(prompt)

        result = self.extract_tool(response)

        return result
    
_default_router = ToolRouter()


def route_question(question):
    """
    Route a question using the default ToolRouter.
    """
    result = _default_router.route_question(question)

    if result is None:
        return None
    
    tool = result.get("tool")

    if tool not in TOOLS:
        return None

    return tool