from src.config import (
    CONFIDENCE_THRESHOLD,
    SENSITIVE_KEYWORDS
)

def should_escalate(
    query,
    retrieved_chunks
):

    query = query.lower()

    for keyword in SENSITIVE_KEYWORDS:

        if keyword in query:
            return True

    if len(retrieved_chunks) == 0:
        return True

    return False


def generate_handoff(
    persona,
    query,
    retrieved_chunks
):

    return {
        "persona": persona,
        "issue": query,
        "documents_used": [
            chunk["source"]
            for chunk in retrieved_chunks
        ],
        "attempted_steps": [],
        "recommendation":
        "Human review required."
    }