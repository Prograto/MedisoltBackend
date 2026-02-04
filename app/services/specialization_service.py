from app.database import doctors_collection

def get_all_specializations():
    return doctors_collection.distinct("specialization")
