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
    
    def update_order(self, order_id: int, order_update):
        order = self.get_order(order_id)
        if not order:
            return None
        for field, value in order_update.dict(exclude_unset=True).items():
            setattr(order, field, value)
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def delete_order(self, order: Order):
        self.db.delete(order)
        self.db.commit()
        return order