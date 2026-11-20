
from pathlib import Path
import chromadb

from chunk_documents import create_chunks
from extract_documents import extract_all_documents
from embeddings import generate_embeddings


# Find the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Store ChromaDB data locally
DB_PATH = BASE_DIR / "chroma_db"


def store_documents():

    # Step 1: Extract text from HR documents
    documents = extract_all_documents()

    # Step 2: Divide documents into chunks
    chunks = create_chunks(documents)

    # Step 3: Get text from every chunk
    texts = [chunk["text"] for chunk in chunks]

    # Step 4: Generate embeddings
    embeddings = generate_embeddings(texts)

    # Step 5: Connect to ChromaDB
    client = chromadb.PersistentClient(path=str(DB_PATH))

    # Step 6: Delete the old collection
    try:
        client.delete_collection(name="hr_policy")
        print("Old collection deleted successfully.")
    except Exception:
        print("No old collection found.")

    # Step 7: Create a fresh collection
    collection = client.create_collection(
        name="hr_policy"
    )

    # Step 8: Create unique IDs for every chunk
    ids = [
        f"{chunk['source']}_{chunk['chunk_number']}"
        for chunk in chunks
    ]

    # Step 9: Store chunks, embeddings and source details
    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[
            {
                "source": chunk["source"],
                "chunk_number": chunk["chunk_number"]
            }
            for chunk in chunks
        ]
    )

    print("\nDocuments stored successfully!")
    print("Total chunks stored:", collection.count())


if __name__ == "__main__":
    store_documents()
