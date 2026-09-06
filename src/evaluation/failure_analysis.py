import pandas as pd


class FailureAnalyzer:
    """
    Analyze failures produced by the end-to-end evaluation.
    """

    def __init__(self, results: pd.DataFrame):
        self.results = results.copy()

    def classify_failure(self, row) -> str:

        # An exception occurred inside the application
        if (
            pd.notna(row.get("error"))
            and str(row.get("error")).strip()
        ):
            return "SYSTEM_ERROR"

        # Successful end-to-end result
        if (
            row["company_correct"]
            and row["tool_correct"]
            and row["answer_valid"]
        ):
            return "SUCCESS"

        # Company identification failure
        if not row["company_correct"]:
            return "COMPANY_ERROR"

        # Tool routing failure
        if not row["tool_correct"]:
            return "TOOL_ROUTING_ERROR"

        # Answer generation failure
        if pd.isna(row["answer"]) or not row["answer"]:
            return "ANSWER_GENERATION_ERROR"

        # Answer validation failure
        if not row["answer_valid"]:
            return "ANSWER_VALIDATION_ERROR"

        return "UNKNOWN_ERROR"
    
    def analyze(self) -> pd.DataFrame:

        analysis = self.results.copy()

        analysis["failure_type"] = analysis.apply(
            self.classify_failure,
            axis=1
        )

        return analysis

    def summary(self) -> dict:

        analysis = self.analyze()

        counts = (
            analysis["failure_type"]
            .value_counts()
            .to_dict()
        )

        total = len(analysis)

        return {
            "total_questions": total,
            "successful_questions": counts.get(
                "SUCCESS", 0
            ),
            "company_errors": counts.get(
                "COMPANY_ERROR", 0
            ),
            "tool_routing_errors": counts.get(
                "TOOL_ROUTING_ERROR", 0
            ),
            "answer_generation_errors": counts.get(
                "ANSWER_GENERATION_ERROR", 0
            ),
            "answer_validation_errors": counts.get(
                "ANSWER_VALIDATION_ERROR", 0
            ),
            "system_errors": counts.get(
                "SYSTEM_ERROR", 0
            ),
            "unknown_errors": counts.get(
                "UNKNOWN_ERROR", 0
            ),
        }