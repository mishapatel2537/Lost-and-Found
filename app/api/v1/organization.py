from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.organization import OrganizationCreate, OrganizationOut
from app.schemas.organization_settings import OrganizationSettingsOut
from app.services.organization_service import create_organization, get_org_settings

router = APIRouter(prefix="/organizations", tags=["Organizations"])

@router.post("/", response_model=OrganizationOut)
def create_org(data: OrganizationCreate, db: Session = Depends(get_db)):
    try:
        return create_organization(db, data.name)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.get("/my/settings", response_model=OrganizationSettingsOut)
def my_org_settings(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user.organization_id:
        raise HTTPException(status_code=404, detail="You are not part of any organization")
    settings = get_org_settings(db, user.organization_id)
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    return settings
