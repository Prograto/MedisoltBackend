from pydantic import BaseModel
from typing import List, Optional

class DoctorCreateSchema(BaseModel):
    name: str
    specialization: str
    designation: str
    experience: int
    description: str
    availability_days: List[str]
    availability_time: str
    max_slots_per_day: int


class DoctorUpdateSchema(BaseModel):
    name: Optional[str]
    specialization: Optional[str]
    designation: Optional[str]
    experience: Optional[int]
    description: Optional[str]
    availability_days: Optional[List[str]]
    availability_time: Optional[str]
    max_slots_per_day: Optional[int]
