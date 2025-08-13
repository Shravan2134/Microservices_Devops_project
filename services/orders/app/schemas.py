from sqlmodel import SQLModel

class OrderCreate(SQLModel):
    user_id: int
    item: str
    quantity: int

class OrderRead(SQLModel):
    id: int
    user_id: int
    item: str
    quantity: int
