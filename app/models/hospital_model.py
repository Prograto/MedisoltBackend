from datetime import datetime

def hospital_model(data):
    return {
        "role": "hospital",
        "hospital_name": data["hospital_name"],
        "email": data["email"],
        "password": data["password"],
        "address": data["address"],
        "license_number": data["license_number"],
        "created_at": datetime.utcnow()
    }
