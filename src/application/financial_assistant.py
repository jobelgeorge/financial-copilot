from src.tools.tool_router import ToolRouter
from src.tools.tool_executor import ToolExecutor
from src.data.financial_data_loader import FinancialDataLoader
from src.llm.answer_generator import AnswerGenerator
from src.llm.models import FinancialLLM
from src.llm.answer_validator import AnswerValidator
from src.rag.rag_pipeline import RAGPipeline
from src.llm.llm_judge import LLMJudge
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
        self.rag_pipeline = RAGPipeline()
        user_agent = os.getenv("SEC_USER_AGENT")

        if not user_agent:
            raise ValueError(
                "SEC_USER_AGENT is not configured in the environment."
            )

        self.loader = FinancialDataLoader(user_agent)
        self.answer_generator = AnswerGenerator(self.llm)
        self.answer_validator = AnswerValidator()
        self.llm_judge = LLMJudge(self.llm)
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
            
        # Step 2a: If qualitative question, use RAG instead of tool executor
        if tool_name == "rag_search":
            answer, context = self.rag_pipeline.answer(company, question, self.llm)
            judge_result = self.llm_judge.evaluate(question, context, answer)
            return {
                "question": question,
                "company": company,
                "tool": "rag_search",
                "result": {},
                "answer": answer,
                "answer_valid": True,
                "judge_score": judge_result["score"],
                "judge_reasoning": judge_result["reasoning"],
                "judge_passed": judge_result["passed"],
            }

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
        
        formatted_data = self.answer_generator.format_result(tool_name, result)
        judge_result = self.llm_judge.evaluate(question, formatted_data, answer)

        return {
            "question": question,
            "company": company,
            "tool": tool_name,
            "result": result,
            "answer": answer,
            "answer_valid": answer_valid,
            "judge_score": judge_result["score"],
            "judge_reasoning": judge_result["reasoning"],
            "judge_passed": judge_result["passed"],
        }
