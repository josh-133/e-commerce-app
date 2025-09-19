from sqlalchemy.orm import Session
from app.models.user import User

class UsersRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all_users(self):
        return self.db.query(User).all()
    
    def get_user(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
    
    def update_user(self, user_id: int, user_update):
        user = self.get_user(user_id)
        if not user:
            return None
        for field, value in user_update.dict(exclude_unset=True).items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(self, user: User):
        self.db.delete(user)
        self.db.commit()
        return user