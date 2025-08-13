from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session, create_engine, select
from .models import Order
from .schemas import OrderCreate, OrderRead
import os

DB_URL = os.getenv("DB_URL", "sqlite:///./orders.db")
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}
engine = create_engine(DB_URL, connect_args=connect_args)

app = FastAPI(title="orders-service")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.post("/orders", response_model=OrderRead, status_code=201)
def create_order(payload: OrderCreate):
    with Session(engine) as session:
        order = Order(**payload.model_dump())
        session.add(order)
        session.commit()
        session.refresh(order)
        return order

@app.get("/orders/{order_id}", response_model=OrderRead)
def get_order(order_id: int):
    with Session(engine) as session:
        order = session.get(Order, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

@app.get("/orders", response_model=list[OrderRead])
def list_orders():
    with Session(engine) as session:
        return session.exec(select(Order)).all()
