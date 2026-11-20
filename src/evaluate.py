
import json
from pathlib import Path

from chatbot import generate_answer

BASE_DIR = Path(__file__).resolve().parent.parent
EVALUATION_FILE = BASE_DIR / "evaluation" / "evaluation_set.json"


def evaluate_chatbot():

    with open(EVALUATION_FILE, "r", encoding="utf-8") as file:
        test_questions = json.load(file)

    correct_count = 0
    total_questions = len(test_questions)

    print("\nBCT HR Chatbot Evaluation")
    print("=" * 50)

    for index, test in enumerate(test_questions, start=1):

        question = test["question"]
        expected_keywords = test["expected_keywords"]

        print(f"\nQuestion {index}: {question}")

        answer = generate_answer(question)

        print("Chatbot Answer:", answer)

        # Check whether all expected keywords are present
        answer_lower = answer.lower()

        is_correct = all(
            keyword.lower() in answer_lower
            for keyword in expected_keywords
        )

        if is_correct:
            correct_count += 1
            print("Result: PASS")
        else:
            print("Result: FAIL")
            print("Expected keywords:", expected_keywords)

    accuracy = (correct_count / total_questions) * 100

    print("\n" + "=" * 50)
    print("EVALUATION SUMMARY")
    print("Total Questions:", total_questions)
    print("Correct Answers:", correct_count)
    print("Incorrect Answers:", total_questions - correct_count)
    print("Accuracy:", round(accuracy, 2), "%")


if __name__ == "__main__":
    evaluate_chatbot()
