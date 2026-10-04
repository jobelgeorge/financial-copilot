# Financial Copilot

An LLM-powered financial analysis assistant grounded in real SEC EDGAR data.
Ask questions about any publicly listed US company in plain English and get
answers backed by verified financial data — quantitative metrics from 10-K
filings and qualitative insights from the full filing text.

---

## Live Demo

**Terminal 1 — API:**
```bash
python -m uvicorn src.api.main:app --port 8000
```

**Terminal 2 — UI:**
```bash
streamlit run app.py
```

Then open `http://localhost:8501`

---

## Architecture

```
+----------------------------------------------------------+
|                      Streamlit UI                        |
|                   Chat interface (app.py)                |
+-------------------------+--------------------------------+
                          | POST /ask
                          v
+----------------------------------------------------------+
|               FastAPI Backend  (src/api/main.py)         |
|          Answer Cache (1-hour TTL, in-memory)            |
+-------------------------+--------------------------------+
                          |
                          v
+----------------------------------------------------------+
|          AgentOrchestrator (agent_orchestrator.py)       |
|    Detects single-company vs multi-company questions     |
+----------+-------------------------------+---------------+
           |                               |
    Single company                  Multi-company
           |                               |
           v                               v
+----------------------+     +------------------------------+
|  FinancialAssistant  |     |  Execute tool per company    |
|                      |     |  Combine + compare results   |
| 1. ToolRouter        |     +------------------------------+
|    LLM -> tool name  |
|    + company name    |
|                      |
| 2. DataLoader        |     +------------------------------+
|    CSV cache +       |     |      RAG Pipeline            |
|    on-demand ingest  |     |                              |
|                      |     | TenKTextFetcher              |
| 3. ToolExecutor      |     |   -> SEC 10-K HTML download  |
|    Run metric fn     |     | TextChunker                  |
|                      |     |   -> 500-word passages       |
| 4. AnswerGenerator   |     | VectorStore (ChromaDB)       |
|    LLM + 27 rules    |     |   -> embed + store passages  |
|                      |     | Semantic search              |
| 5. AnswerValidator   |     |   -> top-5 relevant chunks   |
|    Fact-check vs     |     | LLM -> grounded answer       |
|    source data       |     +------------------------------+
|                      |
| 6. LLM Judge         |
|    Score 1-5 +       |
|    reasoning         |
+----------------------+
           |
           v
+----------------------------------------------------------+
|              SEC EDGAR REST API                          |
|   Financial data (XBRL) + 10-K filing text (HTML)       |
+----------------------------------------------------------+
```

---

## Key Features

- **LLM Tool Routing** — Maps natural language to the right analysis function
  using few-shot prompted LLM. No hardcoded keyword matching.

- **10 Financial Metrics** — Revenue growth, profit margins, operating cash flow
  margin, asset growth, liability-to-asset ratio, revenue CAGR, net income CAGR,
  revenue vs income growth, latest summary, trend summary.

- **RAG over 10-K Filing Text** — Qualitative questions (risks, strategy, causes)
  are answered by retrieving the most relevant passages from the actual 10-K filing
  using ChromaDB vector search. First query ingests the filing automatically.

- **Grounded Answer Generation** — 27 strict rules prevent hallucination. Answers
  are built only from SEC-verified data, never from the LLM's parametric memory.

- **Answer Validation + Regeneration** — Regex-based fact-checker verifies every
  numerical claim; if it fails, the LLM receives corrective feedback and retries.

- **LLM-as-Judge Evaluation** — A second LLM call scores every answer 1–5 for
  factual accuracy and identifies specific unsupported claims.

- **Agentic Multi-Company Comparison** — The AgentOrchestrator detects comparison
  questions ("Compare Apple and Tesla profitability"), runs the tool against each
  company, and synthesizes a unified comparative answer.

- **On-Demand Ingestion** — Any publicly listed US company works. If financial
  data is not cached locally, it is fetched live from SEC EDGAR at query time.

- **Answer Cache** — Identical questions are served instantly from a 1-hour
  in-memory cache with zero LLM calls.

- **Structured JSON Logging** — Every pipeline step (routing, execution, validation,
  judge scoring) is logged with latency in machine-readable JSON format.

- **Conversational Fallback** — Greetings, off-topic messages, and private company
  queries return a natural response instead of an error.

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq API — Qwen3 27B (`qwen/qwen3.8-27b`) |
| Backend API | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Vector Database | ChromaDB (persistent, local) |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Output Schemas | Pydantic v2 |
| Data Source | SEC EDGAR REST API (XBRL + 10-K filings) |
| Data Processing | Pandas + NumPy |
| Logging | Python logging with JSON formatter |
| Language | Python 3.11 |

---

## Project Structure

```
financial-copilot/
├── app.py                               # Streamlit chat UI
├── src/
│   ├── api/
│   │   └── main.py                      # FastAPI endpoints + answer cache
│   ├── application/
│   │   ├── financial_assistant.py       # Core pipeline orchestrator
│   │   └── agent_orchestrator.py        # Multi-company comparison agent
│   ├── llm/
│   │   ├── models.py                    # Groq LLM client
│   │   ├── tool_router.py               # Routes questions to tools (few-shot)
│   │   ├── tool_definitions.py          # Tool schemas + descriptions
│   │   ├── answer_generator.py          # LLM answer generation (27 rules)
│   │   ├── answer_validator.py          # Regex fact-checker
│   │   └── llm_judge.py                 # LLM-as-judge (score 1-5)
│   ├── rag/
│   │   ├── text_fetcher.py              # Downloads 10-K HTML from SEC EDGAR
│   │   ├── chunker.py                   # Splits text into 500-word passages
│   │   ├── vector_store.py              # ChromaDB embed + query wrapper
│   │   └── rag_pipeline.py              # RAG orchestrator (ingest + answer)
│   ├── tools/
│   │   ├── tool_executor.py             # Dispatches to analysis functions
│   │   └── tool_router.py               # (see llm/)
│   ├── analysis/
│   │   └── financial_analysis.py        # 10 financial metric functions
│   ├── schemas/
│   │   └── tool_outputs.py              # Pydantic models for tool results
│   ├── data/
│   │   └── financial_data_loader.py     # Loads CSV + in-memory DataFrame cache
│   ├── ingestion/
│   │   ├── sec_client.py                # SEC EDGAR XBRL API client
│   │   ├── sec_parser.py                # Parses XBRL financial data
│   │   ├── company_lookup.py            # Maps company names to CIK tickers
│   │   ├── financial_metrics.py         # Computes metrics from raw filings
│   │   └── pipeline.py                  # End-to-end ingestion pipeline
│   ├── utils/
│   │   └── logger.py                    # JSON structured logger
│   └── evaluation/
│       ├── evaluate_tool_router.py      # Tool routing accuracy
│       ├── evaluate_end_to_end.py       # Full pipeline accuracy
│       ├── evaluate_edge_cases.py       # Edge case handling
│       ├── evaluate_robustness.py       # Paraphrase robustness
│       └── failure_analysis.py          # Root cause classification
├── data/
│   ├── processed/                       # Company financial CSVs (auto-generated)
│   └── chroma/                          # ChromaDB vector store (auto-generated)
└── logs/
    └── financial_copilot.log            # Structured JSON logs
```

---

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/jobelgeorge/financial-copilot
cd financial-copilot
python -m venv fin
fin\Scripts\activate      # Windows
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
SEC_USER_AGENT=your_name your_email@example.com
```

- **GROQ_API_KEY** — Free at [console.groq.com](https://console.groq.com)
- **SEC_USER_AGENT** — Required by SEC EDGAR (any name + email)

### 3. Run the app

```bash
# Terminal 1 — API server
python -m uvicorn src.api.main:app --port 8000

# Terminal 2 — Chat UI
streamlit run app.py
```

No pre-ingestion needed. Financial data and 10-K text are fetched automatically
from SEC EDGAR the first time you ask about a company.

---

## Example Questions

| Question | Route |
|---|---|
| What is Apple's revenue trend? | `get_revenue_growth` |
| Is Tesla becoming more profitable? | `get_profit_margin` |
| What is Amazon's long-term revenue CAGR? | `get_revenue_cagr` |
| How much cash flow does Microsoft generate? | `get_operating_cash_flow_margin` |
| Give me a summary of Google's latest financials | `get_latest_summary` |
| What risks does Apple face? | `rag_search` → ChromaDB |
| Why did Tesla's revenue slow down? | `rag_search` → ChromaDB |
| What is Amazon's cloud strategy? | `rag_search` → ChromaDB |
| Compare Apple and Tesla's profit margins | `AgentOrchestrator` → multi-tool |
| Which is more profitable — Amazon or Microsoft? | `AgentOrchestrator` → multi-tool |

---

## How the Anti-Hallucination System Works

Standard LLMs freely invent financial numbers. This system prevents that through
four layers:

1. **Data grounding** — The LLM only sees real numbers from SEC filings or real
   text passages from the 10-K filing. It never generates numbers from memory.

2. **27-rule prompt constraints** — Rules like "never say consistently increasing
   if the data contains any decrease", "never state a number not present in the
   data", "never calculate a metric not already provided by the tool."

3. **Answer validation + regeneration** — A regex-based fact-checker verifies
   every numerical claim in the answer against the source data. If it fails, the
   LLM is shown the failing answer with explicit corrective feedback and asked to
   try again.

4. **LLM-as-judge** — A second independent LLM call scores the answer 1–5 and
   identifies specific unsupported claims. This catches semantic errors that regex
   cannot — such as correct numbers but wrong trend direction.

---

## Evaluation

The project includes a structured evaluation suite across 4 dimensions:

| Evaluation | What it measures |
|---|---|
| Tool routing accuracy | Does the LLM pick the right tool? |
| End-to-end accuracy | Is the final answer factually correct? |
| Edge case handling | Graceful responses for missing data, ambiguous questions |
| Robustness | Consistent answers under paraphrased inputs |

Run evaluations:

```bash
python -m src.evaluation.evaluate_end_to_end
```

---

## Data Source

Financial data is sourced from the
[SEC EDGAR REST API](https://data.sec.gov/api/xbrl/companyfacts/) using official
XBRL-tagged financial statement data from annual 10-K filings.
10-K filing text is fetched from the
[SEC EDGAR filing archives](https://www.sec.gov/cgi-bin/browse-edgar).
All data is publicly available.
