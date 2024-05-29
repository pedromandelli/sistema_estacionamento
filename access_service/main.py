# access_service/main.py
from typing import Optional, List, Dict

from fastapi import FastAPI, HTTPException

from pymongo import MongoClient
import uvicorn

from pydantic import BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from bson import ObjectId

from typing_extensions import Annotated

import httpx

PyObjectId = Annotated[str, BeforeValidator(str)]

app = FastAPI()

uri = "mongodb+srv://pbalconimandelli:LtwoROD0lfsCYF7i@embarcados.soia3gj.mongodb.net/?retryWrites=true&w=majority&appName=Embarcados"
client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
db = client.Embarcados
access_log_collection = db.get_collection("access_log")
users_collection = db.get_collection("users")
credits_collection = db.get_collection("credits")
spots_collection = db.get_collection("spots")

class AccessModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    cpf: str
    parking_lot: str
    action: str = Field(..., pattern="^(entry|exit)$")  # "entry" or "exit"

@app.post("/access/")
async def control_access(access: AccessModel):
    async with httpx.AsyncClient() as client:
        # Verifica usuário
        user_response = await client.get(f"http://localhost:8001/users/{access.cpf}")
        if user_response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")
        user = user_response.json()

        # Verifica vagas disponíveis
        spot_response = await client.get(f"http://localhost:8003/spots/{access.parking_lot}")
        if spot_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Parking lot not found")
        spot = spot_response.json()

        if access.action == "entry":
            if spot["spots_available"] > 0:
                await client.post("http://localhost:8003/spots/", json={"parking_lot": access.parking_lot, "spots_available": spot["spots_available"] - 1})
                access_log_collection.insert_one(access.dict())
                return {"message": "Access granted for entry"}
                await client.post("http://localhost:8005/gate/", json={"action": "open"})
                await client.post("http://localhost:8005/gate/", json={"action": "close"})
            else:
                raise HTTPException(status_code=400, detail="No available spots")
        
        elif access.action == "exit":
            if user["category"] in ["estudante", "visitante"]:
                credit_response = await client.get(f"http://localhost:8002/credits/{access.cpf}")
                if credit_response.status_code != 200:
                    raise HTTPException(status_code=400, detail="Insufficient credits")
                credit = credit_response.json()
                if credit["amount"] > 0:
                    await client.post(f"http://localhost:8002/credits/{access.cpf}/decrement")
                    await client.post("http://localhost:8003/spots/", json={"parking_lot": access.parking_lot, "spots_available": spot["spots_available"] + 1})
                    access_log_collection.insert_one(access.dict())
                    return {"message": "Access granted for exit"}
                    await client.post("http://localhost:8005/gate/", json={"action": "open"})
                else:
                    raise HTTPException(status_code=400, detail="Insufficient credits")
            else:
                await client.post("http://localhost:8003/spots/", json={"parking_lot": access.parking_lot, "spots_available": spot["spots_available"] + 1})
                access_log_collection.insert_one(access.dict())
                return {"message": "Access granted for exit"}
        
        raise HTTPException(status_code=400, detail="Invalid action")
 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
