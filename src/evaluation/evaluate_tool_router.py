import pandas as pd

from src.tools.tool_router import route_question


def evaluate():

    df = pd.read_csv(
        "data/evaluation/tool_routing_eval.csv"
    )

    predictions = []

    for i, question in enumerate(df["question"], start=1):

        print(f"Processing question {i}/50...")

        predicted_tool = route_question(question)

        predictions.append(predicted_tool)

    df["predicted_tool"] = predictions

    df["correct"] = (
        df["expected_tool"]
        == df["predicted_tool"]
    )

    accuracy = df["correct"].mean() * 100

    print("\nTool Routing Evaluation")
    print("=" * 50)

    print(f"Total questions: {len(df)}")
    print(f"Correct: {df['correct'].sum()}")
    print(
        f"Incorrect: {(~df['correct']).sum()}"
    )
    print(
        f"Accuracy: {accuracy:.2f}%"
    )

    print("\nAccuracy by tool")
    print("=" * 50)

    tool_accuracy = (
        df.groupby("expected_tool")["correct"]
        .mean()
        .mul(100)
        .round(2)
    )

    print(tool_accuracy)
    print("\nIncorrect predictions")
    print("=" * 50)

    incorrect = df[
        df["correct"] == False
    ]

    print(
        incorrect[
            [
                "question",
                "expected_tool",
                "predicted_tool",
            ]
        ].to_string(index=False)
    )

    df.to_csv(
        "data/evaluation/"
        "tool_routing_50_results.csv",
        index=False
    )

    print(
        "\nResults saved to:"
        " data/evaluation/"
        "tool_routing_50_results.csv"
    )


if __name__ == "__main__":
    evaluate()