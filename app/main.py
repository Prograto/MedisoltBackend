from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, doctor, availability, appointment, hospital, ai_chat

app = FastAPI(title="MediSlot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(doctor.router)
app.include_router(availability.router)
app.include_router(appointment.router)
app.include_router(hospital.router)
app.include_router(ai_chat.router)

@app.get("/")
def root():
    return {"status": "MediSlot backend running"}
