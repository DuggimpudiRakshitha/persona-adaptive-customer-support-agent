import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def classify_persona(user_message):

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
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
        model="models/gemini-2.5-flash",
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction="""
Classify customer into:
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