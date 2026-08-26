from src.tools.tool_router import ToolRouter
from src.tools.tool_executor import ToolExecutor
from src.data.financial_data_loader import FinancialDataLoader
import os

class FinancialAssistant:
    """
    End-to-end financial analysis assistant.

    Takes a user's natural-language question,
    selects the appropriate financial tool,
    loads the company's financial data,
    and executes the selected analysis.
    """

    def __init__(self):

        self.router = ToolRouter()
        user_agent = os.getenv("SEC_USER_AGENT")

        if not user_agent:
            raise ValueError(
                "SEC_USER_AGENT is not configured in the environment."
            )

        self.loader = FinancialDataLoader(user_agent)

    def ask(self, question):
        """
        Process a user's financial question.
        """

        # Step 1: Determine which tool to use
        route_result = self.router.route_question(question)

        if route_result is None:
            raise ValueError(
                "The LLM could not determine an appropriate tool."
            )

        tool_name = route_result.get("tool")

        company = route_result.get(
            "arguments",
            {}
        ).get(
            "company"
        )

        if not tool_name:
            raise ValueError(
                "No tool was selected."
            )

        if not company:
            raise ValueError(
                "No company was identified."
            )

        # Step 2: Load financial data
        financials = self.loader.load(company)

        # Step 3: Execute the selected tool
        executor = ToolExecutor(financials)

        result = executor.execute(tool_name)

        return {
            "question": question,
            "company": company,
            "tool": tool_name,
            "result": result,
        }