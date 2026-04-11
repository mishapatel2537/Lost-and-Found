from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.claim import ClaimCreate, ClaimUpdate
from app.services.claim_service import (
    create_claim,
    update_claim_status,
    get_claims_for_item
)

router = APIRouter(prefix="/claims", tags=["Claims"])


@router.post("/")
def create(
    data: ClaimCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    org = user.organization  # assuming relationship exists
    return create_claim(db, user, data, org)


@router.patch("/{claim_id}")
def update(
    claim_id: int,
    data: ClaimUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return update_claim_status(db, user, claim_id, data.status)


@router.get("/item/{item_id}")
def history(
    item_id: int,
    db: Session = Depends(get_db)
):
    return get_claims_for_item(db, item_id)