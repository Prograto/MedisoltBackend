from pydantic import BaseModel, EmailStr

class PatientRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone: str


class HospitalRegisterSchema(BaseModel):
    hospital_name: str
    email: EmailStr
    password: str
    address: str
    license_number: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    role: str   # "patient" or "hospital"
