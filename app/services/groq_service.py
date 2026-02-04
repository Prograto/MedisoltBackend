import requests
from app.config import GROQ_API_KEY

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_groq(message: str):
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a medical triage assistant.\n\n"
                    "Rules:\n"
                    "- If the user asks which doctor/specialist to consult → intent MUST be 'booking'\n"
                    "- Choose ONE specialization only (e.g., Neurology, Cardiology, Orthopedics)\n"
                    "- Return ONLY valid JSON\n\n"
                    "Booking format:\n"
                    "{ \"intent\": \"booking\", \"specialization\": \"Neurology\", "
                    "\"reply\": \"You should consult a Neurology doctor.\" }\n\n"
                    "Chat format:\n"
                    "{ \"intent\": \"chat\", \"reply\": \"medical advice\" }"
                )
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "temperature": 0.2
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        GROQ_URL,
        json=payload,
        headers=headers,
        timeout=30
    )

    return response.json()
