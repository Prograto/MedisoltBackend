from pydantic import BaseModel

class AppointmentSchema(BaseModel):
    doctor_id: str
    date: str              # YYYY-MM-DD
    problem: str           # Patient complaint
