import pandas as pd


class RootCauseAnalyzer:
    """
    Analyze evaluation failures and assign root causes.

    This class focuses on identifying the likely source
    of a failure rather than modifying the application.
    """

    def __init__(self, results: pd.DataFrame):
        self.results = results.copy()

    def classify_root_cause(self, row) -> str:

        failure_type = row.get(
            "failure_type",
            "UNKNOWN_ERROR"
        )

        # --------------------------------------------------
        # 1. Successful system execution
        # --------------------------------------------------

        if failure_type == "SUCCESS":
            return "SUCCESS"

        # --------------------------------------------------
        # 2. System/data failures
        # --------------------------------------------------

        if failure_type == "SYSTEM_ERROR":

            error = str(
                row.get("error", "")
            ).lower()

            if (
                "liabilities" in error
                or "assets" in error
                or "revenue" in error
                or "net_income" in error
            ):
                return "DATA_ERROR"

            return "SYSTEM_ERROR"

        # --------------------------------------------------
        # 3. Company identification
        # --------------------------------------------------

        if failure_type == "COMPANY_ERROR":
            return "ROUTING_ERROR"

        # --------------------------------------------------
        # 4. Tool routing
        # --------------------------------------------------

        if failure_type == "TOOL_ROUTING_ERROR":
            return "ROUTING_ERROR"

        # --------------------------------------------------
        # 5. Answer generation
        # --------------------------------------------------

        if failure_type == "ANSWER_GENERATION_ERROR":
            return "LLM_GENERATION_ERROR"

        # --------------------------------------------------
        # 6. Answer validation
        # --------------------------------------------------

        if failure_type == "ANSWER_VALIDATION_ERROR":
            return "VALIDATOR_ERROR"

        return "UNKNOWN_ERROR"

    def analyze(self) -> pd.DataFrame:

        analysis = self.results.copy()

        analysis["root_cause"] = analysis.apply(
            self.classify_root_cause,
            axis=1
        )

        return analysis

    def summary(self) -> dict:

        analysis = self.analyze()

        counts = (
            analysis["root_cause"]
            .value_counts()
            .to_dict()
        )

        return {
            "total_questions": len(analysis),
            "success": counts.get(
                "SUCCESS", 0
            ),
            "data_errors": counts.get(
                "DATA_ERROR", 0
            ),
            "routing_errors": counts.get(
                "ROUTING_ERROR", 0
            ),
            "llm_generation_errors": counts.get(
                "LLM_GENERATION_ERROR", 0
            ),
            "validator_errors": counts.get(
                "VALIDATOR_ERROR", 0
            ),
            "system_errors": counts.get(
                "SYSTEM_ERROR", 0
            ),
            "unknown_errors": counts.get(
                "UNKNOWN_ERROR", 0
            ),
        }