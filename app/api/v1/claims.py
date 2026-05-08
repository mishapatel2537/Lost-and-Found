from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.claim import ClaimCreate, ClaimUpdate
from app.services.claim_service import create_claim, update_claim_status, get_claims_for_item
from app.services.organization_service import get_org_settings

router = APIRouter(prefix="/claims", tags=["Claims"])


@router.post("/")
def create(
    data: ClaimCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    org_settings = get_org_settings(db, user.organization_id)
    if not org_settings:
        raise HTTPException(status_code=400, detail="Organization settings not found")
    try:
        return create_claim(db, user, data, org_settings)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.patch("/{claim_id}")
def update(
    claim_id: int,
    data: ClaimUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return update_claim_status(db, user, claim_id, data.status)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/item/{item_id}")
def history(
    item_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return get_claims_for_item(db, item_id, user)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
