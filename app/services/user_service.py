from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password

def create_user(db: Session, user: UserCreate):

    hashed_pw = hash_password(user.password)

    db_user = User(
        email = user.email,
        username = user.username,
        hashed_password = hashed_pw
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def authenticate_user(db: Session, email:str, password:str):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user