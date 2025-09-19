from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.order_repository import OrdersRepository
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.dependencies.auth_dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = OrdersRepository(db)
    db_order = Order(**order.dict())
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return repo.create_order(db_order)

@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = OrdersRepository(db)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return repo.get_all_orders()

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = OrdersRepository(db)
    order = repo.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    elif order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return order

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = OrdersRepository(db)
    updated_order = repo.update_order(order_id, order_update)
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    elif updated_order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return updated_order

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = OrdersRepository(db)
    order = repo.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    elif order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    repo.delete_order(order)
    return f"Order with an id of {order_id} was successfully deleted"
        