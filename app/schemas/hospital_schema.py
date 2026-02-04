from pydantic import BaseModel
from typing import List

class HospitalUpdateSchema(BaseModel):
    working_days: List[str]        # ["Monday", "Tuesday", ...]
    morning_time: str              # "09:00-12:30"
    evening_time: str              # "13:30-21:30"
    hospital_fee: int
