# init_db.py
from .database import engine, Base
from .models.user import User
from .models.product import Product
from .models.order import Order
from .models.cart import Cart
from .models.cart_item import CartItem

Base.metadata.create_all(bind=engine)
print("Tables created successfully.")