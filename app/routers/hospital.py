from fastapi import APIRouter, Depends, HTTPException
from app.database import (
    hospitals_collection,
    doctors_collection,
    appointments_collection
)
from app.schemas.hospital_schema import HospitalUpdateSchema
from app.utils.dependencies import get_current_user
from bson import ObjectId

router = APIRouter(
    prefix="/hospital",
    tags=["Hospital"]
)

# -------------------------------
# Get Logged-in Hospital Profile
# -------------------------------
@router.get("/me")
def get_hospital_profile(user=Depends(get_current_user)):
    if user["role"] != "hospital":
        raise HTTPException(status_code=403, detail="Access denied")

    hospital = hospitals_collection.find_one(
        {"_id": ObjectId(user["id"])},
        {"password": 0}
    )

    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    hospital["_id"] = str(hospital["_id"])
    return hospital


# -------------------------------
# Get All Doctors of This Hospital
# -------------------------------
@router.get("/doctors")
def get_my_doctors(user=Depends(get_current_user)):
    if user["role"] != "hospital":
        raise HTTPException(status_code=403, detail="Access denied")

    doctors = list(
        doctors_collection.find(
            {"hospital_id": user["id"]},
            {"_id": 0}
        )
    )
    return doctors


# -------------------------------
# Get All Appointments for Hospital
# -------------------------------
@router.get("/appointments")
def get_hospital_appointments(user=Depends(get_current_user)):
    if user["role"] != "hospital":
        raise HTTPException(status_code=403, detail="Access denied")

    appointments = list(
        appointments_collection.find(
            {"hospital_id": user["id"]},
            {"_id": 0}
        )
    )
    return appointments

@router.put("/update")
def update_hospital(
    data: HospitalUpdateSchema,
    user=Depends(get_current_user)
):
    if user["role"] != "hospital":
        raise HTTPException(403, "Unauthorized")

    hospitals_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": data.dict()}
    )

    return {"message": "Hospital details updated"}

@router.get("/details/{hospital_id}")
def hospital_details(hospital_id: str):
    hospital = hospitals_collection.find_one(
        {"_id": ObjectId(hospital_id)},
        {"password": 0}
    )
    hospital["_id"] = str(hospital["_id"])
    return hospital
