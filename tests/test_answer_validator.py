import pandas as pd

from src.llm.answer_validator import AnswerValidator


def test_profit_margin_rejects_false_consistency():

    df = pd.DataFrame({
        "fiscal_year": [
            2017, 2018, 2019, 2020
        ],
        "net_profit_margin_pct": [
            21.09, 22.41, 21.24, 20.91
        ]
    })

    validator = AnswerValidator()

    answer = (
        "Apple's profitability has "
        "consistently increased."
    )

    assert validator.validate(
        "get_profit_margin",
        df,
        answer
    ) is False
    

def test_profit_margin_accepts_fluctuating_answer():

    df = pd.DataFrame({
        "fiscal_year": [
            2017, 2018, 2019, 2020
        ],
        "net_profit_margin_pct": [
            21.09, 22.41, 21.24, 20.91
        ]
    })

    validator = AnswerValidator()

    answer = (
        "Apple's profitability fluctuated "
        "over the period."
    )

    assert validator.validate(
        "get_profit_margin",
        df,
        answer
    ) is True
    
def test_profit_margin_rejects_incorrect_percentage():

    df = pd.DataFrame({
        "fiscal_year": [
            2017, 2018, 2019, 2020
        ],
        "net_profit_margin_pct": [
            21.09, 22.41, 21.24, 20.91
        ]
    })

    validator = AnswerValidator()

    answer = (
        "Apple's profit margin increased "
        "from 21.09% to 25.88%."
    )

    assert validator.validate(
        "get_profit_margin",
        df,
        answer
    ) is False
    
def test_profit_margin_accepts_valid_percentage():

    df = pd.DataFrame({
        "fiscal_year": [
            2017, 2018, 2019, 2020
        ],
        "net_profit_margin_pct": [
            21.09, 22.41, 21.24, 20.91
        ]
    })

    validator = AnswerValidator()

    answer = (
        "Apple's profit margin was "
        "21.09% in 2017 and 20.91% in 2020."
    )

    assert validator.validate(
        "get_profit_margin",
        df,
        answer
    ) is True
    
def test_profit_margin_rejects_wrong_year_value_pair():

    df = pd.DataFrame({
        "fiscal_year": [
            2017, 2018, 2019, 2020, 2021,
            2022, 2023, 2024, 2025
        ],
        "net_profit_margin_pct": [
            21.09, 22.41, 21.24, 20.91, 25.88,
            25.31, 25.31, 23.97, 26.92
        ]
    })

    validator = AnswerValidator()

    answer = (
        "Apple's net profit margin increased "
        "from 21.09% in 2017 to 25.88% in 2024."
    )

    assert validator.validate(
        "get_profit_margin",
        df,
        answer
    ) is False
    
    
def test_profit_margin_accepts_correct_year_value_pair():

    df = pd.DataFrame({
        "fiscal_year": [
            2017, 2018, 2019, 2020, 2021,
            2022, 2023, 2024, 2025
        ],
        "net_profit_margin_pct": [
            21.09, 22.41, 21.24, 20.91, 25.88,
            25.31, 25.31, 23.97, 26.92
        ]
    })

    validator = AnswerValidator()

    answer = (
        "Apple's net profit margin was "
        "21.09% in 2017 and 26.92% in 2025."
    )

    assert validator.validate(
        "get_profit_margin",
        df,
        answer
    ) is True
    
def test_revenue_growth_rejects_false_consistency():

    df = pd.DataFrame({
        "fiscal_year": [
            2018, 2019, 2020, 2021
        ],
        "revenue_growth_pct": [
            15.86, -2.04, 5.51, 33.26
        ]
    })

    validator = AnswerValidator()

    answer = (
        "Apple's revenue consistently "
        "increased every year."
    )

    assert validator.validate(
        "get_revenue_growth",
        df,
        answer
    ) is False


def test_revenue_growth_accepts_fluctuating_answer():

    df = pd.DataFrame({
        "fiscal_year": [
            2018, 2019, 2020, 2021
        ],
        "revenue_growth_pct": [
            15.86, -2.04, 5.51, 33.26
        ]
    })

    validator = AnswerValidator()

    answer = (
        "Apple's revenue growth "
        "fluctuated over the period."
    )

    assert validator.validate(
        "get_revenue_growth",
        df,
        answer
    ) is True


def test_revenue_growth_rejects_incorrect_percentage():

    df = pd.DataFrame({
        "fiscal_year": [
            2018, 2019, 2020, 2021
        ],
        "revenue_growth_pct": [
            15.86, -2.04, 5.51, 33.26
        ]
    })

    validator = AnswerValidator()

    answer = (
        "Apple's revenue increased "
        "by 50% in 2020."
    )

    assert validator.validate(
        "get_revenue_growth",
        df,
        answer
    ) is False


def test_asset_growth_rejects_false_consistency():

    df = pd.DataFrame({
        "fiscal_year": [
            2019, 2020, 2021, 2022
        ],
        "asset_growth_pct": [
            5.0, -2.0, 8.0, 3.0
        ]
    })

    validator = AnswerValidator()

    answer = (
        "Apple's assets consistently "
        "increased every year."
    )

    assert validator.validate(
        "get_asset_growth",
        df,
        answer
    ) is False