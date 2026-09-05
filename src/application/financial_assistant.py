from src.tools.tool_router import ToolRouter
from src.tools.tool_executor import ToolExecutor
from src.data.financial_data_loader import FinancialDataLoader
from src.llm.answer_generator import AnswerGenerator
from src.llm.models import FinancialLLM
from src.llm.answer_validator import AnswerValidator
import os
from dotenv import load_dotenv

load_dotenv()

class FinancialAssistant:
    """
    End-to-end financial analysis assistant.

    Takes a user's natural-language question,
    selects the appropriate financial tool,
    loads the company's financial data,
    and executes the selected analysis.
    """

    def __init__(self):

        self.llm = FinancialLLM()

        self.router = ToolRouter(
            self.llm
        )
        user_agent = os.getenv("SEC_USER_AGENT")

        if not user_agent:
            raise ValueError(
                "SEC_USER_AGENT is not configured in the environment."
            )

        self.loader = FinancialDataLoader(user_agent)
        self.answer_generator = AnswerGenerator(self.llm)
        self.answer_validator = AnswerValidator()

    def ask(self, question):
        # Process a user's financial question.

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
        
        max_attempts = 2

        answer = None
        answer_valid = False
        previous_answer = None

        for attempt in range(max_attempts):

            answer = self.answer_generator.generate(
                question=question,
                company=company,
                tool_name=tool_name,
                result=result,
                previous_answer=previous_answer
            )

            answer_valid = self.answer_validator.validate(
                tool_name=tool_name,
                result=result,
                answer=answer
            )

            print(
                f"Answer validation attempt "
                f"{attempt + 1}: {answer_valid}"
            )

            if answer_valid:
                break

            previous_answer = answer
        
        return {
            "question": question,
            "company": company,
            "tool": tool_name,
            "result": result,
            "answer": answer,
            "answer_valid": answer_valid,
        }