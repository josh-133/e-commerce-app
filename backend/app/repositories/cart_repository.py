from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.schemas.cart import CartCreate, CartItem as CartItemSchema

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
    
    # Add item to cart
    def add_item(self, cart: Cart, item: CartItemSchema) -> CartItem:
        cart_item = CartItem(
            cart_id=cart.id,
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