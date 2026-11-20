
from pathlib import Path
import chromadb

from embeddings import generate_embeddings

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "chroma_db"

# Map question topics to their source documents
DOCUMENT_KEYWORDS = {
    "Claims User Manual.docx": [
        "claim", "claims", "reimbursement"
    ],
    "Timecard User Manual.docx": [
        "timecard", "timesheet", "time sheet"
    ],
    "Regularisiation User Manual.docx": [
        "regularization", "regularisation",
        "regularize", "regularise",
        "missed swipe", "biometric",
        "work from home", "wfh", "forgot id",
        "on-site", "onsite"
    ],
    "5_day_work_week_policy.txt": [
        "five day", "5 day", "5-day",
        "work week", "payroll cutoff",
        "payroll cut-off", "lop",
        "loss of pay", "salary deduction",
        "deduction", "leave", "attendance",
        "working days"
    ]
}


def retrieve_documents(question):

    client = chromadb.PersistentClient(path=str(DB_PATH))
    collection = client.get_collection(name="hr_policy")

    question_embedding = generate_embeddings([question])
    question_lower = question.lower()

    # Identify all relevant documents
    selected_sources = []

    for source, keywords in DOCUMENT_KEYWORDS.items():

        if any(keyword in question_lower for keyword in keywords):
            selected_sources.append(source)

    # Retrieve information from all selected documents
    if selected_sources:

        all_documents = []
        all_metadatas = []
        all_distances = []

        for source in selected_sources:

            results = collection.query(
                query_embeddings=question_embedding.tolist(),
                n_results=5,
                where={"source": source}
            )

            all_documents.extend(results["documents"][0])
            all_metadatas.extend(results["metadatas"][0])
            all_distances.extend(results["distances"][0])

        return {
            "documents": [all_documents],
            "metadatas": [all_metadatas],
            "distances": [all_distances]
        }

    else:

        # General retrieval when no topic is identified
        return collection.query(
            query_embeddings=question_embedding.tolist(),
            n_results=5
        )


if __name__ == "__main__":

    question = input("Ask an HR question: ")
    results = retrieve_documents(question)

    print("\nRelevant information found:")

    for i, document in enumerate(results["documents"][0]):

        source = results["metadatas"][0][i]["source"]

        print("\n" + "=" * 50)
        print("Source:", source)
        print("Retrieved text:")
        print(document)
