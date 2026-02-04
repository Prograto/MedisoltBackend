from fastapi import APIRouter, HTTPException
from app.database import users_collection, hospitals_collection
from app.schemas.auth_schema import (
    PatientRegisterSchema,
    HospitalRegisterSchema,
    LoginSchema,
)
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register/patient")
def register_patient(data: PatientRegisterSchema):
    if users_collection.find_one({"email": data.email}):
        raise HTTPException(400, "Email already exists")

    users_collection.insert_one({
        "role": "patient",
        "username": data.username,
        "email": data.email,
        "password": hash_password(data.password),
        "phone": data.phone
    })

    return {"message": "Patient registered successfully"}


@router.post("/register/hospital")
def register_hospital(data: HospitalRegisterSchema):
    if hospitals_collection.find_one({"email": data.email}):
        raise HTTPException(400, "Email already exists")

    hospitals_collection.insert_one({
        "role": "hospital",
        "hospital_name": data.hospital_name,
        "email": data.email,
        "password": hash_password(data.password),
        "address": data.address,
        "license_number": data.license_number
    })

    return {"message": "Hospital registered successfully"}


@router.post("/login")
def login(data: LoginSchema):
    # 🔥 ROLE-AWARE LOGIN (CORRECT)
    if data.role == "patient":
        account = users_collection.find_one({"email": data.email})
    elif data.role == "hospital":
        account = hospitals_collection.find_one({"email": data.email})
    else:
        raise HTTPException(400, "Invalid role")

    if not account or not verify_password(data.password, account["password"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({
        "id": str(account["_id"]),
        "role": account["role"]
    })

    return {
        "access_token": token,
        "role": account["role"]
    }
