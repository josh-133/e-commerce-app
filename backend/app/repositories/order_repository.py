from sqlalchemy.orm import Session
from app.models.order import Order

class OrdersRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: Order):
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_order(self, order_id: int):
        return self.db.query(Order).filter(Order.id == order_id).first()

    def get_all_orders(self):
        return self.db.query(Order).all()