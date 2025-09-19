from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=True)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    image_url = Column(String)
    category = Column(String, nullable=False)
    stock = Column(Integer, default=0)