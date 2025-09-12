from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.user_repository import UsersRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.utils.auth import hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    role = user.role if user.role else "user"
    db_user = User(
        email=user.email, 
        hashed_password=hashed_password, 
        role=role
        )
    return UsersRepository(db).create_user(db_user)

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return UsersRepository(db).get_all_users()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UsersRepository(db).get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    updated_user = UsersRepository(db).update_user(user_id, user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = UsersRepository(db).get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    UsersRepository(db).delete_user(user)
    return f"User with an id of {user_id} was successfully deleted"