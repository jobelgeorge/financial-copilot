from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.application.financial_assistant import FinancialAssistant
from src.llm.models import FinancialLLM


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


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    question: str
    company: str
    tool: str
    answer: str
    answer_valid: bool


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
def ask(request: QuestionRequest):

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        result = assistant.ask(request.question)
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

            return AnswerResponse(
                question=request.question,
                company="N/A",
                tool="conversational",
                answer=fallback,
                answer_valid=True,
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

    return AnswerResponse(
        question=result["question"],
        company=result["company"],
        tool=result["tool"],
        answer=result["answer"],
        answer_valid=result["answer_valid"],
    )
