import pandas as pd

from src.application.financial_assistant import FinancialAssistant


def evaluate():

    df = pd.read_csv(
        "data/evaluation/end_to_end_questions.csv"
    )

    print(f"Loaded {len(df)} questions")

    assistant = FinancialAssistant()

    print("FinancialAssistant created")

    results = []

    for _, row in df.iterrows():

        question = row["question"]

        print("\n" + "=" * 70)
        print(f"Question: {question}")

        try:

            result = assistant.ask(question)

            predicted_company = result["company"]
            predicted_tool = result["tool"]
            answer = result["answer"]
            answer_valid = result["answer_valid"]

            company_correct = (
                predicted_company.lower()
                == row["expected_company"].lower()
            )

            tool_correct = (
                predicted_tool
                == row["expected_tool"]
            )

            results.append(
                {
                    "question": question,
                    "expected_company":row["expected_company"],
                    "predicted_company":predicted_company,
                    "company_correct":company_correct,
                    "expected_tool":row["expected_tool"],
                    "predicted_tool":predicted_tool,
                    "tool_correct":tool_correct,
                    "answer":answer,
                    "answer_valid": answer_valid,
                }
            )

            print(f"Company: {predicted_company}")
            print(f"Tool: {predicted_tool}")
            print(f"Answer: {answer}")

        except Exception as e:

            print(f"ERROR: {e}")

            results.append(
                {
                    "question": question,
                    "expected_company":row["expected_company"],
                    "predicted_company": None,
                    "company_correct": False,
                    "expected_tool":row["expected_tool"],
                    "predicted_tool": None,
                    "tool_correct": False,
                    "answer": None,
                    "answer_valid": False,
                }
            )

    results_df = pd.DataFrame(results)
    
    answers_generated = (
        results_df["answer"].notna().mean() * 100
    )

    final_validation_rate = (
        results_df["answer_valid"].fillna(False).mean() * 100
    )
    
    validation_failures = (
        ~results_df["answer_valid"].fillna(False)
    ).sum()

    company_accuracy = (
        results_df["company_correct"].mean() * 100
    )

    tool_accuracy = (
        results_df["tool_correct"].mean() * 100
    )

    end_to_end_success = (
        (
            results_df["company_correct"]
            & results_df["tool_correct"]
            & results_df["answer_valid"].fillna(False)
        ).mean()
        * 100
    )

    print("\n")
    print("=" * 70)
    print("END-TO-END FINANCIAL ASSISTANT EVALUATION")
    print("=" * 70)

    print(
        f"Total questions: "
        f"{len(results_df)}"
    )

    print(
        f"Company accuracy: "
        f"{company_accuracy:.2f}%"
    )

    print(
        f"Tool routing accuracy: "
        f"{tool_accuracy:.2f}%"
    )

    print(
        f"End-to-end success: "
        f"{end_to_end_success:.2f}%"
    )
    
    print(
        f"Answers generated: "
        f"{answers_generated:.2f}%"
    )
    
    print(
        f"Final answer validation: "
        f"{final_validation_rate:.2f}%"
    )
    
    print(
        f"Validation failures: "
        f"{validation_failures}"
    )

    output_file = (
        "data/evaluation/"
        "end_to_end_results.csv"
    )

    results_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nResults saved to: {output_file}"
    )


if __name__ == "__main__":
    evaluate()