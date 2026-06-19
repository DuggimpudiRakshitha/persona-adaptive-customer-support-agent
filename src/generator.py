import os
import streamlit as st

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def get_api_key():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        api_key = st.secrets.get("GEMINI_API_KEY")

    return api_key


def generate_response(
    query,
    persona,
    chunks
):

    try:

        client = genai.Client(
            api_key=get_api_key()
        )

        context = "\n\n".join(
            [
                f"Source: {c['source']}\n{c['text']}"
                for c in chunks
            ]
        )

        if persona == "Technical Expert":

            style = """
Provide detailed technical explanations.
Provide root cause analysis.
Provide troubleshooting steps.
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
            model="gemini-2.0-flash",
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

    except Exception as e:

        print("Generator Error:", e)

        return f"Unable to generate response. Error: {str(e)}"