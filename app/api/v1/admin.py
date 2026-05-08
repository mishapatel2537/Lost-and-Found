from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.item import Item

router = APIRouter(prefix="/admin", tags=["Admin"])

def require_admin(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.get("/users")
def list_users(db: Session = Depends(get_db), user=Depends(require_admin)):
    return db.query(User).all()

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(target)
    db.commit()
    return {"message": "User deleted"}

@router.get("/items")
def list_all_items(db: Session = Depends(get_db), user=Depends(require_admin)):
    return db.query(Item).all()

@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted"}