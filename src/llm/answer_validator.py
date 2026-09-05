import pandas as pd
import numpy as np
import re

class AnswerValidator:
    """
    Validates whether an LLM-generated answer
    is consistent with the underlying financial data.
    """

    def validate(self, tool_name, result, answer):

        if not answer or not isinstance(answer, str):
            return False

        if tool_name == "get_profit_margin":
            return self._validate_profit_margin(result, answer)

        if tool_name == "get_revenue_growth":
            return self._validate_revenue_growth(result, answer)

        if tool_name == "get_asset_growth":
            return self._validate_asset_growth(result, answer)

        return True
    
    def _extract_percentages(self, answer):
        """
        Extract percentage values mentioned in an answer.
        """

        matches = re.findall(
            r"(-?\d+(?:\.\d+)?)\s*%",
            answer
        )

        return [
            float(value)
            for value in matches
        ]
        
    def _validate_year_value_pairs(
        self,
        result,
        answer,
        value_column
    ):
        """
        Validate explicit year/value pairs mentioned in the answer.
        """

        if "fiscal_year" not in result.columns:
            return True

        if value_column not in result.columns:
            return True

        actual = result[
            ["fiscal_year", value_column]
        ].dropna()

        tolerance = 0.05

        # Find expressions such as:
        # "21.09% in 2017"
        # "26.92% in 2025"
        pattern = (
            r"(-?\d+(?:\.\d+)?)\s*%\s+in\s+(20\d{2})"
        )

        matches = re.findall(
            pattern,
            answer,
            flags=re.IGNORECASE
        )

        if not matches:
            return True

        for value, year in matches:

            value = float(value)
            year = int(year)

            matching_year = actual[
                actual["fiscal_year"] == year
            ]

            if matching_year.empty:
                return False

            actual_value = float(
                matching_year.iloc[0][value_column]
            )

            if abs(value - actual_value) > tolerance:
                return False

        return True
    
    def _validate_profit_margin(self, result, answer):

        if not isinstance(result, pd.DataFrame):
            return True

        if "net_profit_margin_pct" not in result.columns:
            return True

        margins = (
            result["net_profit_margin_pct"]
            .dropna()
        )

        if len(margins) < 2:
            return True

        answer_lower = answer.lower()

        # 1. Validate consistency claims

        increasing = all(
            margins.iloc[i] >= margins.iloc[i - 1]
            for i in range(1, len(margins))
        )

        consistency_phrases = [
            "consistently increasing",
            "consistently increased",
            "consistently improves",
            "consistently improved",
            "steadily increasing",
            "steadily increased",
            "steadily improves",
            "steadily improved",
        ]

        claims_consistent_improvement = any(
            phrase in answer_lower
            for phrase in consistency_phrases
        )

        if claims_consistent_improvement and not increasing:
            return False

        # 2. Validate numerical percentage claims
        mentioned_percentages = self._extract_percentages(answer)

        actual_values = margins.tolist()

        tolerance = 0.05

        for value in mentioned_percentages:

            matches_actual_value = any(
                abs(value - actual) <= tolerance
                for actual in actual_values
            )

            if not matches_actual_value:
                return False

        return self._validate_year_value_pairs(
            result,
            answer,
            "net_profit_margin_pct"
        )
        
    def _validate_revenue_growth(self, result, answer):
        # Validate revenue growth claims against the underlying data.

        if not isinstance(result, pd.DataFrame):
            return True

        if "revenue_growth_pct" not in result.columns:
            return True

        growth = (
            result["revenue_growth_pct"]
            .dropna()
        )

        if len(growth) == 0:
            return True

        answer_lower = answer.lower()

        # ---------------------------------------------------------
        # 1. Validate claims of consistent growth
        # ---------------------------------------------------------

        has_positive = (growth > 0).any()
        has_negative = (growth < 0).any()

        consistency_phrases = [
            "consistently increased",
            "consistently grew",
            "consistently growing",
            "steadily increased",
            "steadily grew",
            "steadily growing",
            "increased every year",
            "grew every year",
            "grew consistently",
        ]

        claims_consistent_growth = any(
            phrase in answer_lower
            for phrase in consistency_phrases
        )

        if claims_consistent_growth:
            if has_positive and has_negative:
                return False

        # ---------------------------------------------------------
        # 2. Validate numerical percentage claims
        # ---------------------------------------------------------

        mentioned_percentages = self._extract_percentages(answer)

        actual_values = growth.tolist()

        tolerance = 0.05

        for value in mentioned_percentages:

            matches_actual_value = any(
                abs(value - actual) <= tolerance
                for actual in actual_values
            )

            if not matches_actual_value:
                return False

        # ---------------------------------------------------------
        # 3. Validate explicit year/value pairs
        # ---------------------------------------------------------

        return self._validate_year_value_pairs(
            result,
            answer,
            "revenue_growth_pct"
        )


    def _validate_asset_growth(self, result, answer):
        """
        Validate asset growth claims against the underlying data.
        """

        if not isinstance(result, pd.DataFrame):
            return True

        if "asset_growth_pct" not in result.columns:
            return True

        growth = (
            result["asset_growth_pct"]
            .dropna()
        )

        if len(growth) == 0:
            return True

        answer_lower = answer.lower()

        # ---------------------------------------------------------
        # 1. Validate claims of consistent growth
        # ---------------------------------------------------------

        has_positive = (growth > 0).any()
        has_negative = (growth < 0).any()

        consistency_phrases = [
            "consistently increased",
            "consistently grew",
            "consistently growing",
            "steadily increased",
            "steadily grew",
            "steadily growing",
            "increased every year",
            "grew every year",
            "grew consistently",
        ]

        claims_consistent_growth = any(
            phrase in answer_lower
            for phrase in consistency_phrases
        )

        if claims_consistent_growth:
            if has_positive and has_negative:
                return False

        # ---------------------------------------------------------
        # 2. Validate numerical percentage claims
        # ---------------------------------------------------------

        mentioned_percentages = self._extract_percentages(answer)

        actual_values = growth.tolist()

        tolerance = 0.05

        for value in mentioned_percentages:

            matches_actual_value = any(
                abs(value - actual) <= tolerance
                for actual in actual_values
            )

            if not matches_actual_value:
                return False

        # ---------------------------------------------------------
        # 3. Validate explicit year/value pairs
        # ---------------------------------------------------------

        return self._validate_year_value_pairs(
            result,
            answer,
            "asset_growth_pct"
        )