from sqlalchemy.orm import Session
from models.user import User, UserProfile

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_profile_by_user_id(db: Session, user_id: int):
    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()