from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    location: Optional[str]
    description: Optional[str]
    category: Optional[str] 
    type: str

class ItemUpdateStatus(BaseModel):
    status: str


class ItemOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: Optional[str]
    location: Optional[str]
    type: str
    status: str
    image_url: Optional[str]

    class Config:
        from_attributes = True
