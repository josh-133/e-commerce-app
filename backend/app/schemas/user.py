from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.role import Role


class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Role = Role.USER


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[Role] = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: Role

    class Config:
        orm_mode = True