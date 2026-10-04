import os
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import requests
from dotenv import load_dotenv

from src.data.financial_data_loader import FinancialDataLoader
from src.analysis.financial_analysis import FinancialAnalyzer

load_dotenv()

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Financial Copilot",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #0f1117;
}
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #e0e0e0 !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #1e2130 !important;
    border-color: #3d4260 !important;
    color: #ffffff !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #ffffff !important;
}
[data-testid="stSidebar"] hr {
    border-color: #2d3250;
}
div[data-testid="metric-container"] {
    background: #1e2130;
    border: 1px solid #2d3250;
    border-radius: 8px;
    padding: 16px;
}
</style>
""", unsafe_allow_html=True)


COMPANIES = [
    "Apple", "Microsoft", "Tesla", "Amazon",
    "NVIDIA", "Meta", "Netflix", "Walmart",
    "JPMorgan", "Intel"
]


@st.cache_data(ttl=3600, show_spinner=False)
def load_data(company_name: str):
    user_agent = os.getenv("SEC_USER_AGENT")
    loader = FinancialDataLoader(user_agent)
    return loader.load(company_name)


# Sidebar
with st.sidebar:

    st.markdown("""
    <div style='text-align:center; padding: 12px 0 4px 0;'>
        <div style='font-size: 2.8rem;'>📈</div>
        <div style='font-size: 1.3rem; font-weight: 700; color: white;'>Financial Copilot</div>
        <div style='font-size: 0.78rem; color: #888; margin-top: 2px;'>
            Grounded in SEC EDGAR 10-K filings
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(
        "<div style='color:#888; font-size:0.72rem; letter-spacing:1px;"
        " margin-bottom:4px;'>COMPANY</div>",
        unsafe_allow_html=True
    )
    company = st.selectbox("Company", COMPANIES, label_visibility="collapsed")

    # Show ticker hint below selector
    TICKERS = {
        "Apple": "AAPL", "Microsoft": "MSFT", "Tesla": "TSLA",
        "Amazon": "AMZN", "NVIDIA": "NVDA", "Meta": "META",
        "Netflix": "NFLX", "Walmart": "WMT", "JPMorgan": "JPM", "Intel": "INTC"
    }
    ticker = TICKERS.get(company, "")
    if ticker:
        st.markdown(
            f"<div style='color:#555; font-size:0.75rem; margin-top:-8px;"
            f" margin-bottom:8px;'>Ticker: {ticker}</div>",
            unsafe_allow_html=True
        )

    st.divider()

    st.markdown(
        "<div style='color:#888; font-size:0.72rem; letter-spacing:1px;"
        " margin-bottom:8px;'>NAVIGATE</div>",
        unsafe_allow_html=True
    )

    if "page" not in st.session_state:
        st.session_state.page = "dashboard"

    if st.button(
        " Dashboard",
        use_container_width=True,
        type="primary" if st.session_state.page == "dashboard" else "secondary"
    ):
        st.session_state.page = "dashboard"
        st.rerun()

    if st.button(
        " Talk to your data",
        use_container_width=True,
        type="primary" if st.session_state.page == "chat" else "secondary"
    ):
        st.session_state.page = "chat"
        st.rerun()

    st.divider()

    st.markdown("""
    <div style='color:#555; font-size:0.73rem; line-height:1.8;'>
        <div>&nbsp;LLM — Groq · Qwen3 27B</div>
        <div>&nbsp;RAG — ChromaDB · MiniLM</div>
        <div>&nbsp;Eval — LLM-as-Judge</div>
        <div>&nbsp;Data — SEC EDGAR 10-K</div>
    </div>
    """, unsafe_allow_html=True)


if st.session_state.page == "dashboard":

    st.title(f"{company} — Financial Dashboard")
    st.caption("Annual data from SEC EDGAR 10-K filings · All figures in USD billions")

    with st.spinner(f"Loading {company} financial data from SEC EDGAR..."):
        try:
            df = load_data(company)
            analyzer = FinancialAnalyzer(df)
        except Exception as e:
            st.error(f"Could not load data for {company}. Error: {e}")
            st.stop()

    df_sorted = df.sort_values("fiscal_year").reset_index(drop=True)
    latest = df_sorted.iloc[-1]
    prev = df_sorted.iloc[-2] if len(df_sorted) > 1 else None

    revenue = float(latest["revenue"])
    net_income = float(latest["net_income"])
    cash = float(latest["cash"])
    assets = float(latest["assets"])
    liabilities = float(latest["liabilities"])
    op_cf = float(latest["operating_cash_flow"])
    profit_margin = (net_income / revenue * 100) if revenue else 0
    cf_margin = (op_cf / revenue * 100) if revenue else 0
    liab_ratio = (liabilities / assets * 100) if assets else 0

    rev_delta = None
    ni_delta = None
    if prev is not None:
        prev_rev = float(prev["revenue"])
        prev_ni = float(prev["net_income"])
        rev_delta = f"{((revenue - prev_rev) / prev_rev * 100):+.1f}% YoY"
        ni_delta = f"{((net_income - prev_ni) / prev_ni * 100):+.1f}% YoY"

    # Key Metric Cards
    st.subheader("Key Metrics — Latest Fiscal Year")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Revenue", f"${revenue:.1f}B", rev_delta)
    c2.metric("Net Income", f"${net_income:.1f}B", ni_delta)
    c3.metric("Profit Margin", f"{profit_margin:.1f}%")
    c4.metric("Cash", f"${cash:.1f}B")
    c5.metric("Cash Flow Margin", f"{cf_margin:.1f}%")
    c6.metric("Liability Ratio", f"{liab_ratio:.1f}%")

    st.divider()

    # Row 1: Revenue + Profit Margin
    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(
            df_sorted, x="fiscal_year", y="revenue",
            title="Revenue ($B)",
            markers=True,
            color_discrete_sequence=["#4f8ef7"]
        )
        fig.update_layout(
            xaxis_title="Year", yaxis_title="Revenue ($B)",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        margin_df = analyzer.net_profit_margin()
        fig2 = px.line(
            margin_df, x="fiscal_year", y="net_profit_margin_pct",
            title="Net Profit Margin (%)",
            markers=True,
            color_discrete_sequence=["#00cc88"]
        )
        fig2.update_layout(
            xaxis_title="Year", yaxis_title="Margin (%)",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Row 2: Revenue vs Net Income + Assets vs Liabilities 
    col3, col4 = st.columns(2)

    with col3:
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=df_sorted["fiscal_year"], y=df_sorted["revenue"],
            name="Revenue", marker_color="#4f8ef7"
        ))
        fig3.add_trace(go.Bar(
            x=df_sorted["fiscal_year"], y=df_sorted["net_income"],
            name="Net Income", marker_color="#00cc88"
        ))
        fig3.update_layout(
            title="Revenue vs Net Income ($B)",
            barmode="group",
            xaxis_title="Year", yaxis_title="$B",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=df_sorted["fiscal_year"], y=df_sorted["assets"],
            name="Assets", marker_color="#4f8ef7"
        ))
        fig4.add_trace(go.Bar(
            x=df_sorted["fiscal_year"], y=df_sorted["liabilities"],
            name="Liabilities", marker_color="#ff4d4d"
        ))
        fig4.update_layout(
            title="Assets vs Liabilities ($B)",
            barmode="group",
            xaxis_title="Year", yaxis_title="$B",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig4, use_container_width=True)

    # Row 3: Cash Flow + Asset/Liability Pie
    col5, col6 = st.columns(2)

    with col5:
        cf_df = analyzer.operating_cash_flow_margin()
        fig5 = px.area(
            cf_df, x="fiscal_year", y="operating_cash_flow_margin_pct",
            title="Operating Cash Flow Margin (%)",
            color_discrete_sequence=["#a855f7"]
        )
        fig5.update_layout(
            xaxis_title="Year", yaxis_title="Margin (%)",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        fig6 = px.pie(
            values=[liabilities, assets - liabilities],
            names=["Liabilities", "Equity"],
            title=f"Balance Sheet Composition — Latest Year",
            color_discrete_sequence=["#ff4d4d", "#4f8ef7"],
            hole=0.4
        )
        fig6.update_layout(paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig6, use_container_width=True)


# Chat 
elif st.session_state.page == "chat":

    st.title("Talk to your data")
    st.caption(
        "Ask about any publicly listed US company. "
        "Data is fetched live from SEC EDGAR."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("metadata"):
                meta = message["metadata"]
                cols = st.columns(4)
                cols[0].caption(f"**Company:** {meta['company']}")
                cols[1].caption(f"**Tool:** `{meta['tool']}`")
                cols[2].caption(f"**Validated:** {meta['answer_valid']}")
                if meta.get("judge_score"):
                    cols[3].caption(f"**Accuracy:** {meta['judge_score']}/5")

    if prompt := st.chat_input(
        f"e.g. What are {company}'s risks? Compare Apple and Tesla revenue."
    ):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                try:
                    response = requests.post(
                        f"{API_URL}/ask",
                        json={"question": prompt},
                        timeout=120
                    )
                    if not response.ok:
                        raise requests.exceptions.HTTPError(response=response)

                    data = response.json()
                    answer = data["answer"]
                    metadata = {
                        "company": data["company"],
                        "tool": data["tool"],
                        "answer_valid": "Yes" if data["answer_valid"] else "No",
                        "judge_score": data.get("judge_score"),
                    }
                    st.markdown(answer)
                    cols = st.columns(4)
                    cols[0].caption(f"**Company:** {metadata['company']}")
                    cols[1].caption(f"**Tool:** `{metadata['tool']}`")
                    cols[2].caption(f"**Validated:** {metadata['answer_valid']}")
                    if metadata["judge_score"]:
                        cols[3].caption(f"**Accuracy:** {metadata['judge_score']}/5")

                except requests.exceptions.HTTPError as e:
                    try:
                        detail = e.response.json().get("detail", str(e))
                    except Exception:
                        detail = str(e)
                    answer = f"{detail}"
                    metadata = None
                    st.error(answer)

                except Exception as e:
                    answer = f"Error: {str(e)}"
                    metadata = None
                    st.error(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "metadata": metadata
        })
