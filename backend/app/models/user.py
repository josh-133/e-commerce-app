from sqlalchemy import Column, Integer, String
from app.models.role import Role
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, default=Role.USER.value)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)