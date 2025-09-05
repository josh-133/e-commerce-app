from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.order_repository import OrdersRepository
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    repo = OrdersRepository(db)
    db_order = Order(**order.dict())
    return repo.create_order(db_order)

@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    repo = OrdersRepository(db)
    return repo.get_all_orders()

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    repo = OrdersRepository(db)
    order = repo.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order