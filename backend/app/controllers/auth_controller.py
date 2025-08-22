from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.auth import hash_password, verify_password, create_access_token
from app.schemas.user import UserRegister, UserLogin, UserResponse
from app.services.auth_service import AuthService

# Fake DB for now
users_db = {}

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()

@router.post("/register")
async def register(user: UserRegister):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")    
    hashed = hash_password(user.password)
    users_db[user.email] = hashed

    return {"id": len(users_db), "email": user.email}

@router.post("/login")
async def login(username: str, password: str):
    return await auth_service.login(username, password)