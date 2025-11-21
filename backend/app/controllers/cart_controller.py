from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.cart import CartResponse, CartItem as CartItemSchema, CartUpdate
from app.models.user import User
from app.dependencies.auth_dependencies import get_current_user
from app.kafka.producer import producer, delivery_report
from app.repositories.cart_repository import CartsRepository
import datetime, json, uuid

router = APIRouter(prefix="/cart", tags=["Cart"])


# ------------------------
# Get current user's cart
# ------------------------
@router.get("/current", response_model=CartResponse)
def get_current_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Synchronous call to fetch the current cart for a user.
    """
    from app.repositories.cart_repository import CartsRepository

    repo = CartsRepository(db)
    cart = repo.get_by_user_id(current_user.id)
    if not cart:
        cart = repo.create_cart(current_user.id)
    return cart


# ------------------------
# Add item to cart
# ------------------------
@router.post("/current/items", response_model=CartItemSchema)
def add_item_to_cart(item: CartItemSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = CartsRepository(db)
    repo.validate_stock(item) # raises HTTP Exception if invalid
    
    # Kafka event
    event = {
        "event_id": str(uuid.uuid4()),
        "service": "cart_service",
        "event_type": "cart.item_added",
        "version": 1,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "data": {
            "user_id": current_user.id,
            **item.dict()
        }
    }

    producer.produce(
        topic="cart_events",
        value=json.dumps(event).encode("utf-8"),
        callback=delivery_report
    )
    producer.flush()
    return item  # return the requested payload immediately


# ------------------------
# Remove item from cart
# ------------------------
@router.delete("/current/items/{item_id}", response_model=dict)
def remove_item_from_cart(item_id: int, current_user: User = Depends(get_current_user)):
    event = {
        "event_id": str(uuid.uuid4()),
        "service": "cart_service",
        "event_type": "cart.item_removed",
        "version": 1,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "data": {
            "user_id": current_user.id,
            "product_id": item_id  # just the product_id is enough
        }
    }

    producer.produce(
        topic="cart_events",
        value=json.dumps(event).encode("utf-8"),
        callback=delivery_report
    )
    producer.flush()
    return {"status": "event emitted", "product_id": item_id}

@router.delete("/current/{cart_id}/clear")
def clear_cart(cart_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    repo = CartsRepository(db)
    cart = repo.get_by_user_id(current_user.id)
    if not cart or cart.id != cart_id:
        raise HTTPException(status_code=404, detail="Cart not found")
    repo.clear_items(cart)
    db.refresh(cart)
    return cart


# ------------------------
# Update item quantity
# ------------------------
@router.put("/current/items/{item_id}", response_model=dict)
def update_cart_item(item_id: int, item_update: CartUpdate, current_user: User = Depends(get_current_user)):
    event = {
        "event_id": str(uuid.uuid4()),
        "service": "cart_service",
        "event_type": "cart.item_updated",
        "version": 1,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "data": {
            "user_id": current_user.id,
            "product_id": item_id,
            "quantity": item_update.quantity
        }
    }

    producer.produce(
        topic="cart_events",
        value=json.dumps(event).encode("utf-8"),
        callback=delivery_report
    )
    producer.flush()
    return {"status": "event emitted", "product_id": item_id, "quantity": item_update.quantity}