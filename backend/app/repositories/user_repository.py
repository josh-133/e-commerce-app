from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:

    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def create_user(db: Session, email: str, hashed_password: str) -> User:
        new_user = User(email=email, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user