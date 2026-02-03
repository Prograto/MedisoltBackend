from fastapi import FastAPI
from routers import auth, hospital, doctor, appointment

app = FastAPI(title="MediSlot API")

app.include_router(auth.router)
app.include_router(hospital.router)
app.include_router(doctor.router)
app.include_router(appointment.router)

@app.get("/")
def root():
    return {"message": "MediSlot Backend Running"}
