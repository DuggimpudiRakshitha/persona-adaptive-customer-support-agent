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


def generate_response(query, persona, chunks):

    context = "\n\n".join(
        [
            f"Source: {chunk['source']}\n{chunk['text']}"
            for chunk in chunks
        ]
    )

    try:

        client = genai.Client(
            api_key=get_api_key()
        )

        if persona == "Technical Expert":

            style = """
Provide detailed technical explanations.
Provide root cause analysis.
Provide troubleshooting steps.
Use bullet points.
"""

        elif persona == "Frustrated User":

            style = """
Be empathetic.
Acknowledge the frustration.
Use simple language.
Provide clear next steps.
"""

        else:

            style = """
Be concise.
Focus on business impact.
Focus on resolution timeline.
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=query,
            config=types.GenerateContentConfig(
                system_instruction=f"""
You are a customer support assistant.

Persona:
{persona}

Response Style:
{style}

Answer ONLY using the provided context.

Context:
{context}
""",
                temperature=0.2
            )
        )

        return response.text

    except Exception as e:

        print("Generator Error:", e)

        # Fallback when Gemini quota is exceeded
        if chunks:

            response = "Based on the retrieved knowledge base:\n\n"

            for chunk in chunks[:3]:
                response += (
                    f"Source: {chunk['source']}\n"
                    f"{chunk['text']}\n\n"
                )

            response += "\n\nResponse generated from the knowledge base."

            return response

        return "No relevant information found."