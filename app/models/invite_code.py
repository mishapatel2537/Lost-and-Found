from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from datetime import datetime, timedelta
from app.db.base import Base

class InviteCode(Base):
    __tablename__ = "invite_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)

    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    max_uses = Column(Integer, default=5, nullable=False)
    used_count = Column(Integer, default=0, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=1), nullable=False)
