
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(texts):
    # Convert text into numerical vectors
    embeddings = model.encode(texts)

    return embeddings


if __name__ == "__main__":

    sample_texts = [
        "Employees must complete 9 hours of work.",
        "Attendance should be regularized every working day."
    ]

    vectors = generate_embeddings(sample_texts)

    print("Number of texts:", len(sample_texts))
    print("Embedding dimensions:", vectors.shape[1])
    print("First embedding preview:", vectors[0][:5])
