# user_service/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import uvicorn

app = FastAPI()

uri = ""
client = MongoClient(uri)
db = client.Cluster0
users_collection = db.get_collection("users")

class User(BaseModel):
    cpf: str
    name: str
    category: str

@app.post("/users/")
async def create_user(user: User):
    user_dict = user.dict()
    if users_collection.find_one({"cpf": user.cpf}):
        raise HTTPException(status_code=400, detail="User already exists")
    users_collection.insert_one(user_dict)
    return user_dict

@app.get("/users/{cpf}")
async def get_user(cpf: str):
    user = users_collection.find_one({"cpf": cpf})
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
