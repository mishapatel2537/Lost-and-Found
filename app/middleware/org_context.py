from fastapi import Request
from app.core.security import decode_access_token
from app.models.user import User
from app.services.organization_service import get_org_settings
from app.db.session import SessionLocal

async def org_context_middleware(request: Request, call_next):
    db = SessionLocal()
    try:
        user = None
        auth_header = request.headers.get("Authorization", "")

        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1].strip()
            payload = decode_access_token(token)
            if payload:
                user_id = payload.get("user_id") or payload.get("sub")
                try:
                    user_id = int(user_id)
                except (TypeError, ValueError):
                    user_id = None

                if user_id is not None:
                    user = db.query(User).filter(User.id == user_id).first()
                    if user:
                        request.state.user = user

        if user:
            settings = get_org_settings(db, user.organization_id)
            request.state.org_settings = settings

        response = await call_next(request)
        return response
    finally:
        db.close()
