import pandas as pd

from src.evaluation.root_cause_analysis import (
    RootCauseAnalyzer
)


def test_success_root_cause():

    df = pd.DataFrame([
        {
            "failure_type": "SUCCESS",
            "error": None,
        }
    ])

    analyzer = RootCauseAnalyzer(df)

    result = analyzer.analyze()

    assert (
        result.iloc[0]["root_cause"]
        == "SUCCESS"
    )


def test_liabilities_error_is_data_error():

    df = pd.DataFrame([
        {
            "failure_type": "SYSTEM_ERROR",
            "error": "'liabilities'",
        }
    ])

    analyzer = RootCauseAnalyzer(df)

    result = analyzer.analyze()

    assert (
        result.iloc[0]["root_cause"]
        == "DATA_ERROR"
    )


def test_company_error_is_routing_error():

    df = pd.DataFrame([
        {
            "failure_type": "COMPANY_ERROR",
            "error": None,
        }
    ])

    analyzer = RootCauseAnalyzer(df)

    result = analyzer.analyze()

    assert (
        result.iloc[0]["root_cause"]
        == "ROUTING_ERROR"
    )


def test_tool_error_is_routing_error():

    df = pd.DataFrame([
        {
            "failure_type": "TOOL_ROUTING_ERROR",
            "error": None,
        }
    ])

    analyzer = RootCauseAnalyzer(df)

    result = analyzer.analyze()

    assert (
        result.iloc[0]["root_cause"]
        == "ROUTING_ERROR"
    )


def test_validation_error():

    df = pd.DataFrame([
        {
            "failure_type": "ANSWER_VALIDATION_ERROR",
            "error": None,
        }
    ])

    analyzer = RootCauseAnalyzer(df)

    result = analyzer.analyze()

    assert (
        result.iloc[0]["root_cause"]
        == "VALIDATOR_ERROR"
    )