
# Import libraries to work with files and documents
from pathlib import Path
from docx import Document
from pypdf import PdfReader

# Find our main project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Location of our HR documents
DOCUMENTS_DIR = BASE_DIR / "documents"


def extract_text_from_docx(file_path):
    """Extract text from a Word document."""
    doc = Document(file_path)

    text = []

    # Extract paragraphs
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)

    # Extract text from tables
    for table in doc.tables:
        for row in table.rows:
            row_text = " | ".join(cell.text for cell in row.cells)
            if row_text.strip():
                text.append(row_text)

    return "\n".join(text)


def extract_text_from_pdf(file_path):
    """Extract text from a PDF document."""
    reader = PdfReader(file_path)

    text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return "\n".join(text)


def extract_text_from_txt(file_path):
    """Extract text from a text file."""
    return file_path.read_text(encoding="utf-8")


def extract_all_documents():
    """Read all supported HR documents."""

    documents = []

    for file_path in DOCUMENTS_DIR.iterdir():

        # Read Word documents
        if file_path.suffix.lower() == ".docx":
            text = extract_text_from_docx(file_path)

        # Read PDF documents
        elif file_path.suffix.lower() == ".pdf":
            text = extract_text_from_pdf(file_path)

        # Read text documents
        elif file_path.suffix.lower() == ".txt":
            text = extract_text_from_txt(file_path)

        else:
            continue

        # Store document name and extracted text
        documents.append({
            "source": file_path.name,
            "text": text
        })

    return documents


# Run the extraction
if __name__ == "__main__":

    docs = extract_all_documents()

    print(f"\nDocuments found: {len(docs)}")

    for doc in docs:
        print("\n" + "=" * 50)
        print("Document:", doc["source"])
        print("Characters extracted:", len(doc["text"]))
        print("\nPreview:")
        print(doc["text"][:300])
