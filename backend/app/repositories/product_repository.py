from sqlalchemy.orm import Session
from app.models.product import Product

class ProductsRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product: Product):
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def get_product(self, product_id: int):
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def get_all_products(self):
        return self.db.query(Product).all()
    
    def update_product(self, product_id: int, product_update):
        product = self.get_product(product_id)
        if not product:
            return None
        for field, value in product_update.dict(exclude_unset=True).items():
            setattr(product, field, value)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def delete_product(self, product: Product):
        self.db.delete(product)
        self.db.commit()
        return product