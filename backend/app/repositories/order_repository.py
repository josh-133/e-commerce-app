from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.order import Order
from app.models.product import Product

class OrdersRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: Order):
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        
            
        for item in order.cart_items:
            product = self.db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                product.stock -= item.quantity  # <-- update stock
                self.db.commit()
            item.order_id = order.id
            self.db.add(item)

        self.db.commit()
        return order

    def get_order(self, order_id: int):
        return self.db.query(Order).filter(Order.id == order_id).first()

    def get_all_orders(self):
        return self.db.query(Order).all()
    
    def update_order(self, order_id: int, order_update):
        order = self.get_order(order_id)
        if not order:
            return None
        for field, value in order_update.dict(exclude_unset=True).items():
            setattr(order, field, value)
        self.db.commit()
        self.db.refresh(order)
        return order

    def update_status(self, order: Order, status: str):
        order.status = status
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def delete_order(self, order: Order):
        self.db.delete(order)
        self.db.commit()
        return order