from fastapi import APIRouter, HTTPException
from app.services.groq_service import ask_groq
from app.database import doctors_collection
import json

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/chat")
def chat_ai(payload: dict):
    user_message = payload.get("message")

    if not user_message:
        raise HTTPException(400, "Message is required")

    ai = ask_groq(user_message)

    print("GROQ RAW RESPONSE:", ai)

    if "choices" not in ai:
        return {
            "type": "chat",
            "reply": "Please describe your health issue so I can help 😊"
        }

    try:
        content = ai["choices"][0]["message"]["content"]
        data = json.loads(content)
    except Exception as e:
        print("AI PARSE ERROR:", e)
        return {
            "type": "chat",
            "reply": "I can help with medical questions or booking doctors."
        }

    # ---------------- BOOKING FLOW ----------------
    if data.get("intent") == "booking":
        specialization = data.get("specialization")

        # 🔥 VERY IMPORTANT: flexible matching
        doctors = list(
            doctors_collection.find(
                {
                    "specialization": {
                        "$regex": specialization,
                        "$options": "i"
                    }
                },
                {"password": 0}
            ).limit(5)
        )

        for d in doctors:
            d["_id"] = str(d["_id"])

        if not doctors:
            return {
                "type": "chat",
                "reply": f"No doctors found for {specialization}. Please try another issue."
            }

        return {
            "type": "booking",
            "specialization": specialization,
            "doctors": doctors
        }

    # ---------------- NORMAL CHAT ----------------
    return {
        "type": "chat",
        "reply": data.get(
            "reply",
            "Please consult a doctor for accurate advice."
        )
    }
