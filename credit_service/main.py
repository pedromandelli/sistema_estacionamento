# credit_service/main.py
from typing import Optional, List, Dict

from fastapi import FastAPI, HTTPException

from pymongo import MongoClient
import uvicorn

from pydantic import BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from bson import ObjectId

from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

app = FastAPI()

uri = "mongodb+srv://pbalconimandelli:LtwoROD0lfsCYF7i@embarcados.soia3gj.mongodb.net/?retryWrites=true&w=majority&appName=Embarcados"
client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
db = client.Embarcados
users_collection = db.get_collection("users")
credits_collection = db.get_collection("credits")

class CreditModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    cpf: str
    amount: float

@app.post("/credits/")
async def add_credit(credit: CreditModel):
    user = users_collection.find_one({"cpf": credit.cpf})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_credit = credits_collection.find_one({"cpf": credit.cpf})
    if user_credit:
        new_amount = user_credit["amount"] + credit.amount
        credits_collection.update_one({"cpf": credit.cpf}, {"$set": {"amount": new_amount}})
    else:
        credits_collection.insert_one(credit.dict())
    return {"cpf": credit.cpf, "amount": credit.amount}

@app.get("/credits/{cpf}")
async def get_credit(cpf: str):
    credit_data = credits_collection.find_one({"cpf": cpf})
    if credit_data:
        return CreditModel(**credit_data)
    raise HTTPException(status_code=404, detail="Credit not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
