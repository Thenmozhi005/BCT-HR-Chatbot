
# Import our document extraction function
from extract_documents import extract_all_documents


# Chunk settings
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 250


def create_chunks(documents):
    """Divide extracted documents into smaller chunks."""

    all_chunks = []

    for document in documents:

        text = document["text"]
        source = document["source"]

        start = 0
        chunk_number = 0

        while start < len(text):

            end = start + CHUNK_SIZE

            # Extract a piece of text
            chunk_text = text[start:end]

            # Store chunk and its information
            all_chunks.append({
                "text": chunk_text,
                "source": source,
                "chunk_number": chunk_number
            })

            chunk_number += 1

            # Move forward while keeping some overlap
            start += CHUNK_SIZE - CHUNK_OVERLAP

    return all_chunks


# Run the chunking process
if __name__ == "__main__":

    # Extract text from all documents
    documents = extract_all_documents()

    # Divide documents into chunks
    chunks = create_chunks(documents)

    print("Total documents:", len(documents))
    print("Total chunks:", len(chunks))

    # Display a few chunks
    for chunk in chunks[:3]:
        print("\n" + "=" * 50)
        print("Source:", chunk["source"])
        print("Chunk number:", chunk["chunk_number"])
        print("Chunk length:", len(chunk["text"]))
        print("Text preview:")
        print(chunk["text"][:200])
