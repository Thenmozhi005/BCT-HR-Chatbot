# BCT HR Chatbot

## Project Overview

The BCT HR Chatbot is an AI-powered assistant developed using Retrieval-Augmented Generation (RAG).

It helps associates find answers to HR-related questions using company policy documents and user manuals.

The chatbot retrieves relevant information from documents and generates answers based on the retrieved context.

## Technologies Used

- Python
- ChromaDB
- Sentence Transformers
- Ollama
- Llama 3.2 (3B)
- Retrieval-Augmented Generation (RAG)
- Streamlit

## Project Features

- Answers HR-related questions using company documents.
- Retrieves relevant information using semantic search.
- Generates context-based answers using an LLM.
- Provides a fallback response when information is unavailable.
- Maintains logs of questions, retrieved documents, and chatbot answers.
- Evaluates chatbot performance using a predefined question set.
- Provides a web-based chat interface using Streamlit.
- Supports sample HR questions and chat history.
- Includes a Clear Chat option.

## Setup Instructions

### 1. Create a Virtual Environment

```bash
python -m venv venv
```

### 2. Activate the Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the Ollama Model

```bash
ollama pull llama3.2:3b
```

Make sure the Ollama application is running before starting the chatbot.

### 5. Add HR Policy Documents

Place the approved HR policy documents inside the `documents` folder.

### 6. Store Documents

```bash
python src/store_data.py
```

This extracts, processes, and stores document information in ChromaDB.

### 7. Run the Chatbot in Terminal

```bash
python src/chatbot.py
```

### 8. Run the Web Interface

```bash
python -m streamlit run src/app.py
```

The Streamlit application will open in your default browser.

## Evaluation Results

The chatbot was tested using 10 predefined questions.

- Total Questions: 10
- Correct Answers: 10
- Incorrect Answers: 0
- Accuracy: 100%

*Note: The reported accuracy is based on the predefined set of 10 evaluation questions.*