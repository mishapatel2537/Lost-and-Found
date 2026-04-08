from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, index=True)
    description = Column(Text)

    category = Column(String, index=True)
    location = Column(String, index=True)

    type = Column(String, nullable=False, index=True)    # lost / found
    status = Column(String, nullable=False, index=True)  # open / claimed / returned

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", backref="items")

    organization_id = Column(Integer, ForeignKey("organizations.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())