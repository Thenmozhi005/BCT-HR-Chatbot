
import streamlit as st
from chatbot import generate_answer

# Configure the webpage
st.set_page_config(
    page_title="BCT HR Assistant",
    page_icon="🤖",
    layout="centered"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:

    st.title("🤖 BCT HR Assistant")

    st.markdown("""
    ### About
    This chatbot answers employee HR questions
    using HR policy documents and user manuals.
    """)

    st.divider()

    st.markdown("### Technologies")
    st.markdown("""
    - Python
    - RAG
    - ChromaDB
    - Sentence Transformers
    - Ollama
    - Llama 3.2
    - Streamlit
    """)

    st.divider()

    # Sample HR questions
    st.markdown("### 💡 Sample Questions")

    sample_questions = [
        "What is the monthly payroll cutoff date?",
        "What should I do if I forget my ID card?",
        "How do I submit a claim in Oracle EBS?"
    ]

    for sample in sample_questions:
        if st.button(sample, use_container_width=True):
            st.session_state.selected_question = sample

    st.divider()

    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pop("selected_question", None)
        st.rerun()

# Main page
st.title("💬 HR Policy Assistant")

st.caption("Ask questions about HR policies and procedures.")

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input box
question = st.chat_input("Ask your HR question...")

# Check whether a sample question was selected
if "selected_question" in st.session_state:
    question = st.session_state.pop("selected_question")

# Process the question
if question:

    # Display user's question
    st.chat_message("user").markdown(question)

    # Save user question
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    # Generate chatbot response
    with st.chat_message("assistant"):

        with st.spinner("Searching HR documents..."):

            try:
                answer = generate_answer(question)
                st.markdown(answer)

            except Exception:
                answer = (
                    "Sorry, something went wrong while processing "
                    "your question. Please check whether the Ollama "
                    "application and required services are running, "
                    "then try again."
                )

                st.error(answer)

    # Save chatbot response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
