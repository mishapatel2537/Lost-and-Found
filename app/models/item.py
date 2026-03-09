from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False, index=True)
    description = Column(Text)

    category = Column(String, index=True)
    location = Column(String, index=True)

    status = Column(String, nullable=False, index=True)  # "lost" or "found"

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User")
    created_at = Column(DateTime(timezone=True), server_default=func.now())