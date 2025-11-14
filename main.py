from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ISP Finder API")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MongoDB Atlas ----------------
MONGO_URI = "mongodb+srv://vivek:vivek@cluster0.avwiuf8.mongodb.net/isp_db?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["isp_db"]
collection = db["providers"]

# ---------------- Routes ----------------

@app.get("/")
def home():
    return {"status": "API Running"}

@app.get("/providers/{zip_code}")
def get_providers(zip_code: str):
    providers = list(collection.find({"zip": zip_code}, {"_id": 0}))
    
    if not providers:
        raise HTTPException(status_code=404, detail="No providers found for this ZIP")
    
    return {"zip": zip_code, "providers": providers}
