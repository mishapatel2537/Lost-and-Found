from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.organization import OrganizationCreate
from app.services.organization_service import create_organization

router = APIRouter(prefix="/organizations", tags=["Organizations"])

@router.post("/")
def create_org(data: OrganizationCreate, db: Session = Depends(get_db)):
    return create_organization(db, data.name)
