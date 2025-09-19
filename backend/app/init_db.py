from app.database import engine, Base, SessionLocal
from app.models.product import Product
from app.models.user import User
from app.models.order import Order  # if you have it
from app.models.cart import Cart     # if you have it
from app.models.cart_item import CartItem  # if you have it

def init_db():
    # Create tables in PostgreSQL
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    init_db()