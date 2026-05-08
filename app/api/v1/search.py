from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.services.matching_service import get_matches_for_item

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/matches/{item_id}")
def find_matches(item_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_matches_for_item(db, item_id, user)