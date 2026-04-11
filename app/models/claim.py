from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)

    item_id = Column(Integer, ForeignKey("items.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    proof = Column(String, nullable=True)

    status = Column(String, default="pending")   # pending / accepted / rejected

    item = relationship("Items")
    user = relationship("Users")