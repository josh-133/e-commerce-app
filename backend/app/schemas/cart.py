from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.enums import CartStatus

# Each product in the cart
class CartItem(BaseModel):
    product_id: int
    quantity: int
    price_at_time: Optional[float] = None  # Optional, stores price at time of adding

    class Config:
        orm_mode = True

# Schema for creating a new cart
class CartCreate(BaseModel):
    user_id: int
    cart_items: List[CartItem] = []  # Can start empty
    status: Optional[CartStatus] = CartStatus.ACTIVE

# Schema for updating a cart
class CartUpdate(BaseModel):
    cart_items: Optional[List[CartItem]] = None
    status: Optional[CartStatus] = None

# Schema for reading cart (response)
class CartResponse(BaseModel):
    id: int
    user_id: int
    cart_items: List[CartItem]
    created_at: datetime
    updated_at: datetime
    status: CartStatus

    class Config:
        orm_mode = True