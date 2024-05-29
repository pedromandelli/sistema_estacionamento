# gate_service/main.py
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

class GateControlModel(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    action: str = Field(..., pattern="^(open|close)$")  # "open" or "close"

@app.post("/gate/")
async def control_gate(control: GateControlModel):
    if control.action == "open":
        print("Gate is opening...")
    elif control.action == "close":
        print("Gate is closing...")
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
    return {"message": f"Gate {control.action} command sent"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
