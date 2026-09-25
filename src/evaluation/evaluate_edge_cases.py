import numpy as np
import pandas as pd

from src.analysis.financial_analysis import FinancialAnalyzer


def classify_result(result, expected_behavior, error):
    """
    Classify the outcome of an edge-case test.

    Categories:
        PASS
        EXPECTED_UNDEFINED
        NUMERICAL_FAILURE
        SEMANTIC_WARNING
        DATA_HANDLING_FAILURE
    """

    # ---------------------------------------------------------
    # Expected undefined results
    # ---------------------------------------------------------

    if expected_behavior in {
        "RETURN_NAN",
        "RETURN_ZERO_OR_NAN",
    }:

        if result is None:
            return "DATA_HANDLING_FAILURE"

        if isinstance(result, (float, np.floating)):

            if np.isnan(result):
                return "EXPECTED_UNDEFINED"

            if np.isinf(result):
                return "NUMERICAL_FAILURE"

            return "PASS"

    # ---------------------------------------------------------
    # Explicit semantic review
    # ---------------------------------------------------------

    if expected_behavior == "SEMANTIC_REVIEW":
        return "SEMANTIC_WARNING"

    # ---------------------------------------------------------
    # DataFrame results
    # ---------------------------------------------------------

    if isinstance(result, pd.DataFrame):

        numeric_columns = result.select_dtypes(
            include=[np.number]
        )

        # Infinite values are numerical failures.
        if np.isinf(
            numeric_columns.to_numpy()
        ).any():

            return "NUMERICAL_FAILURE"

        # NaN values are not automatically failures.
        #
        # Examples:
        # - first pct_change() observation
        # - unavailable growth because previous value is missing
        #
        # These can be legitimate analytical results.

        return "PASS"

    # ---------------------------------------------------------
    # Dictionary results
    # ---------------------------------------------------------

    if isinstance(result, dict):

        for value in result.values():

            if isinstance(
                value,
                (int, float, np.number)
            ):

                if np.isinf(value):
                    return "NUMERICAL_FAILURE"

        return "PASS"

    # ---------------------------------------------------------
    # Scalar numerical results
    # ---------------------------------------------------------

    if isinstance(
        result,
        (int, float, np.number)
    ):

        if np.isinf(result):
            return "NUMERICAL_FAILURE"

        if np.isnan(result):

            if expected_behavior in {
                "RETURN_NAN",
                "RETURN_ZERO_OR_NAN",
            }:
                return "EXPECTED_UNDEFINED"

            return "NUMERICAL_FAILURE"

        return "PASS"

    return "PASS"


def determine_test_outcome(
    expected_behavior,
    classification,
    error
):
    """
    Determine whether observed behavior matches
    the desired behavior.
    """

    # Any exception means the system did not
    # behave as expected.
    if error:
        return "UNEXPECTED"

    if expected_behavior == "VALID_RESULT":
        return (
            "EXPECTED"
            if classification == "PASS"
            else "UNEXPECTED"
        )

    if expected_behavior == "NO_CRASH":
        return (
            "EXPECTED"
            if classification == "PASS"
            else "UNEXPECTED"
        )

    if expected_behavior == "RETURN_NAN":
        return (
            "EXPECTED"
            if classification == "EXPECTED_UNDEFINED"
            else "UNEXPECTED"
        )

    if expected_behavior == "RETURN_ZERO_OR_NAN":
        return (
            "EXPECTED"
            if classification in {
                "EXPECTED_UNDEFINED",
                "PASS"
            }
            else "UNEXPECTED"
        )

    if expected_behavior == "SEMANTIC_REVIEW":
        return (
            "EXPECTED"
            if classification == "SEMANTIC_WARNING"
            else "UNEXPECTED"
        )

    if expected_behavior == "FAIL_GRACEFULLY":
        return "REVIEW"

    return "REVIEW"

def run_test(
    test_id,
    description,
    financials,
    test_function,
    expected_behavior,
):
    """
    Execute one edge-case test and classify the result.
    """

    print("\n" + "=" * 70)
    print(f"TEST: {test_id}")
    print(f"DESCRIPTION: {description}")
    print(f"EXPECTED: {expected_behavior}")

    try:

        analyzer = FinancialAnalyzer(financials)

        result = test_function(analyzer)

        classification = classify_result(
            result=result,
            expected_behavior=expected_behavior,
            error=None
        )   

        test_outcome = determine_test_outcome(
            expected_behavior=expected_behavior,
            classification=classification,
            error=None
        )

        print(f"CLASSIFICATION: {classification}")
        print(f"TEST OUTCOME: {test_outcome}")
        print(f"RESULT: {result}")

        return {
            "id": test_id,
            "description": description,
            "expected_behavior": expected_behavior,
            "classification": classification,
            "test_outcome": test_outcome,
            "result": str(result),
            "error": None,
        }

    except Exception as e:

        error_message = str(e)

        classification = "DATA_HANDLING_FAILURE"

        if expected_behavior == "FAIL_GRACEFULLY":
            test_outcome = "EXPECTED"
        else:
            test_outcome = "UNEXPECTED"

        print(
            f"CLASSIFICATION: {classification}"
        )
        print(
            f"TEST OUTCOME: {test_outcome}"
        )
        print(
            f"ERROR: {error_message}"
        )

        return {
            "id": test_id,
            "description": description,
            "expected_behavior": expected_behavior,
            "classification": classification,
            "test_outcome": test_outcome,
            "result": None,
            "error": error_message,
        }


def evaluate():

    results = []

    # ---------------------------------------------------------
    # E001 - Missing revenue metric
    # ---------------------------------------------------------

    financials = pd.DataFrame({
        "fiscal_year": [2023, 2024, 2025],
        "net_income": [10, 12, 15],
        "assets": [100, 110, 120],
        "liabilities": [50, 55, 60],
        "cash": [20, 22, 25],
        "operating_cash_flow": [12, 14, 17],
    })

    results.append(
        run_test(
            "E001",
            "Revenue metric completely unavailable",
            financials,
            lambda analyzer: analyzer.revenue_growth(),
            "FAIL_GRACEFULLY"
        )
    )

    # ---------------------------------------------------------
    # E002 - Missing net income metric
    # ---------------------------------------------------------

    financials = pd.DataFrame({
        "fiscal_year": [2023, 2024, 2025],
        "revenue": [100, 110, 120],
        "assets": [100, 110, 120],
        "liabilities": [50, 55, 60],
        "cash": [20, 22, 25],
        "operating_cash_flow": [12, 14, 17],
    })

    results.append(
        run_test(
            "E002",
            "Net income metric completely unavailable",
            financials,
            lambda analyzer: analyzer.net_profit_margin(),
            "FAIL_GRACEFULLY"
        )
    )

    # ---------------------------------------------------------
    # E003 - NaN revenue
    # ---------------------------------------------------------

    financials = pd.DataFrame({
        "fiscal_year": [2023, 2024, 2025],
        "revenue": [100, np.nan, 120],
        "net_income": [10, 12, 15],
        "assets": [100, 110, 120],
        "liabilities": [50, 55, 60],
        "cash": [20, 22, 25],
        "operating_cash_flow": [12, 14, 17],
    })

    results.append(
        run_test(
            "E003",
            "Revenue contains missing values",
            financials,
            lambda analyzer: analyzer.revenue_growth(),
            "VALID_RESULT"
        )
    )

    # ---------------------------------------------------------
    # E004 - NaN net income
    # ---------------------------------------------------------

    financials = pd.DataFrame({
        "fiscal_year": [2023, 2024, 2025],
        "revenue": [100, 110, 120],
        "net_income": [10, np.nan, 15],
        "assets": [100, 110, 120],
        "liabilities": [50, 55, 60],
        "cash": [20, 22, 25],
        "operating_cash_flow": [12, 14, 17],
    })

    results.append(
        run_test(
            "E004",
            "Net income contains missing values",
            financials,
            lambda analyzer: analyzer.net_profit_margin(),
            "VALID_RESULT"
        )
    )

    # ---------------------------------------------------------
    # E005 - Negative net income
    # ---------------------------------------------------------

    financials = pd.DataFrame({
        "fiscal_year": [2023, 2024, 2025],
        "revenue": [100, 110, 120],
        "net_income": [-10, -5, 8],
        "assets": [100, 110, 120],
        "liabilities": [50, 55, 60],
        "cash": [20, 22, 25],
        "operating_cash_flow": [12, 14, 17],
    })

    results.append(
        run_test(
            "E005",
            "Company has negative net income",
            financials,
            lambda analyzer: analyzer.net_profit_margin(),
            "VALID_RESULT"
        )
    )

    # ---------------------------------------------------------
    # E006 - Insufficient revenue data for CAGR
    # ---------------------------------------------------------

    financials = pd.DataFrame({
        "fiscal_year": [2025],
        "revenue": [120],
    })

    results.append(
        run_test(
            "E006",
            "Only one year of revenue available for CAGR",
            financials,
            lambda analyzer: analyzer.revenue_cagr(),
            "RETURN_NAN"
        )
    )

    # ---------------------------------------------------------
    # E007 - Insufficient net income data for CAGR
    # ---------------------------------------------------------

    financials = pd.DataFrame({
        "fiscal_year": [2025],
        "net_income": [10],
    })

    results.append(
        run_test(
            "E007",
            "Only one year of net income available for CAGR",
            financials,
            lambda analyzer: analyzer.net_income_cagr(),
            "RETURN_NAN"
        )
    )

    # ---------------------------------------------------------
    # E008 - Zero revenue / profit margin
    # ---------------------------------------------------------

    financials = pd.DataFrame({
        "fiscal_year": [2024, 2025],
        "revenue": [100, 0],
        "net_income": [10, 5],
    })

    results.append(
        run_test(
            "E008",
            "Revenue is zero when calculating profit margin",
            financials,
            lambda analyzer: analyzer.net_profit_margin(),
            "NO_CRASH"
        )
    )

    # ---------------------------------------------------------
    # E009 - Zero revenue / operating cash flow margin
    # ---------------------------------------------------------

    financials = pd.DataFrame({
        "fiscal_year": [2024, 2025],
        "revenue": [100, 0],
        "operating_cash_flow": [10, 5],
    })

    results.append(
        run_test(
            "E009",
            "Revenue is zero when calculating operating cash flow margin",
            financials,
            lambda analyzer: analyzer.operating_cash_flow_margin(),
            "NO_CRASH"
        )
    )

    # ---------------------------------------------------------
    # E010 - Zero assets
    # ---------------------------------------------------------

    financials = pd.DataFrame({
        "fiscal_year": [2024, 2025],
        "assets": [100, 0],
        "liabilities": [50, 20],
    })

    results.append(
        run_test(
            "E010",
            "Assets are zero when calculating liability to asset ratio",
            financials,
            lambda analyzer: analyzer.liability_to_asset_ratio(),
            "NO_CRASH"
        )
    )

    # ---------------------------------------------------------
    # E011 - Missing years
    # ---------------------------------------------------------

    financials = pd.DataFrame({
        "fiscal_year": [2021, 2023, 2025],
        "revenue": [100, 120, 150],
        "net_income": [10, 15, 20],
        "assets": [100, 120, 150],
        "liabilities": [50, 60, 70],
        "cash": [20, 25, 30],
        "operating_cash_flow": [12, 18, 22],
    })

    results.append(
        run_test(
            "E011",
            "Fiscal years contain gaps",
            financials,
            lambda analyzer: analyzer.revenue_growth(),
            "SEMANTIC_REVIEW"
        )
    )

    # ---------------------------------------------------------
    # E012 - Incomplete records
    # ---------------------------------------------------------

    financials = pd.DataFrame({
        "fiscal_year": [2023, 2024, 2025],
        "revenue": [100, 110, 120],
        "net_income": [10, np.nan, 15],
        "assets": [100, 110, np.nan],
        "liabilities": [50, np.nan, 60],
        "cash": [20, 22, 25],
        "operating_cash_flow": [12, np.nan, 17],
    })

    results.append(
        run_test(
            "E012",
            "Different financial metrics have different available years",
            financials,
            lambda analyzer: analyzer.trend_summary(),
            "SEMANTIC_REVIEW"
        )
    )

    # ---------------------------------------------------------
    # E013 - Empty dataset
    # ---------------------------------------------------------

    financials = pd.DataFrame(
        columns=[
            "fiscal_year",
            "revenue",
            "net_income",
            "assets",
            "liabilities",
            "cash",
            "operating_cash_flow",
        ]
    )

    results.append(
        run_test(
            "E013",
            "No financial records available",
            financials,
            lambda analyzer: analyzer.trend_summary(),
            "FAIL_GRACEFULLY"
        )
    )

    # ---------------------------------------------------------
    # E014 - Extreme revenue increase
    # ---------------------------------------------------------

    financials = pd.DataFrame({
        "fiscal_year": [2024, 2025],
        "revenue": [1, 1_000_000],
    })

    results.append(
        run_test(
            "E014",
            "Revenue experiences an extreme increase",
            financials,
            lambda analyzer: analyzer.revenue_growth(),
            "VALID_RESULT"
        )
    )

    # ---------------------------------------------------------
    # E015 - Extreme revenue decline
    # ---------------------------------------------------------

    financials = pd.DataFrame({
        "fiscal_year": [2024, 2025],
        "revenue": [1_000_000, 1],
    })

    results.append(
        run_test(
            "E015",
            "Revenue experiences an extreme decline",
            financials,
            lambda analyzer: analyzer.revenue_growth(),
            "VALID_RESULT"
        )
    )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    results_df = pd.DataFrame(results)

    classification_counts = (
        results_df["classification"]
        .value_counts()
        .to_dict()
    )

    outcome_counts = (
        results_df["test_outcome"]
        .value_counts()
        .to_dict()
    )

    print("\n")
    print("=" * 70)
    print("EDGE-CASE EVALUATION")
    print("=" * 70)

    print(f"Total tests: {len(results_df)}")

    print("\nClassification:")
    print(
        f"PASS: "
        f"{classification_counts.get('PASS', 0)}"
    )

    print(
        f"EXPECTED_UNDEFINED: "
        f"{classification_counts.get('EXPECTED_UNDEFINED', 0)}"
    )

    print(
        f"NUMERICAL_FAILURE: "
        f"{classification_counts.get('NUMERICAL_FAILURE', 0)}"
    )

    print(
        f"SEMANTIC_WARNING: "
        f"{classification_counts.get('SEMANTIC_WARNING', 0)}"
    )

    print(
        f"DATA_HANDLING_FAILURE: "
        f"{classification_counts.get('DATA_HANDLING_FAILURE', 0)}"
    )

    print("\nTest outcome:")

    print(
        f"EXPECTED: "
        f"{outcome_counts.get('EXPECTED', 0)}"
    )

    print(
        f"REVIEW: "
        f"{outcome_counts.get('REVIEW', 0)}"
    )

    print(
        f"UNEXPECTED: "
        f"{outcome_counts.get('UNEXPECTED', 0)}"
    )

    # ---------------------------------------------------------
    # Detailed results
    # ---------------------------------------------------------

    print("\nDetailed classification:")

    for _, row in results_df.iterrows():

        print(
            f"{row['id']}: "
            f"{row['classification']} "
            f"({row['test_outcome']})"
        )

    # ---------------------------------------------------------
    # Save results
    # ---------------------------------------------------------

    output_file = "data/evaluation/edge_case_results.csv"

    results_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nResults saved to: {output_file}"
    )


if __name__ == "__main__":
    evaluate()