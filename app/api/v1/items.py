from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.item import ItemCreate, ItemResponse
from app.services.item_service import create_item, get_items, get_item_by_id
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/lost", response_model=ItemResponse)
def report_lost_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_item(db, item, user_id=current_user.id, status="lost")

@router.post("/found", response_model=ItemResponse)
def report_found_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_item(db, item, user_id=current_user.id, status="found")

@router.get("/", response_model=list[ItemResponse])
def list_items(
    skip: int=0,
    limit: int=10,
    status: str | None = None,
    search: str | None = None,
    category: str | None = None,
    location: str | None = None,
    db: Session = Depends(get_db)):
    return get_items(db, skip, limit, status, search, category, location)

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    return get_item_by_id(db, item_id)