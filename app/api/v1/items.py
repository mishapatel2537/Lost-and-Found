from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user

from app.schemas.item import ItemCreate, ItemUpdateStatus
from app.services.item_service import (
    create_item,
    get_items,
    get_item_by_id,
    update_item_status
)

from app.utils.file_upload import save_file

router = APIRouter(prefix="/items", tags=["Items"])


# CREATE ITEM (NO IMAGE)
@router.post("/")
def create_new_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return create_item(db, item, user)


# CREATE ITEM WITH IMAGE
@router.post("/upload")
def create_item_with_image(
    item: ItemCreate = Depends(),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    image_url = save_file(file)
    return create_item(db, item, user, image_url)


@router.get("/")
def list_items(
    type: str = None,
    search: str = None,
    category: str = None,
    location: str = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return get_items(
        db=db,
        user=user,
        skip=skip,
        limit=limit,
        type=type,
        search=search,
        category=category,
        location=location
    )


@router.get("/{item_id}")
def get_single_item(
    item_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return get_item_by_id(db, user, item_id)


@router.patch("/{item_id}/status")
def update_status(
    item_id: int,
    data: ItemUpdateStatus,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return update_item_status(db, user, item_id, data.status)