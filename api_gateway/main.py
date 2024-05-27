# api_gateway/main.py
from fastapi import FastAPI, HTTPException
import uvicorn
import httpx

app = FastAPI()

@app.get("/users/{cpf}")
async def get_user(cpf: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8001/users/{cpf}")
        return response.json()

@app.post("/credits/")
async def add_credit(credit: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8002/credits/", json=credit)
        return response.json()

@app.get("/spots/{parking_lot}")
async def get_spots(parking_lot: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8003/spots/{parking_lot}")
        return response.json()

@app.post("/access/")
async def control_access(access: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8004/access/", json=access)
        return response.json()

@app.post("/gate/")
async def control_gate(control: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8005/gate/", json=control)
        return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
