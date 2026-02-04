from datetime import datetime

def patient_model(data):
    return {
        "role": "patient",
        "username": data["username"],
        "email": data["email"],
        "password": data["password"],
        "phone": data["phone"],
        "created_at": datetime.utcnow()
    }
