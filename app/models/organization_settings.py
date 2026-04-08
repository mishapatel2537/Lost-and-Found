from sqlalchemy import Column, Integer, Boolean, ForeignKey
from app.db.base import Base

class OrganizationSettings(Base):
    __tablename__ = "organization_settings"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    require_proof = Column(Boolean, default=True)
    max_claims_per_item = Column(Integer, default=3)
    enable_chat = Column(Boolean, default=True)
    enable_mathcing = Column(Boolean, default=True)