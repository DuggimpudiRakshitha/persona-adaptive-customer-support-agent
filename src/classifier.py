import os
import json
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


def classify_persona(user_message):

    try:

        client = genai.Client(
            api_key=get_api_key()
        )

        schema = {
            "type": "OBJECT",
            "properties": {
                "persona": {
                    "type": "STRING",
                    "enum": [
                        "Technical Expert",
                        "Frustrated User",
                        "Business Executive"
                    ]
                },
                "confidence": {
                    "type": "NUMBER"
                },
                "reasoning": {
                    "type": "STRING"
                }
            },
            "required": [
                "persona",
                "confidence",
                "reasoning"
            ]
        }

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction="""
Classify the customer into exactly one persona:

1. Technical Expert
2. Frustrated User
3. Business Executive

Return JSON only.
""",
                response_mime_type="application/json",
                response_schema=schema,
                temperature=0
            )
        )

        return json.loads(response.text)

    except Exception as e:

        print("Classifier Error:", e)

        return {
            "persona": "Technical Expert",
            "confidence": 0.5,
            "reasoning": str(e)
        }