from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.application.financial_assistant import FinancialAssistant
from src.llm.models import FinancialLLM
from src.application.agent_orchestrator import AgentOrchestrator
from src.utils.logger import get_logger
import json
import time

logger = get_logger("financial_copilot.api")

_answer_cache: dict = {}
CACHE_TTL = 3600  # 1 hour


app = FastAPI(
    title="Financial Copilot API",
    description="LLM-powered financial analysis assistant grounded in SEC EDGAR data.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

assistant = FinancialAssistant()
orchestrator = AgentOrchestrator(assistant)


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    question: str
    company: str
    tool: str
    answer: str
    answer_valid: bool
    judge_score: int = 0
    judge_reasoning: str = ""
    judge_passed: bool = False


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
def ask(request: QuestionRequest):

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    question_key = request.question.lower().strip()
    t_start = time.time()

    logger.info(json.dumps({
        "event": "request_received",
        "question": request.question
    }))

    # Check answer cache
    cached = _answer_cache.get(question_key)
    if cached:
        result, cached_at = cached
        if time.time() - cached_at < CACHE_TTL:
            logger.info(json.dumps({
                "event": "cache_hit",
                "question": request.question
            }))
            return result

    logger.info(json.dumps({
        "event": "cache_miss",
        "question": request.question
    }))

    try:
        result = orchestrator.run(request.question)

    except ValueError:
        llm = FinancialLLM()
        fallback = llm.generate(
            f"""You are Financial Copilot, a helpful assistant specialized in analyzing 
        company financials from SEC EDGAR data.

        You can answer questions about any publicly listed US company — 
        revenue, profit margins, asset growth, cash flow, and more.

        Note: Private companies (like Anthropic, OpenAI, SpaceX) are not listed 
        on SEC EDGAR and have no public filings, so you cannot provide data for them.

        If the user sends a greeting or off-topic message, respond naturally and briefly,
        then mention what you can help with.

        If the user asks about a private company, politely explain it is not publicly 
        listed and suggest a similar public company if relevant.

        User message: {request.question}"""
        )

        response = AnswerResponse(
            question=request.question,
            company="N/A",
            tool="conversational",
            answer=fallback,
            answer_valid=True,
            judge_score=5,
            judge_reasoning="Conversational response, no evaluation needed.",
            judge_passed=True,
        )

        _answer_cache[question_key] = (response, time.time())
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

    response = AnswerResponse(
        question=result["question"],
        company=result["company"],
        tool=result["tool"],
        answer=result["answer"],
        answer_valid=result["answer_valid"],
        judge_score=result.get("judge_score", 0),
        judge_reasoning=result.get("judge_reasoning", ""),
        judge_passed=result.get("judge_passed", False),
    )

    _answer_cache[question_key] = (response, time.time())

    logger.info(json.dumps({
        "event": "request_completed",
        "company": result["company"],
        "tool": result["tool"],
        "judge_score": result.get("judge_score", 0),
        "total_latency_ms": round((time.time() - t_start) * 1000)
    }))

    return response

