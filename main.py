from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ISP Finder API")

# Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MongoDB Connection ----------------
client = MongoClient("mongodb://localhost:27017/")  # or use Atlas
db = client.isp_db
collection = db.providers

# ---------------- API Routes ----------------

@app.get("/providers/{zip_code}")
def get_providers(zip_code: str):
    providers = list(collection.find({"zip": zip_code}, {"_id": 0}))  # hide _id
    if not providers:
        raise HTTPException(status_code=404, detail="No providers found for this ZIP")
    return {"zip": zip_code, "providers": providers}
