from fastapi import APIRouter, Depends, HTTPException
from app.database import appointments_collection, availability_collection, doctors_collection
from app.schemas.appointment_schema import AppointmentSchema
from app.utils.dependencies import get_current_user
from bson import ObjectId

router = APIRouter(prefix="/appointment", tags=["Appointment"])


# -------------------------
# BOOK APPOINTMENT (PATIENT)
# -------------------------
@router.post("/book")
def book_appointment(data: AppointmentSchema, user=Depends(get_current_user)):
    if user["role"] != "patient":
        raise HTTPException(403, "Unauthorized")

    doctor = doctors_collection.find_one(
        {"_id": ObjectId(data.doctor_id)}
    )

    if not doctor:
        raise HTTPException(404, "Doctor not found")

    # Count bookings for the day
    booked_count = appointments_collection.count_documents({
        "doctor_id": data.doctor_id,
        "date": data.date
    })

    if booked_count >= doctor["max_slots_per_day"]:
        raise HTTPException(400, "No slots available")

    appointments_collection.insert_one({
        "doctor_id": data.doctor_id,
        "doctor_name": doctor["name"],
        "hospital_id": doctor["hospital_id"],
        "patient_id": user["id"],
        "patient_name": user.get("username"),
        "problem": data.problem,
        "date": data.date,
        "status": "booked"
    })

    return {"message": "Appointment booked successfully"}


# -------------------------
# HOSPITAL VIEW (DATE WISE)
# -------------------------
@router.get("/hospital")
def hospital_appointments(
    date: str,
    user=Depends(get_current_user)
):
    if user["role"] != "hospital":
        raise HTTPException(403, "Unauthorized")

    appointments = list(
        appointments_collection.find({
            "hospital_id": user["id"],
            "date": date
        })
    )

    for a in appointments:
        a["_id"] = str(a["_id"])

    return appointments




@router.get("/my")
def my_appointments(user=Depends(get_current_user)):
    appointments = list(
        appointments_collection.find({"patient_id": user["id"]})
    )

    for a in appointments:
        a["_id"] = str(a["_id"])

    return appointments

@router.delete("/cancel/{appointment_id}")
def cancel_appointment(
    appointment_id: str,
    user=Depends(get_current_user)
):
    appointments_collection.delete_one({
        "_id": ObjectId(appointment_id),
        "patient_id": user["id"]
    })

    return {"message": "Appointment cancelled"}
