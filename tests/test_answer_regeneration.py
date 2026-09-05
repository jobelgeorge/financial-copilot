from unittest.mock import patch

from src.application.financial_assistant import FinancialAssistant


def test_regenerates_invalid_profit_margin_answer():

    bad_answer = (
        "Apple's profitability has consistently increased."
    )

    good_answer = (
        "Apple's profitability fluctuated over the period, "
        "with the net profit margin moving between increases "
        "and decreases."
    )

    with patch(
        "src.application.financial_assistant.AnswerGenerator.generate",
        side_effect=[
            bad_answer,
            good_answer
        ]
    ):

        assistant = FinancialAssistant()

        result = assistant.ask(
            "Is Apple's profitability improving?"
        )

    assert result["answer"] == good_answer
    assert result["answer_valid"] is True