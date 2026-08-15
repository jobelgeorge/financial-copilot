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
            "Calculates year-over-year revenue growth "
            "for a company."
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
            "Calculates the compound annual growth rate "
            "of revenue over the available financial period."
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
            "Calculates net profit margin as a percentage "
            "of revenue."
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
            "Calculates the compound annual growth rate "
            "of net income."
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
            "Compares year-over-year revenue growth "
            "with net income growth."
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