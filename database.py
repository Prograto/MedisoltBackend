from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client["medislot_db"]

users_collection = db["users"]
hospitals_collection = db["hospitals"]
doctors_collection = db["doctors"]
appointments_collection = db["appointments"]
availability_collection = db["availability"]
