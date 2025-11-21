from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.product import Product
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.order import Order
from app.utils.auth import hash_password

# Drop all tables and create fresh ones (optional)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # --- Seed Users ---
    users = [
        {"email": "admin@example.com", "password": "admin123", "role": "admin"},
        {"email": "user1@example.com", "password": "user123", "role": "user"},
        {"email": "user2@example.com", "password": "user123", "role": "user"},
    ]

    user_objects = []
    for u in users:
        hashed_pw = hash_password(u["password"])
        user_obj = User(email=u["email"], hashed_password=hashed_pw, role=u["role"])
        db.add(user_obj)
        user_objects.append(user_obj)
    db.commit()
    print("Users seeded!")

    # --- Seed Products ---
    products = [
        {"name": "Wireless Headphones", "description": "Over-ear, noise-cancelling", "price": 99.99, "image_url": "https://images.unsplash.com/photo-1657223143975-d29d7959a70f?q=80&w=1625&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", "category": "Electronics", "stock": 50},
        {"name": "Smartphone Stand", "description": "Adjustable desktop stand", "price": 14.95, "image_url": "https://images.unsplash.com/photo-1669255344177-dc55f537acc9?q=80&w=654&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", "category": "Electronics", "stock": 200},
        {"name": "Yoga Mat", "description": "Eco-friendly non-slip mat", "price": 29.99, "image_url": "https://plus.unsplash.com/premium_photo-1675155952889-abb299df1fe7?q=80&w=2058&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", "category": "Sports", "stock": 80},
        {"name": "Coffee Mug", "description": "12oz ceramic mug", "price": 9.99, "image_url": "https://images.unsplash.com/photo-1616241673111-508b4662c707?q=80&w=1004&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", "category": "Home & Kitchen", "stock": 100},
    ]

    product_objects = []
    for p in products:
        product_obj = Product(**p)
        db.add(product_obj)
        product_objects.append(product_obj)
    db.commit()
    print("Products seeded!")

    # --- Seed Carts & Cart Items ---
    cart1 = Cart(user_id=user_objects[1].id)
    db.add(cart1)
    db.commit()

    cart_items = [
        CartItem(cart_id=cart1.id, product_id=product_objects[0].id, quantity=1, price_at_time=product_objects[0].price),
        CartItem(cart_id=cart1.id, product_id=product_objects[1].id, quantity=2, price_at_time=product_objects[1].price),
    ]
    db.add_all(cart_items)
    db.commit()
    print("Carts and cart items seeded!")

    # --- Seed Orders ---
    order1 = Order(user_id=user_objects[1].id, quantity=len(cart_items),  total_price=sum([ci.quantity*ci.price_at_time for ci in cart_items]))
    db.add(order1)
    db.commit()
    print("Orders seeded!")

except Exception as e:
    db.rollback()
    print(f"Error seeding database: {e}")
finally:
    db.close()