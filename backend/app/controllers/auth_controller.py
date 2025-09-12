from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.utils.auth import verify_password, create_access_token
from app.utils.auth import hash_password
from app.repositories.user_repository import UsersRepository
from app.models.user import User
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    repo = UsersRepository(db)
    if repo.get_by_email(user.email):
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = hash_password(user.password)
    db_user = User(
        email=user.email, 
        hashed_password=hashed, 
        role="user"
        )
    new_user = repo.create_user(db_user)
    return {"id": new_user.id, "email": new_user.email}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    repo = UsersRepository(db)
    db_user = repo.get_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}