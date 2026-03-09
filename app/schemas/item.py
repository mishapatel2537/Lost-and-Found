from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    title: str
    location: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    status: str
    owner_id: int

    class Config:
        from_attributes = True
