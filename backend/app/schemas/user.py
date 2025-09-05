from pydantic import BaseModel
from app.models.role import Role


class UserRegister(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    role: Role

    class Config:
        orm_mode = True
        