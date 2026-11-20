
import ollama
import json
import re
from pathlib import Path
from datetime import datetime

from retrieve import retrieve_documents

MODEL_NAME = "llama3.2:3b"

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "logs" / "chatbot_logs.jsonl"


def generate_answer(question):

    # Step 1: Retrieve relevant documents
    results = retrieve_documents(question)

    retrieved_chunks = results["documents"][0]
    metadata = results["metadatas"][0]

    context = "\n\n".join(retrieved_chunks)

    print("\nDEBUG - Retrieved Context:")
    print(context)

    # Step 2: Prepare question and context
    answer = None
    question_lower = question.lower()
    context_lower = context.lower()

    # Rule 1: Future date regularization
    regularization_question = any(
        word in question_lower
        for word in ["regulariz", "attendance", "regularis"]
    )

    future_date_question = any(
        word in question_lower
        for word in ["future", "tomorrow", "next day", "upcoming"]
    )

    if regularization_question and future_date_question:
        if "future dates are not permitted" in context_lower:
            answer = (
                "No, employees cannot regularize attendance "
                "for future dates. Only past and current dates "
                "are permitted."
            )

    # Rule 2: Daily attendance shortage
    if answer is None and (
        "shortage" in question_lower
        and any(word in question_lower for word in ["daily", "per day"])
    ):
        if "less than 2 hours" in context_lower:
            answer = (
                "Attendance regularization is applicable only "
                "when the daily shortage is less than 2 hours."
            )

    # Rule 3: Payroll cutoff date
    if answer is None and "payroll" in question_lower and (
        "cutoff" in question_lower or "cut-off" in question_lower
    ):
        match = re.search(
            r"payroll\s+cut[- ]?off\s+date\s+(?:would be|is)\s+(.+?)(?:\s+and\b|[.!?\n]|$)",
            context,
            re.IGNORECASE
        )

        if match:
            answer = (
                f"The monthly payroll cutoff date is "
                f"{match.group(1).strip()}."
            )

    # Rule 4: Missed both IN and OUT swipes
    if answer is None and (
        "missed both" in question_lower
        or (
            "in" in question_lower
            and "out" in question_lower
            and "swipe" in question_lower
        )
    ):
        if (
            "either in-time or out-time" in context_lower
            or "either in time or out time" in context_lower
        ):
            answer = (
                "The Missed to Swipe request is applicable when "
                "either the IN swipe or the OUT swipe is recorded, "
                "but not both."
            )

    # Rule 5: Timecard access not available
    if answer is None and "timecard" in question_lower and any(
        word in question_lower for word in ["cannot see", "can't see", "missing", "not visible"]
    ):
        if "ia team" in context_lower:
            answer = (
                "If you cannot see the Timecard option in Oracle EBS, "
                "contact the IA team to enable the required flag."
            )

    # Rule 6: Timecard task missing
    if answer is None and "timecard" in question_lower and "task" in question_lower:
        if "rmg team" in context_lower:
            answer = (
                "If the required task is missing from the Timecard dropdown, "
                "contact the RMG team to have the task included."
            )

    # Rule 7: Maximum normal Timecard hours
    if answer is None and "timecard" in question_lower and any(
        word in question_lower for word in ["maximum", "max", "normal working hours"]
    ):
        if "india" in context_lower and "8 hours" in context_lower:
            answer = (
                "For India-based associates, normal working hours "
                "must not exceed 9 hours. For associates in other "
                "locations, the limit is 8 hours."
            )

    # Rule 8: Timecard prerequisites
    if answer is None and "timecard" in question_lower and any(
        word in question_lower for word in ["before", "prerequisite", "required", "submit"]
    ):
        if (
            "regularization" in context_lower
            and "biometric" in context_lower
        ):
            answer = (
                "Before entering a Timecard, biometric attendance "
                "or regularization details must be available."
            )

    # Rule 9: LOP meaning
    if answer is None and (
        any(word in question_lower for word in ["lop", "loss of pay", "leave of absence"])
        or (
            "attendance" in question_lower
            and any(word in question_lower for word in ["regularize", "regularise"])
            and "leave" in question_lower
        )
    ):
        if "treated as lop" in context_lower and "deductions" in context_lower:
            answer = (
                "If attendance is not regularized and leave is not applied, "
                "those days will be treated as LOP (Loss of Pay), "
                "and salary deductions will be made accordingly."
            )

       # Rule 10: Regularization biometric requirements
    if answer is None and (
        "regulariz" in question_lower
        and any(word in question_lower for word in [
            "biometric", "worked", "hours"
        ])
    ):
        if (
            "less than 9 hours" in context_lower
            and "greater than 7 hours" in context_lower
        ):
            answer = (
    "To apply for attendance regularization, "
    "biometric attendance must be greater than 7 hours "
    "and less than 9 hours. The request must be submitted "
    "within 15 days."
)

    # Rule 11: Work From Home eligibility
    if answer is None and (
        "work from home" in question_lower or "wfh" in question_lower
    ):
        if (
            "not be eligible" in context_lower
            and "biometric attendance" in context_lower
        ):
            answer = (
                "Employees can apply for Work From Home when "
                "biometric attendance is not available. If biometric "
                "attendance is available, they are not eligible "
                "for this request."
            )
                # Rule 11B: Claim prerequisites
    if answer is None and (
        "claim" in question_lower
        and any(word in question_lower for word in [
            "document", "proof", "details", "before"
        ])
    ):
        if "claim details" in context_lower and "proof" in context_lower:
            answer = (
                "Before submitting a claim, ensure you are eligible "
                "according to the claim policy. Keep the necessary "
                "claim details and supporting proof ready. "
                "Project-related claims must be submitted against "
                "a project to which you are mapped or allocated."
            )

        # Rule 12: How to submit a claim
    if answer is None and (
        "claim" in question_lower
        and any(word in question_lower for word in ["submit", "apply", "process"])
    ):
        if "claim" in context_lower and "oracle" in context_lower:
            answer = (
                "To submit a claim in Oracle EBS:\n"
                "1. Check your eligibility according to the claim policy "
                "or contact your BU HR.\n"
                "2. Navigate to BCT Employee Claim Search.\n"
                "3. Click Create and select the appropriate claim type.\n"
                "4. Click Add New Row and enter the required claim details.\n"
                "5. Click Save.\n"
                "6. Review the confirmation dialogue and click OK.\n"
                "7. Submit the claim for approval.\n"
                "8. Check the Dashboard to view the claim status and approval details."
            )

    # Step 3: Use the LLM if no direct rule matched
    if answer is None:

        response = ollama.chat(
            model=MODEL_NAME,
            options={"temperature": 0},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a BCT HR Policy Assistant. "
                        "Answer only using the provided HR context. "
                        "Answer only the employee's actual question. "
                        "Do not mix information from different processes. "
                        "Do not add unrelated instructions or steps. "
                        "Do not invent information or assumptions. "
                        "If the answer is unavailable, respond exactly: "
                        "This information is not mentioned in the HR policy."
                    )
                },
                {
                    "role": "user",
                    "content": f"""
HR Context:
{context}

Employee Question:
{question}

Give a clear, simple and relevant answer.
"""
                }
            ]
        )

        answer = response["message"]["content"]

    # Step 4: Save conversation details
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "retrieved_documents": [
            {
                "source": metadata[i]["source"],
                "text": retrieved_chunks[i]
            }
            for i in range(len(retrieved_chunks))
        ],
        "answer": answer
    }

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    return answer


# Step 5: Run chatbot
if __name__ == "__main__":

    print("Welcome to BCT HR Chatbot!")
    print("Type 'exit' to stop the chatbot.")

    while True:

        question = input("\nAsk your HR question: ")

        if question.lower() == "exit":
            print("Thank you for using BCT HR Chatbot!")
            break

        answer = generate_answer(question)

        print("\nChatbot Answer:")
        print(answer)
