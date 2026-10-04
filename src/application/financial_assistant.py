from src.tools.tool_router import ToolRouter
from src.tools.tool_executor import ToolExecutor
from src.data.financial_data_loader import FinancialDataLoader
from src.llm.answer_generator import AnswerGenerator
from src.llm.models import FinancialLLM
from src.llm.answer_validator import AnswerValidator
from src.rag.rag_pipeline import RAGPipeline
from src.llm.llm_judge import LLMJudge
from src.utils.logger import get_logger
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

logger = get_logger("financial_copilot.assistant")


class FinancialAssistant:

    def __init__(self):

        self.llm = FinancialLLM()
        self.router = ToolRouter(self.llm)
        self.rag_pipeline = RAGPipeline()

        user_agent = os.getenv("SEC_USER_AGENT")
        if not user_agent:
            raise ValueError("SEC_USER_AGENT is not configured in the environment.")

        self.loader = FinancialDataLoader(user_agent)
        self.answer_generator = AnswerGenerator(self.llm)
        self.answer_validator = AnswerValidator()
        self.llm_judge = LLMJudge(self.llm)

    def ask(self, question):

        # Step 1: Route
        t0 = time.time()
        route_result = self.router.route_question(question)

        if route_result is None:
            raise ValueError("The LLM could not determine an appropriate tool.")

        tool_name = route_result.get("tool")
        company = route_result.get("arguments", {}).get("company")

        logger.info(json.dumps({
            "event": "tool_routed",
            "question": question,
            "tool": tool_name,
            "company": company,
            "latency_ms": round((time.time() - t0) * 1000)
        }))

        if not tool_name:
            raise ValueError("No tool was selected.")

        if not company:
            raise ValueError("No company was identified.")

        # Step 2a: RAG path
        if tool_name == "rag_search":
            t1 = time.time()
            answer, context = self.rag_pipeline.answer(company, question, self.llm)

            judge_result = self.llm_judge.evaluate(question, context, answer)

            logger.info(json.dumps({
                "event": "rag_answered",
                "company": company,
                "judge_score": judge_result["score"],
                "latency_ms": round((time.time() - t1) * 1000)
            }))

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

        # Step 2b: Tool path
        t1 = time.time()
        financials = self.loader.load(company)
        executor = ToolExecutor(financials)
        result = executor.execute(tool_name)

        logger.info(json.dumps({
            "event": "tool_executed",
            "tool": tool_name,
            "company": company,
            "latency_ms": round((time.time() - t1) * 1000)
        }))

        # Step 3: Generate + validate
        max_attempts = 2
        answer = None
        answer_valid = False
        previous_answer = None

        for attempt in range(max_attempts):

            t2 = time.time()
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

            logger.info(json.dumps({
                "event": "answer_generated",
                "attempt": attempt + 1,
                "valid": answer_valid,
                "latency_ms": round((time.time() - t2) * 1000)
            }))

            if answer_valid:
                break

            previous_answer = answer

        # Step 4: Judge
        t3 = time.time()
        formatted_data = self.answer_generator.format_result(tool_name, result)
        judge_result = self.llm_judge.evaluate(question, formatted_data, answer)

        logger.info(json.dumps({
            "event": "judge_scored",
            "score": judge_result["score"],
            "passed": judge_result["passed"],
            "latency_ms": round((time.time() - t3) * 1000)
        }))

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
