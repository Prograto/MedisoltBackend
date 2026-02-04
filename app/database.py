from pymongo import MongoClient
from app.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["medislot_db"]

users_collection = db["users"]
hospitals_collection = db["hospitals"]
doctors_collection = db["doctors"]
availability_collection = db["availability"]
appointments_collection = db["appointments"]
