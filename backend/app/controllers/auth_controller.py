from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserRegister, UserLogin, UserResponse
from app.services.auth_service import AuthService
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()

@router.post("/register")
async def register(request: UserRegister, db: Session = Depends(get_db)):
    return await auth_service.register(db, request.email, request.password)

@router.post("/login")
async def login(request: UserLogin, db: Session = Depends(get_db)):
    return await auth_service.login(db, request.email, request.password)