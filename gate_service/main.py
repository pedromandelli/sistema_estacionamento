# gate_service/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class GateControl(BaseModel):
    action: str  # "open" or "close"

@app.post("/gate/")
async def control_gate(control: GateControl):
    if control.action == "open":
        print("Gate is opening...")
    elif control.action == "close":
        print("Gate is closing...")
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
    return {"message": f"Gate {control.action} command sent"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
