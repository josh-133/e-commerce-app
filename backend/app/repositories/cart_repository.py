from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.schemas.cart import CartItem as CartItemSchema

import logging
class CartsRepository:

    def __init__(self, db: Session):
        self.db = db

    # Create empty cart
    def create_cart(self, user_id: int, status: str = "active") -> Cart:
        cart = Cart(user_id=user_id, status=status)
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart

    def get_all_carts(self):
        return self.db.query(Cart).all()
    
    def get_cart(self, cart_id: int) -> Cart | None:
        return self.db.query(Cart).filter(Cart.id == cart_id).first()
    
    def get_by_user_id(self, user_id: int) -> Cart | None:
        return self.db.query(Cart).filter(Cart.user_id == user_id).first()
    
    def validate_stock(self, item: CartItemSchema):
        product = self.db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # You also want to consider quantity already in cart
        existing_cart_item = self.db.query(CartItem).filter(
            CartItem.product_id == item.product_id
        ).first()
        existing_qty = existing_cart_item.quantity if existing_cart_item else 0

        if item.quantity + existing_qty > product.stock:
            raise HTTPException(
                status_code=400,
                detail=f"Only {product.stock} left in stock"
        )
    
    # Add item to cart
    def add_item(self, cart: Cart, item: CartItemSchema) -> CartItem:
        # 1. Fetch product from DB
        product = (
            self.db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # 2. Check if the item is already in the cart
        cart_item = (
            self.db.query(CartItem)
            .filter(CartItem.cart_id == cart.id, CartItem.product_id == item.product_id)
            .first()
        )
                
        existing_quantity = cart_item.quantity if cart_item else 0
        new_total_quantity = existing_quantity + item.quantity
        
        # 3. Check stock
        if new_total_quantity > product.stock:
            raise HTTPException(
            status_code=400,
            detail=f"Only {product.stock} in stock"
        )
        
        if cart_item:
            # If it exists, increase the quantity
            cart_item.quantity = new_total_quantity
        else:
            # If not, create a new CartItem
            cart_item = CartItem(
                cart_id=cart.id,
                name=item.name,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_time=item.price_at_time
            )
            self.db.add(cart_item)
        
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item

    # Remove item
    def remove_item(self, cart_item: CartItem):
        self.db.delete(cart_item)
        self.db.commit()

    # Update cart item
    def update_item(self, cart_item: CartItem, quantity: int):
        cart_item.quantity = quantity
        self.db.commit()
        self.db.refresh(cart_item)
        return cart_item
    
    def update_cart(self, cart_id: int, cart_update):
        cart = self.get_cart(cart_id)
        if not cart:
            return None
        for field, value in cart_update.dict(exclude_unset=True).items():
            setattr(cart, field, value)
        self.db.commit()
        self.db.refresh(cart)
        return cart
    
    def delete_cart(self, cart: Cart):
        self.db.delete(cart)
        self.db.commit()
        return cart
    
    def clear_items(self, cart: Cart):
        # Delete all cart items for this cart
        self.db.query(CartItem).filter(CartItem.cart_id == cart.id).delete(synchronize_session=False)
        self.db.commit()