# Financial Copilot

An LLM-powered financial analysis assistant grounded in real SEC EDGAR data.
Ask questions about Apple, Tesla, and Amazon in plain English and get answers
backed by verified financial metrics — no hallucinated numbers.

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
+-----------------------------------------------------+
|                   Streamlit UI                      |
|              (Chat interface - app.py)               |
+----------------------+------------------------------+
                       | POST /ask
                       v
+-----------------------------------------------------+
|                  FastAPI Backend                     |
|              (src/api/main.py)                       |
+----------------------+------------------------------+
                       |
                       v
+-----------------------------------------------------+
|              FinancialAssistant                      |
|         (src/application/financial_assistant.py)     |
|                                                     |
|  1. ToolRouter  ---- LLM ---> tool + company name  |
|  2. DataLoader  -----------> load SEC CSV data      |
|  3. ToolExecutor ----------> run financial metric   |
|  4. AnswerGenerator -- LLM -> grounded answer       |
|  5. AnswerValidator -------> fact-check vs data     |
|     └── if invalid: regenerate with feedback        |
+----------------------+------------------------------+
                       |
                       v
+-----------------------------------------------------+
|              SEC EDGAR Data (CSV)                    |
|     Apple · Tesla · Amazon  (10-K filings)          |
+-----------------------------------------------------+
```

---

## Key Features

- **LLM Tool Routing** — Maps natural language questions to the right financial
  analysis function using few-shot prompted LLM (no hardcoded keywords)
- **9 Financial Metrics** — Revenue growth, profit margins, EPS, debt-to-equity,
  free cash flow, operating expenses, P/E ratio, YoY comparison, latest summary
- **Grounded Answer Generation** — 27 strict rules prevent hallucination;
  answers are built only from verified SEC data
- **Answer Validation + Regeneration** — Every answer is fact-checked against
  the raw numbers; if it fails, the LLM gets corrective feedback and tries again
- **Conversational Fallback** — Off-topic questions get a natural response
  instead of an error
- **REST API** — FastAPI backend with `/ask` and `/health` endpoints
- **Chat UI** — Streamlit chat interface with per-answer metadata

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq API — Qwen3 27B |
| Backend API | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Data Source | SEC EDGAR REST API |
| Data Processing | Pandas |
| Language | Python 3.11 |

---

## Project Structure

```
financial-copilot/
├── app.py                           # Streamlit chat UI
├── src/
│   ├── api/
│   │   └── main.py                  # FastAPI endpoints
│   ├── application/
│   │   └── financial_assistant.py   # Orchestrator — full pipeline
│   ├── llm/
│   │   ├── models.py                # LLM client (Groq API)
│   │   ├── tool_router.py           # Routes questions to tools
│   │   ├── answer_generator.py      # LLM answer generation
│   │   ├── answer_validator.py      # Fact-checks answers vs data
│   │   └── tool_definitions.py      # Tool schemas + few-shot examples
│   ├── tools/
│   │   └── tool_executor.py         # Executes the selected tool
│   ├── analysis/
│   │   └── financial_analysis.py    # 9 financial metric functions
│   ├── data/
│   │   └── financial_data_loader.py # Loads company CSV data
│   ├── ingestion/
│   │   ├── sec_client.py            # SEC EDGAR API client
│   │   ├── sec_parser.py            # Parses XBRL financial data
│   │   ├── financial_metrics.py     # Computes metrics from raw filings
│   │   └── pipeline.py              # End-to-end ingestion pipeline
│   └── evaluation/
│       ├── evaluate_tool_router.py  # Tool routing accuracy
│       ├── evaluate_end_to_end.py   # Full pipeline accuracy
│       ├── evaluate_edge_cases.py   # Edge case handling
│       ├── evaluate_robustness.py   # Input variation robustness
│       └── failure_analysis.py      # Root cause classification
```

---

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/your-username/financial-copilot
cd financial-copilot
python -m venv fin
fin\Scripts\activate      # Windows
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

Get a free API key at https://console.groq.com

### 3. Ingest financial data

```bash
python -m src.ingestion.pipeline --company apple
python -m src.ingestion.pipeline --company tesla
python -m src.ingestion.pipeline --company amazon
```

### 4. Run the app (two terminals)

```bash
# Terminal 1
python -m uvicorn src.api.main:app --port 8000

# Terminal 2
streamlit run app.py
```

---

## Example Questions

| Question | Tool Used |
|---|---|
| What is Apple's revenue trend? | `get_revenue_growth` |
| Is Tesla becoming more profitable? | `get_profit_margin` |
| How has Amazon's EPS changed over time? | `get_eps_trend` |
| What is Apple's debt-to-equity ratio? | `get_debt_to_equity` |
| How much free cash flow does Tesla generate? | `get_free_cash_flow` |
| Give me a summary of Amazon's latest financials | `get_latest_summary` |

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

## How the Anti-Hallucination System Works

Standard LLMs freely invent financial numbers. This system prevents that through
three layers:

1. **Data grounding** — The LLM only sees real numbers from SEC filings, never
   generates numbers from parametric memory
2. **27-rule prompt constraints** — Rules like "never say consistently increasing
   if the data contains any decrease", "never state a number not present in the data"
3. **Answer validation + regeneration** — Regex-based fact-checker verifies every
   claim in the answer against the source data; if it fails, the LLM is shown
   the bad answer and asked to correct it

---

## What's Next

- [ ] RAG layer — vector search over 10-K filing text for qualitative questions
- [ ] On-demand ingestion — any S&P 500 company, not just Apple/Tesla/Amazon
- [ ] LLM-as-judge evaluation — replace regex validator with semantic checking
- [ ] Multi-company comparison — agentic multi-tool reasoning
- [ ] Docker deployment

---

## Data Source

Financial data is sourced from the
[SEC EDGAR REST API](https://data.sec.gov/api/xbrl/companyfacts/) using official
XBRL-tagged financial statement data from annual 10-K filings.
All data is publicly available.
