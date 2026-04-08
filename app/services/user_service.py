from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password
from app.models.organization import Organization

def create_user(db: Session, user: UserCreate):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise Exception("User already exists")
    
    org = db.query(Organization).filter(
        Organization.invite_code == user.invite_code
    ).first()
    if not org:
        raise Exception("Invalid invite code")

    hashed_pw = hash_password(user.password)

    db_user = User(
        email = user.email,
        username = user.username,
        hashed_password = hashed_pw,
        organization_id = org.id
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