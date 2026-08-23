TOOLS = {

    "get_latest_summary": {
        "description": (
            "Returns the latest available financial "
            "metrics for a company."
        ),
        "input": {
            "company": "string"
        },
        "output": {
            "fiscal_year": "integer",
            "revenue_billions": "float",
            "net_income_billions": "float",
            "assets_billions": "float",
            "liabilities_billions": "float",
            "cash_billions": "float",
            "operating_cash_flow_billions": "float"
        }
    },

    "get_revenue_growth": {
        "description": (
            "Measures how much a company's revenue changes "
            "from one fiscal year to the next. Use this tool "
            "when the question asks about year-over-year revenue "
            "growth, recent revenue growth, sales growth, or "
            "whether revenue is increasing or decreasing. "
            "Do NOT use this tool for long-term average growth "
            "or CAGR questions."
        ),
        "input": {
            "company": "string"
        },
        "output": {
            "fiscal_year": "integer",
            "revenue": "float",
            "revenue_growth_pct": "float"
        }
    },

    "get_revenue_cagr": {
        "description": (
            "Calculates the compound annual growth rate (CAGR) "
            "of revenue over the entire available financial period. "
            "Use this tool when the question explicitly asks about "
            "long-term revenue growth, average annual revenue growth, "
            "revenue CAGR, or how quickly revenue grew over a long "
            "period. Do NOT use this tool for simple year-over-year "
            "revenue growth."
        ),
        "input": {
            "company": "string"
        },
        "output": {
            "revenue_cagr_pct": "float"
        }
    },

    "get_profit_margin": {
        "description": (
            "Calculates net profit margin, which is net income "
            "divided by revenue. Use this tool when the question "
            "asks about profitability, profit margin, net margin, "
            "or whether the company is becoming more profitable. "
            "This measures profitability, not the growth rate of "
            "net income."
        ),
        "input": {
            "company": "string"
        },
        "output": {
            "fiscal_year": "integer",
            "net_profit_margin_pct": "float"
        }
    },

    "get_net_income_cagr": {
        "description": (
            "Calculates the compound annual growth rate (CAGR) "
            "of net income over the available financial period. "
            "Use this tool when the question asks how quickly "
            "profit or net income has grown over the long term. "
            "Do NOT use this tool when the question asks about "
            "profit margin or profitability."
        ),
        "input": {
            "company": "string"
        },
        "output": {
            "net_income_cagr_pct": "float"
        }
    },

    "get_operating_cash_flow_margin": {
        "description": (
            "Calculates operating cash flow as a "
            "percentage of revenue."
        ),
        "input": {
            "company": "string"
        },
        "output": {
            "fiscal_year": "integer",
            "operating_cash_flow_margin_pct": "float"
        }
    },

    "get_asset_growth": {
        "description": (
            "Calculates year-over-year growth in "
            "total assets."
        ),
        "input": {
            "company": "string"
        },
        "output": {
            "fiscal_year": "integer",
            "asset_growth_pct": "float"
        }
    },

    "get_liability_to_asset_ratio": {
        "description": (
            "Calculates liabilities as a percentage "
            "of total assets."
        ),
        "input": {
            "company": "string"
        },
        "output": {
            "fiscal_year": "integer",
            "liability_to_asset_pct": "float"
        }
    },

    "get_revenue_vs_income_growth": {
        "description": (
            "Compares year-over-year revenue growth with "
            "year-over-year net income growth. Use this tool "
            "when the question explicitly compares revenue "
            "growth against net income or profit growth, such as "
            "whether profit is growing faster than sales. "
            "Do NOT use this tool for questions about profit "
            "margin alone."
        ),
        "input": {
            "company": "string"
        },
        "output": {
            "fiscal_year": "integer",
            "revenue_growth_pct": "float",
            "net_income_growth_pct": "float",
            "growth_difference_pct": "float"
        }
    },

    "get_trend_summary": {
        "description": (
            "Provides a high-level summary of long-term "
            "financial trends for a company."
        ),
        "input": {
            "company": "string"
        },
        "output": {
            "revenue_cagr_pct": "float",
            "net_income_cagr_pct": "float",
            "average_revenue_growth_pct": "float",
            "average_net_income_growth_pct": "float",
            "starting_profit_margin_pct": "float",
            "latest_profit_margin_pct": "float",
            "profit_margin_change_pct": "float"
        }
    }
}