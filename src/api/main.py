from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.application.financial_assistant import FinancialAssistant

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
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

    return AnswerResponse(
        question=result["question"],
        company=result["company"],
        tool=result["tool"],
        answer=result["answer"],
        answer_valid=result["answer_valid"],
    )
