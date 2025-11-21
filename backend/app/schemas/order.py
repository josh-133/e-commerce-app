from typing import List
from pydantic import BaseModel
from app.schemas.cart import CartItem  # reuse your cart CartItem

class OrderCreate(BaseModel):
    cart_id: int
    cart_items: List[CartItem]  # reuse your cart item schema

class OrderUpdate(BaseModel):
    status: str

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    cart_items: List[CartItem]

    class Config:
        orm_mode = True