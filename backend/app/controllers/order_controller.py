from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.order_repository import OrdersRepository
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.dependencies.auth_dependencies import get_current_user
from app.models.user import User
from app.kafka.producer import send_event
import asyncio

router = APIRouter(prefix="/orders", tags=["orders"])

# ------------------------
# Create Order
# ------------------------
@router.post("/", response_model=OrderResponse)
def create_order(
    order: OrderCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = OrdersRepository(db)
    
    # Use current_user.id instead of trusting client input
    db_order = Order(**order.dict(exclude={"user_id"}), user_id=current_user.id)
    
    order_created = repo.create_order(db_order)

    # Kafka event
    asyncio.create_task(
        send_event(
            "orders",
            {
                "action": "created",
                "order_id": order_created.id,
                "user_id": order_created.user_id,
                "total": getattr(order_created, "total", None),
                "items": getattr(order_created, "items", [])
            }
        )
    )
    return order_created

# ------------------------
# Get All Orders (Admin Only)
# ------------------------
@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    repo = OrdersRepository(db)
    return repo.get_all_orders()

# ------------------------
# Get Single Order
# ------------------------
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = OrdersRepository(db)
    order = repo.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return order

# ------------------------
# Update Order
# ------------------------
@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = OrdersRepository(db)
    updated_order = repo.update_order(order_id, order_update)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    if updated_order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Kafka event
    asyncio.create_task(
        send_event(
            "orders",
            {
                "action": "updated",
                "order_id": updated_order.id,
                "user_id": updated_order.user_id,
                "total": getattr(updated_order, "total", None),
                "items": getattr(updated_order, "items", [])
            }
        )
    )

    return updated_order

# ------------------------
# Delete Order
# ------------------------
@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = OrdersRepository(db)
    order = repo.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    repo.delete_order(order)

    # Kafka event
    asyncio.create_task(
        send_event(
            "orders",
            {
                "action": "deleted",
                "order_id": order.id,
                "user_id": order.user_id
            }
        )
    )

    return {"detail": f"Order with id {order_id} successfully deleted"}