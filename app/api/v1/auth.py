from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services.user_service import create_user, authenticate_user
from app.core.security import create_access_token
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db, user)
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))

    if not new_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return new_user

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(
        data={"sub": str(user.id), "user_id": user.id}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
