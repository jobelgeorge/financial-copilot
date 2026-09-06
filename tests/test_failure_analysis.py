import pandas as pd

from src.evaluation.failure_analysis import FailureAnalyzer


def test_success_is_classified_correctly():

    df = pd.DataFrame([
        {
            "company_correct": True,
            "tool_correct": True,
            "answer": "Apple revenue increased.",
            "answer_valid": True,
            "error": None,
        }
    ])

    analyzer = FailureAnalyzer(df)

    result = analyzer.analyze()

    assert result.iloc[0]["failure_type"] == "SUCCESS"


def test_validation_failure_is_classified_correctly():

    df = pd.DataFrame([
        {
            "company_correct": True,
            "tool_correct": True,
            "answer": "Apple profitability increased.",
            "answer_valid": False,
            "error": None,
        }
    ])

    analyzer = FailureAnalyzer(df)

    result = analyzer.analyze()

    assert (
        result.iloc[0]["failure_type"]
        == "ANSWER_VALIDATION_ERROR"
    )


def test_system_error_is_classified_correctly():

    df = pd.DataFrame([
        {
            "company_correct": False,
            "tool_correct": False,
            "answer": None,
            "answer_valid": False,
            "error": "'liabilities'",
        }
    ])

    analyzer = FailureAnalyzer(df)

    result = analyzer.analyze()

    assert (
        result.iloc[0]["failure_type"]
        == "SYSTEM_ERROR"
    )


def test_tool_error_is_classified_correctly():

    df = pd.DataFrame([
        {
            "company_correct": True,
            "tool_correct": False,
            "answer": "Some answer",
            "answer_valid": False,
            "error": None,
        }
    ])

    analyzer = FailureAnalyzer(df)

    result = analyzer.analyze()

    assert (
        result.iloc[0]["failure_type"]
        == "TOOL_ROUTING_ERROR"
    )