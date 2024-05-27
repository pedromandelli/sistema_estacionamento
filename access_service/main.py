# access_service/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import uvicorn
import httpx

app = FastAPI()

uri = ""
client = MongoClient(uri)
db = client.Cluster0
access_log_collection = db.get_collection("access_log")
users_collection = db.get_collection("users")
credits_collection = db.get_collection("credits")
spots_collection = db.get_collection("spots")

class Access(BaseModel):
    cpf: str
    parking_lot: str
    action: str  # "entry" or "exit"

@app.post("/access/")
async def control_access(access: Access):
    user = users_collection.find_one({"cpf": access.cpf})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if access.action == "entry":
        spot = spots_collection.find_one({"parking_lot": access.parking_lot})
        if spot and spot["spots_available"] > 0:
            spots_collection.update_one({"parking_lot": access.parking_lot}, {"$inc": {"spots_available": -1}})
            access_log_collection.insert_one(access.dict())
            return {"message": "Access granted for entry"}
        else:
            raise HTTPException(status_code=400, detail="No available spots")
    
    elif access.action == "exit":
        credit = credits_collection.find_one({"cpf": access.cpf})
        if credit and credit["amount"] > 0:
            spots_collection.update_one({"parking_lot": access.parking_lot}, {"$inc": {"spots_available": 1}})
            credits_collection.update_one({"cpf": access.cpf}, {"$inc": {"amount": -1}})
            access_log_collection.insert_one(access.dict())
            return {"message": "Access granted for exit"}
        else:
            raise HTTPException(status_code=400, detail="Insufficient credits")
    
    raise HTTPException(status_code=400, detail="Invalid action")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
