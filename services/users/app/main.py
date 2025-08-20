from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session, create_engine, select
from .models import User
from .schemas import UserCreate, UserRead
import os

# just for testing

DB_URL = os.getenv("DB_URL", "sqlite:///./users.db")
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}
engine = create_engine(DB_URL, connect_args=connect_args)

app = FastAPI(title="users-service")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.post("/users", response_model=UserRead, status_code=201)
def create_user(payload: UserCreate):
    with Session(engine) as session:
        user = User(name=payload.name, email=payload.email)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

@app.get("/users", response_model=list[UserRead])
def list_users():
    with Session(engine) as session:
        return session.exec(select(User)).all()
