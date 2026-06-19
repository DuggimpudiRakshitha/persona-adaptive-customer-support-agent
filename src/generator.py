import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def generate_response(
    query,
    persona,
    chunks
):

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    context = "\n\n".join(
        [
            f"Source: {c['source']}\n{c['text']}"
            for c in chunks
        ]
    )

    if persona == "Technical Expert":

        style = """
Provide detailed technical explanations,
root cause analysis,
and troubleshooting steps.
"""

    elif persona == "Frustrated User":

        style = """
Be empathetic.
Use simple language.
Provide clear actions.
"""

    else:

        style = """
Be concise.
Focus on business impact.
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=query,
        config=types.GenerateContentConfig(
            system_instruction=f"""
{style}

Use ONLY the provided context.

Context:
{context}
""",
            temperature=0.2
        )
    )

    return response.text