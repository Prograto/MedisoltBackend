from pydantic import BaseModel

class AvailabilitySchema(BaseModel):
    doctor_id: str
    date: str
    total_slots: int
