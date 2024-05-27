# credit_service/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import uvicorn

app = FastAPI()

uri = "mongodb+srv://pbalconimandelli:LtwoROD0lfsCYF7i@embarcados.soia3gj.mongodb.net/?retryWrites=true&w=majority&appName=Embarcados"
client = MongoClient(uri)
db = client.Embarcados
credits_collection = db.get_collection("credits")

class Credit(BaseModel):
    cpf: str
    amount: float

@app.post("/credits/")
async def add_credit(credit: Credit):
    user_credit = credits_collection.find_one({"cpf": credit.cpf})
    if user_credit:
        new_amount = user_credit["amount"] + credit.amount
        credits_collection.update_one({"cpf": credit.cpf}, {"$set": {"amount": new_amount}})
    else:
        credits_collection.insert_one(credit.dict())
    return {"cpf": credit.cpf, "amount": credit.amount}

@app.get("/credits/{cpf}")
async def get_credit(cpf: str):
    credit = credits_collection.find_one({"cpf": cpf})
    if credit:
        return credit
    raise HTTPException(status_code=404, detail="Credit not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
