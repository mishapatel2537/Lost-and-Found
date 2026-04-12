from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password
from app.models.organization import Organization
from app.services.invite_service import validate_invite_code

def create_user(db: Session, user: UserCreate):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise Exception("User already exists")

    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise Exception("Username already exists")
    
    invite = validate_invite_code(db, user.invite_code)

    hashed_pw = hash_password(user.password)

    db_user = User(
        email = user.email,
        username = user.username,
        hashed_password = hashed_pw,
        organization_id = invite.organization_id
    )

    db.add(db_user)

    invite.used_count += 1

    db.commit()
    db.refresh(db_user)

    return db_user

def authenticate_user(db: Session, email:str, password:str):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise  Exception("Invalid User")
    
    if not verify_password(password, user.hashed_password):
        raise Exception("Invalid password")
    
    return user
