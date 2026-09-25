import pandas as pd

from src.application.financial_assistant import FinancialAssistant


def evaluate():

    df = pd.read_csv(
        "data/evaluation/robustness_questions.csv"
    )

    print(f"Loaded {len(df)} robustness questions")

    assistant = FinancialAssistant()

    print("FinancialAssistant created")

    results = []

    for _, row in df.iterrows():

        question = row["question"]
        category = row["category"]
        expected_company = row["expected_company"]
        expected_tool = row["expected_tool"]
        expected_behavior = row["expected_behavior"]

        print("\n" + "=" * 70)
        print(f"ID: {row['id']}")
        print(f"Category: {category}")
        print(f"Question: {question}")

        try:

            result = assistant.ask(question)

            predicted_company = result.get(
                "company"
            )

            predicted_tool = result.get(
                "tool"
            )

            answer = result.get(
                "answer"
            )

            answer_valid = result.get(
                "answer_valid",
                False
            )

            # -------------------------------------------------
            # Company evaluation
            # -------------------------------------------------

            if pd.isna(expected_company):
                company_correct = None

            elif predicted_company is None:
                company_correct = False

            else:
                company_correct = (
                    predicted_company.lower()
                    == str(expected_company).lower()
                )

            # -------------------------------------------------
            # Tool evaluation
            # -------------------------------------------------

            if pd.isna(expected_tool):
                tool_correct = None

            elif predicted_tool is None:
                tool_correct = False

            else:
                tool_correct = (
                    predicted_tool
                    == str(expected_tool)
                )

            # -------------------------------------------------
            # Behavior evaluation
            # -------------------------------------------------

            if expected_behavior == "ROUTE":

                behavior_correct = (
                    company_correct is True
                    and tool_correct is True
                    and answer_valid is True
                )

            else:

                # For AMBIGUOUS and UNSUPPORTED cases,
                # we record the actual system behavior.
                #
                # These cases will be analyzed separately
                # because the current FinancialAssistant
                # may not explicitly support these behaviors.

                behavior_correct = None

            results.append(
                {
                    "id": row["id"],
                    "category": category,
                    "question": question,
                    "expected_company": expected_company,
                    "predicted_company": predicted_company,
                    "company_correct": company_correct,
                    "expected_tool": expected_tool,
                    "predicted_tool": predicted_tool,
                    "tool_correct": tool_correct,
                    "expected_behavior": expected_behavior,
                    "answer": answer,
                    "answer_valid": answer_valid,
                    "behavior_correct": behavior_correct,
                    "error": None,
                }
            )

            print(
                f"Company: {predicted_company}"
            )

            print(
                f"Tool: {predicted_tool}"
            )

            print(
                f"Answer valid: {answer_valid}"
            )

            print(
                f"Answer: {answer}"
            )

        except Exception as e:

            error_message = str(e)

            print(
                f"ERROR: {error_message}"
            )

            results.append(
                {
                    "id": row["id"],
                    "category": category,
                    "question": question,
                    "expected_company": expected_company,
                    "predicted_company": None,
                    "company_correct": False,
                    "expected_tool": expected_tool,
                    "predicted_tool": None,
                    "tool_correct": False,
                    "expected_behavior": expected_behavior,
                    "answer": None,
                    "answer_valid": False,
                    "behavior_correct": False,
                    "error": error_message,
                }
            )

    results_df = pd.DataFrame(results)

    # ---------------------------------------------------------
    # Metrics for ROUTE questions
    # ---------------------------------------------------------

    route_results = results_df[
        results_df["expected_behavior"] == "ROUTE"
    ]

    if len(route_results) > 0:

        company_accuracy = (
            route_results["company_correct"]
            .fillna(False)
            .mean()
            * 100
        )

        tool_accuracy = (
            route_results["tool_correct"]
            .fillna(False)
            .mean()
            * 100
        )

        routing_success = (
            (
                route_results["company_correct"].fillna(False)
                &
                route_results["tool_correct"].fillna(False)
                &
                route_results["answer_valid"].fillna(False)
            )
            .mean()
            * 100
        )

    else:

        company_accuracy = 0.0
        tool_accuracy = 0.0
        routing_success = 0.0

    # ---------------------------------------------------------
    # Category counts
    # ---------------------------------------------------------

    category_counts = (
        results_df["category"]
        .value_counts()
        .to_dict()
    )

    print("\n")
    print("=" * 70)
    print("ROBUSTNESS EVALUATION")
    print("=" * 70)

    print(
        f"Total questions: "
        f"{len(results_df)}"
    )

    print(
        f"Paraphrase questions: "
        f"{category_counts.get('PARAPHRASE', 0)}"
    )

    print(
        f"Company variation questions: "
        f"{category_counts.get('COMPANY_VARIATION', 0)}"
    )

    print(
        f"Ambiguous questions: "
        f"{category_counts.get('AMBIGUOUS', 0)}"
    )

    print(
        f"Unsupported questions: "
        f"{category_counts.get('UNSUPPORTED', 0)}"
    )

    print(
        f"\nCompany accuracy "
        f"(ROUTE questions): "
        f"{company_accuracy:.2f}%"
    )

    print(
        f"Tool routing accuracy "
        f"(ROUTE questions): "
        f"{tool_accuracy:.2f}%"
    )

    print(
        f"Routing success "
        f"(company + tool + validation): "
        f"{routing_success:.2f}%"
    )

    # ---------------------------------------------------------
    # Save results
    # ---------------------------------------------------------

    output_file = (
        "data/evaluation/"
        "robustness_results.csv"
    )

    results_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nResults saved to: "
        f"{output_file}"
    )


if __name__ == "__main__":
    evaluate()