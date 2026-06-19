from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from src.classifier import classify_persona
from src.rag_pipeline import LocalRAG
from src.generator import generate_response
from src.escalator import (
    should_escalate,
    generate_handoff
)

st.set_page_config(
    page_title="Persona Support Agent"
)

st.title(
    "Persona-Adaptive Customer Support Agent"
)

# Initialize RAG
rag = LocalRAG()

# Load documents once
if "indexed" not in st.session_state:

    rag.ingest_documents()

    st.session_state.indexed = True

# Store documents in session
if "documents" not in st.session_state:
    st.session_state.documents = rag.documents

# Debug section (remove later)
with st.expander("Loaded Documents"):
    st.write(st.session_state.documents)

query = st.text_area(
    "Enter customer query"
)

if st.button("Submit"):

    if not query.strip():
        st.warning("Please enter a query.")
        st.stop()

    # Persona Classification
    persona_result = classify_persona(query)

    persona = persona_result["persona"]

    # Reload docs into RAG object
    rag.documents = st.session_state.documents

    # Retrieve relevant docs
    chunks = rag.retrieve(query)

    st.subheader("Detected Persona")
    st.write(persona)

    st.subheader("Retrieved Sources")

    if chunks:

        for chunk in chunks:

            st.write(
                f"{chunk['source']} | Score: {chunk['score']}"
            )

    else:

        st.write("No documents retrieved")

    # Escalation check
    escalate = should_escalate(
        query,
        chunks
    )

    if escalate:

        st.error(
            "Escalated to Human Agent"
        )

        handoff = generate_handoff(
            persona,
            query,
            chunks
        )

        st.json(handoff)

    else:

        answer = generate_response(
            query,
            persona,
            chunks
        )

        st.subheader(
            "Generated Response"
        )

        st.write(answer)