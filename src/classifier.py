def classify_persona(user_message):
    
    text = user_message.lower()

    frustrated_keywords = [
        "refund",
        "angry",
        "frustrated",
        "terrible",
        "unacceptable",
        "complaint",
        "charged",
        "duplicate charge",
        "cancel"
    ]

    business_keywords = [
        "revenue",
        "business",
        "executive",
        "enterprise",
        "customer satisfaction",
        "outage",
        "clients",
        "financial impact",
        "operations"
    ]

    if any(word in text for word in frustrated_keywords):
        return {
            "persona": "Frustrated User",
            "confidence": 0.95,
            "reasoning": "Detected frustration-related keywords."
        }

    if any(word in text for word in business_keywords):
        return {
            "persona": "Business Executive",
            "confidence": 0.95,
            "reasoning": "Detected business-related keywords."
        }

    return {
        "persona": "Technical Expert",
        "confidence": 0.95,
        "reasoning": "Detected technical support language."
    }