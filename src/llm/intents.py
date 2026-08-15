INTENTS = {
    "latest_summary": {
        "description": (
            "Get the latest available financial "
            "summary for a company."
        ),
        "tool": "get_latest_summary",
    },

    "revenue_growth": {
        "description": (
            "Analyze year-over-year revenue growth."
        ),
        "tool": "get_revenue_growth",
    },

    "revenue_cagr": {
        "description": (
            "Calculate compounded annual revenue growth."
        ),
        "tool": "get_revenue_cagr",
    },

    "profit_margin": {
        "description": (
            "Analyze net profit margin."
        ),
        "tool": "get_profit_margin",
    },

    "net_income_cagr": {
        "description": (
            "Calculate compounded annual net income growth."
        ),
        "tool": "get_net_income_cagr",
    },

    "cash_flow_margin": {
        "description": (
            "Analyze operating cash flow margin."
        ),
        "tool": "get_operating_cash_flow_margin",
    },

    "asset_growth": {
        "description": (
            "Analyze year-over-year asset growth."
        ),
        "tool": "get_asset_growth",
    },

    "liability_asset_ratio": {
        "description": (
            "Analyze liabilities relative to assets."
        ),
        "tool": "get_liability_to_asset_ratio",
    },

    "revenue_income_growth": {
        "description": (
            "Compare revenue growth with net income growth."
        ),
        "tool": "get_revenue_vs_income_growth",
    },

    "trend_summary": {
        "description": (
            "Provide a high-level summary of financial trends."
        ),
        "tool": "get_trend_summary",
    },
}