# user_service/main.py
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
users_collection = db.get_collection("users")

PyObjectId = Annotated[str, BeforeValidator(str)]

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    cpf: str
    name: str
    category: str = Field(..., regex="^(estudante|professor|TAE|visitante)$")

@app.post("/users/")
async def create_user(user: UserModel):
    user_exists = users_collection.find_one({"cpf": user.cpf})
    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = users_collection.insert_one(user.dict())
    return user

@app.get("/users/{cpf}")
async def get_user(cpf: str):
    user = users_collection.find_one({"cpf": cpf})
    if user:
        return UserModel(**user)
    raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
