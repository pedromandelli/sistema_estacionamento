# spot_service/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import uvicorn

app = FastAPI()

uri = ""
client = MongoClient(uri)
db = client.Cluster0
spots_collection = db.get_collection("spots")

class Spot(BaseModel):
    parking_lot: str
    spots_available: int

@app.post("/spots/")
async def update_spots(spot: Spot):
    existing_spot = spots_collection.find_one({"parking_lot": spot.parking_lot})
    if existing_spot:
        spots_collection.update_one({"parking_lot": spot.parking_lot}, {"$set": {"spots_available": spot.spots_available}})
    else:
        spots_collection.insert_one(spot.dict())
    return spot

@app.get("/spots/{parking_lot}")
async def get_spots(parking_lot: str):
    spot = spots_collection.find_one({"parking_lot": parking_lot})
    if spot:
        return spot
    raise HTTPException(status_code=404, detail="Parking lot not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
