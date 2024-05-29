# spot_service/main.py
from typing import Optional, List, Dict

from fastapi import FastAPI, HTTPException

from pymongo import MongoClient
import uvicorn

from pydantic import BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from bson import ObjectId

from typing_extensions import Annotated

app = FastAPI()

uri = "mongodb+srv://pbalconimandelli:LtwoROD0lfsCYF7i@embarcados.soia3gj.mongodb.net/?retryWrites=true&w=majority&appName=Embarcados"
client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
db = client.Embarcados
spots_collection = db.get_collection("spots")

PyObjectId = Annotated[str, BeforeValidator(str)]

class SpotModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    parking_lot: str
    spots_available: int

@app.post("/spots/")
async def update_spots(spot: SpotModel):
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
        return SpotModel(**spot)
    raise HTTPException(status_code=404, detail="Parking lot not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
