from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.order_repository import OrdersRepository
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.dependencies.auth_dependencies import get_current_user
from app.models.user import User
from app.kafka.producer import producer, delivery_report
import uuid
import datetime
import json

router = APIRouter(prefix="/orders", tags=["orders"])

# ------------------------
# Create Order
# ------------------------
@router.post("", response_model=dict)
def create_order(
    order: OrderCreate,
    current_user: User = Depends(get_current_user)
):
    event = {
        "event_id": str(uuid.uuid4()),
        "service": "order_service",
        "event_type": "order.created",
        "version": 1,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "data": {
            "user_id": current_user.id,
            **order.dict()
        }
    }

    producer.produce(
        topic="order_events",
        value=json.dumps(event).encode("utf-8"),
        callback=delivery_report
    )
    producer.flush()

    return {"status": "ORDER_EVENT_SENT"}

# ------------------------
# Get All Orders (Admin Only)
# ------------------------
@router.get("", response_model=list[OrderResponse])
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
def update_order(
    order_id: int,
    order_update: OrderUpdate,
    current_user: User = Depends(get_current_user)
):
    event = {
        "event_id": str(uuid.uuid4()),
        "service": "order_service",
        "event_type": "order.updated",
        "version": 1,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "data": {
            "order_id": order_id,
            "user_id": current_user.id,
            **order_update.dict()
        }
    }

    producer.produce(
        topic="order_events",
        value=json.dumps(event).encode("utf-8"),
        callback=delivery_report
    )
    producer.flush()

    return order_update

# ------------------------
# Delete Order
# ------------------------
@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    current_user: User = Depends(get_current_user)
):
    event = {
        "event_id": str(uuid.uuid4()),
        "service": "order_service",
        "event_type": "order.deleted",
        "version": 1,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "data": {
            "order_id": order_id,
            "user_id": current_user.id
        }
    }

    producer.produce(
        topic="order_events",
        value=json.dumps(event).encode("utf-8"),
        callback=delivery_report
    )
    producer.flush()

    return {"detail": f"Order {order_id} delete event sent"}