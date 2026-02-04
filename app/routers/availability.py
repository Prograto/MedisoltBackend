from fastapi import APIRouter, Depends, HTTPException
from app.database import availability_collection, doctors_collection
from app.schemas.availability_schema import AvailabilitySchema
from app.utils.dependencies import get_current_user
from bson import ObjectId

router = APIRouter(prefix="/availability", tags=["Availability"])

@router.post("/set")
def set_availability(data: AvailabilitySchema, user=Depends(get_current_user)):
    if user["role"] != "hospital":
        raise HTTPException(403, "Unauthorized")

    availability_collection.update_one(
        {
            "doctor_id": data.doctor_id,
            "date": data.date
        },
        {
            "$set": {
                "doctor_id": data.doctor_id,
                "date": data.date,
                "total_slots": data.total_slots,
                "booked": 0
            }
        },
        upsert=True
    )

    return {"message": "Availability set"}

@router.get("/{doctor_id}/{date}")
def get_availability(doctor_id: str, date: str):
    avail = availability_collection.find_one({
        "doctor_id": doctor_id,
        "date": date
    })

    if not avail:
        # 🔥 AUTO-CREATE from doctor max_slots_per_day
        doctor = doctors_collection.find_one(
            {"_id": ObjectId(doctor_id)}
        )

        if not doctor:
            return {"total_slots": 0, "booked": 0, "available": 0}

        availability_collection.insert_one({
            "doctor_id": doctor_id,
            "date": date,
            "total_slots": doctor["max_slots_per_day"],
            "booked": 0
        })

        return {
            "total_slots": doctor["max_slots_per_day"],
            "booked": 0,
            "available": doctor["max_slots_per_day"]
        }

    return {
        "total_slots": avail["total_slots"],
        "booked": avail["booked"],
        "available": avail["total_slots"] - avail["booked"]
    }
