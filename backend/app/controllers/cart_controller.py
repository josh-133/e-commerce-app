from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.cart import CartResponse, CartCreate, CartItem as CartItemSchema, CartUpdate
from app.models.cart_item import CartItem
from app.repositories.cart_repository import CartsRepository
from app.dependencies.auth_dependencies import get_current_user
from app.models.user import User
from app.kafka.producer import producer, delivery_report
import json

router = APIRouter(prefix="/cart", tags=["Cart"])

# ------------------------
# Create cart for current user
# ------------------------
@router.post("/", response_model=CartResponse)
def create_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = CartsRepository(db)
    cart = repo.create_cart(user_id=current_user.id)
    return cart

# ------------------------
# Get all carts (admin only)
# ------------------------
@router.get("/", response_model=list[CartResponse])
def get_all_carts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    repo = CartsRepository(db)
    carts = repo.get_all_carts()
    return carts

# ------------------------
# Get current user's cart
# ------------------------
@router.get("/current", response_model=CartResponse)
def get_current_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
    cart = repo.get_by_user_id(current_user.id)
    if not cart:
        cart = repo.create_cart(current_user.id)
    cart_item = repo.add_item(cart, item)
    # publish Kafka event
    producer.produce(topic="cart_item_added", value=json.dumps({
        "cart_id": cart.id,
        "product_id": cart_item.product_id,
        "quantity": cart_item.quantity,
        "user_id": current_user.id
    }).encode("utf-8"), callback=delivery_report)
    producer.flush()
    return cart_item

# ------------------------
# Remove item from cart
# ------------------------
@router.delete("/current/items/{item_id}", response_model=CartResponse)
def remove_item_from_cart(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = CartsRepository(db)
    cart = repo.get_by_user_id(current_user.id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    repo.remove_item(cart_item)
    # publish Kafka event
    producer.produce(topic="cart_item_removed", value=json.dumps({
        "cart_id": cart.id,
        "product_id": cart_item.product_id,
        "quantity": cart_item.quantity,
        "user_id": current_user.id
    }).encode("utf-8"), callback=delivery_report)
    producer.flush()
    updated_cart = repo.get_by_user_id(current_user.id)
    return updated_cart

# ------------------------
# Update item quantity
# ------------------------
@router.put("/current/items/{item_id}", response_model=CartItemSchema)
def update_cart_item(item_id: int, item_update: CartUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = CartsRepository(db)
    cart = repo.get_by_user_id(current_user.id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    updated_item = repo.update_item(cart_item, item_update.quantity)
    # publish Kafka event
    producer.produce(topic="cart_item_updated", value=json.dumps({
        "cart_id": cart.id,
        "product_id": updated_item.product_id,
        "quantity": updated_item.quantity,
        "user_id": current_user.id
    }).encode("utf-8"), callback=delivery_report)
    producer.flush()
    return updated_item