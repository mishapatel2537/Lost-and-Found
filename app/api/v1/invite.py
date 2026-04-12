from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.invite_service import create_invite_code

router = APIRouter(prefix="/invite", tags=["Invite"])

@router.post("/invite-codes")
def generate_code(organization_id: int, db: Session = Depends(get_db)):
    try:
        return create_invite_code(db, organization_id)
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))
