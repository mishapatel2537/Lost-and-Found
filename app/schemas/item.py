from fastapi import Form
from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    location: Optional[str]
    description: Optional[str]
    category: Optional[str] 
    type: str

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        location: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        category: Optional[str] = Form(None),
        type: str = Form(...),
    ):
        return cls(
            name=name,
            location=location,
            description=description,
            category=category,
            type=type,
        )

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
