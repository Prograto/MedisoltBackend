from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.database import doctors_collection, hospitals_collection
from app.schemas.doctor_schema import (
    DoctorCreateSchema,
    DoctorUpdateSchema
)
from app.utils.dependencies import get_current_user
from app.database import appointments_collection
from datetime import date, datetime

router = APIRouter(prefix="/doctor", tags=["Doctor"])

# ➕ Add Doctor
@router.post("/add")
def add_doctor(data: DoctorCreateSchema, user=Depends(get_current_user)):
    if user["role"] != "hospital":
        raise HTTPException(403, "Unauthorized")

    hospital = hospitals_collection.find_one({"_id": ObjectId(user["id"])})

    doctors_collection.insert_one({
        "hospital_id": user["id"],
        "hospital_name": hospital["hospital_name"],
        "hospital_address": hospital["address"],  # ✅ IMPORTANT
        **data.dict()
    })

    return {"message": "Doctor added successfully"}



# 📄 Get Doctors List
@router.get("/list")
def list_doctors(user=Depends(get_current_user)):
    if user["role"] != "hospital":
        raise HTTPException(403, "Unauthorized")

    doctors = list(
        doctors_collection.find({"hospital_id": user["id"]})
    )

    for d in doctors:
        d["_id"] = str(d["_id"])

    return doctors


# ✏️ Update Doctor
@router.put("/update/{doctor_id}")
def update_doctor(
    doctor_id: str,
    data: DoctorUpdateSchema,
    user=Depends(get_current_user)
):
    if user["role"] != "hospital":
        raise HTTPException(403, "Unauthorized")

    doctors_collection.update_one(
        {
            "_id": ObjectId(doctor_id),
            "hospital_id": user["id"]
        },
        {"$set": data.dict(exclude_unset=True)}
    )

    return {"message": "Doctor updated successfully"}

@router.delete("/delete/{doctor_id}")
def delete_doctor(
    doctor_id: str,
    user=Depends(get_current_user)
):
    if user["role"] != "hospital":
        raise HTTPException(403, "Unauthorized")

    doctors_collection.delete_one({
        "_id": ObjectId(doctor_id),
        "hospital_id": user["id"]
    })

    return {"message": "Doctor deleted"}


@router.get("/public")
def public_doctors(
    date: str | None = None,
    specialization: str | None = None,
    hospital_id: str | None = None
):
    query = {}

    if specialization:
        query["specialization"] = specialization
    if hospital_id:
        query["hospital_id"] = hospital_id

    doctors = list(doctors_collection.find(query))

    selected_date = date
    selected_day = None

    if selected_date:
        selected_day = datetime.fromisoformat(selected_date).strftime("%A")

    for d in doctors:
        d["_id"] = str(d["_id"])

        # Normalize availability days
        availability_days = [
            day.strip().capitalize()
            for day in d.get("availability_days", [])
        ]

        # Check working day
        d["is_working_today"] = (
            selected_day in availability_days if selected_day else False
        )

        # Count booked slots for selected date
        booked = 0
        if selected_date:
            booked = appointments_collection.count_documents({
                "doctor_id": d["_id"],
                "date": selected_date
            })

        d["booked_slots_today"] = booked
        d["available_slots"] = max(
            d["max_slots_per_day"] - booked,
            0
        )

        # Attach hospital info
        hospital = hospitals_collection.find_one(
            {"_id": ObjectId(d["hospital_id"])},
            {"password": 0}
        )

        if hospital:
            d["hospital_fee"] = hospital.get("hospital_fee", 0)
            d["hospital_morning_time"] = hospital.get("morning_time")
            d["hospital_evening_time"] = hospital.get("evening_time")

    return doctors



@router.get("/hospital/{hospital_id}")
def get_doctors(hospital_id: str):
    return list(doctors_collection.find({"hospital_id": hospital_id}, {"_id": 0}))
