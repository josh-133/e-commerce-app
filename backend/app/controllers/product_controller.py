from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.product_repository import ProductsRepository
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.dependencies.auth_dependencies import get_current_user
from app.models.user import User
import logging

# Create a logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)  # or INFO in production

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = ProductsRepository(db)
    db_product = Product(**product.dict(), user_id=current_user.id)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return repo.create_product(db_product)

@router.get("", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    repo = ProductsRepository(db)
    return repo.get_all_products()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    repo = ProductsRepository(db)
    product = repo.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = ProductsRepository(db)
    updated_product = repo.update_product(product_id, product_update)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if updated_product.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return updated_product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = ProductsRepository(db)
    product = repo.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check for cart items
    cart_item_exists = db.query(CartItem).filter(CartItem.product_id == product.id).first()
    if cart_item_exists:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete product. It is still in users' carts."
        )
    if product.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    repo.delete_product(product)
    return f"Product with an id of {product_id} was successfully deleted"
        