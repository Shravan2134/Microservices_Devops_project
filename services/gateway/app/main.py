from fastapi import FastAPI, HTTPException
import os, httpx

USERS_URL = os.getenv("USERS_URL", "http://localhost:8001")
ORDERS_URL = os.getenv("ORDERS_URL", "http://localhost:8002")

app = FastAPI(title="gateway")

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.get("/api/users")
async def list_users():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{USERS_URL}/users")
        r.raise_for_status()
        return r.json()

@app.post("/api/users")
async def create_user(payload: dict):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{USERS_URL}/users", json=payload)
        r.raise_for_status()
        return r.json()

@app.get("/api/orders")
async def list_orders():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{ORDERS_URL}/orders")
        r.raise_for_status()
        return r.json()

@app.post("/api/orders")
async def create_order(payload: dict):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{ORDERS_URL}/orders", json=payload)
        if r.status_code >= 400:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        return r.json()
