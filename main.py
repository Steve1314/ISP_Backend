from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="ISP Finder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise Exception("❌ Missing MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["isp_db"]
collection = db["providers"]

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/providers/{zip_code}")
def get_providers(zip_code: str):
    providers = list(collection.find({"zip": zip_code}, {"_id": 0}))
    if not providers:
        raise HTTPException(status_code=404, detail="No providers found for this ZIP")
    return {"zip": zip_code, "providers": providers}
