from fastapi import FastAPI, HTTPException
import uvicorn
import httpx
import spot_service.main as spot_service
import user_service.main as user_service
import credit_service.main as credit_service
import access_service.main as access_service

spot_model = spot_service.SpotModel
user_model = user_service.UserModel
credit_model = credit_service.CreditModel
access_model = access_service.AccessModel

app = FastAPI()

async def make_request(method: str, url: str, json: dict = None):
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, json=json)
        response.raise_for_status()
        return response.json()

@app.post("/users/")
async def create_user(user: user_model):
    return await make_request("POST", "http://localhost:8001/users/", json=user.dict())

@app.get("/users/{cpf}")
async def get_user(cpf: str):
    return await make_request("GET", f"http://localhost:8001/users/{cpf}")

@app.post("/credits/")
async def add_credit(credit: credit_model):
    return await make_request("POST", "http://localhost:8002/credits/", json=credit.dict())

@app.get("/credits/{cpf}")
async def get_credit(cpf: str):
    return await make_request("GET", f"http://localhost:8002/credits/{cpf}")

@app.post("/credits/{cpf}/decrement")
async def decrement_credits(cpf: str):
    return await make_request("POST", f"http://localhost:8002/credits/{cpf}/decrement")

@app.get("/spots/{parking_lot}")
async def get_spots(parking_lot: str):
    return await make_request("GET", f"http://localhost:8003/spots/{parking_lot}")

@app.post("/spots/")
async def update_spots(spot: spot_model):
    return await make_request("POST", "http://localhost:8003/spots/", json=spot.dict())

@app.post("/access/")
async def control_access(access: access_model):
    return await make_request("POST", "http://localhost:8004/access/", json=access.dict())

@app.post("/gate/")
async def control_gate(action: str):
    if action == "open":
        print("Abrindo cancela...")
        return {"message": "Cancela aberta"}
    elif action == "close":
        print("Fechando cancela...")
        return {"message": "Cancela fechada"}
    else:
        raise HTTPException(status_code=400, detail="Ação inválida para a cancela")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)