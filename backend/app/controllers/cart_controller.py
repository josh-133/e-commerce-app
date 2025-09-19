from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.cart import CartResponse, CartCreate, CartItem as CartItemSchema
from app.models.cart_item import CartItem
from app.repositories.cart_repository import CartsRepository
from app.dependencies.auth_dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/cart", tags=["Cart"])

# Create empty cart
@router.post("/", response_model=CartResponse)
def create_cart(cart_create: CartCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = CartsRepository(db)
    cart = repo.create_cart(user_id=cart_create.user_id)
    if cart.user_id != current_user.id:  # enforce ownership
        raise HTTPException(status_code=403, detail="Not authorized")
    return cart

@router.get("/", response_model=list[CartResponse])
def get_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = CartsRepository(db)
    carts = repo.get_all_carts()
    if not carts:
        raise HTTPException(status_code=404, detail="No carts were found")
    if current_user.role != "admin":  # enforce ownership
        raise HTTPException(status_code=403, detail="Not authorized")
    return carts


@router.get("/{cart_id}", response_model=CartResponse)
def get_cart(cart_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = CartsRepository(db)
    cart = repo.get_cart(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="No carts were found")
    if cart.user_id != current_user.id:  # enforce ownership
        raise HTTPException(status_code=403, detail="Not authorized")
    return cart

# Add item to cart
@router.post("/{cart_id}/items", response_model=CartItemSchema)
def add_item_to_cart(cart_id: int, item: CartItemSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = CartsRepository(db)
    cart = repo.get_cart(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_item = repo.add_item(cart, item)
    return cart_item

# Remove item from cart
@router.delete("/{cart_id}/items/{item_id}")
def remove_item_from_cart(cart_id: int, item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = CartsRepository(db)
    cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    repo.remove_item(cart_item)
    return {"detail": "Item removed"}

# Update item quantity
@router.put("/{cart_id}/items/{item_id}", response_model=CartItemSchema)
def update_cart_item(cart_id: int, item_id: int, quantity: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = CartsRepository(db)
    cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    updated_item = repo.update_item(cart_item, quantity)
    return updated_item