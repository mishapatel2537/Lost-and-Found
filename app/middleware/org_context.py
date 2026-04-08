from fastapi import Request
from app.services.organization_service import get_org_settings
from app.db.session import SessionLocal

async def org_context_middleware(request: Request, call_next):
    db = SessionLocal()

    user = getattr(request.state, "user", None)

    if user:
        settings = get_org_settings(db, user.organization_id)
        request.state.org_settings = settings

    response = await call_next(request)
    return response