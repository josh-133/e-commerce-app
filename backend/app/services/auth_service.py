from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.utils.auth import hash_password, verify_password, create_access_token
from app.repositories.user_repository import UserRepository


class AuthService:
    async def login(self, db: Session, email: str, password: str):
        user = UserRepository.get_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}

    async def register(self, db: Session, email: str, password: str):
        existing_user = UserRepository.get_by_email(db, email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        hashed = hash_password(password)
        new_user = UserRepository.create_user(db, email, hashed)
        return {"id": new_user.id, "email": new_user.email}