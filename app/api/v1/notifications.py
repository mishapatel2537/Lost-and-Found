from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.services.notification_service import get_notifications, mark_all_read

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/")
def list_notifications(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_notifications(db, user.id)

@router.patch("/read-all")
def read_all(db: Session = Depends(get_db), user=Depends(get_current_user)):
    mark_all_read(db, user.id)
    return {"message": "All notifications marked as read"}