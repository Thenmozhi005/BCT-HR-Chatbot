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

## Project Features

- Answers HR-related questions using company documents.
- Retrieves relevant information using semantic search.
- Generates context-based answers using an LLM.
- Provides a fallback response when information is unavailable.
- Maintains logs of questions, retrieved documents, and chatbot answers.
- Evaluates chatbot performance using a predefined question set.

## Setup Instructions

### 1. Create a Virtual Environment

python -m venv venv

### 2. Activate the Virtual Environment

.\venv\Scripts\Activate.ps1

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Download the Ollama Model

ollama pull llama3.2:3b

### 5. Add HR Policy Documents

Place the approved HR policy documents inside the documents folder.

### 6. Store Documents

python src/store_data.py

### 7. Run the Chatbot

python src/chatbot.py

## Evaluation Results

The chatbot was tested using 10 predefined questions.

- Total Questions: 10
- Correct Answers: 10
- Incorrect Answers: 0
- Accuracy: 100%
