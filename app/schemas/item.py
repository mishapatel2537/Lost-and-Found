from pydantic import BaseModel

class LostItem(BaseModel):
    item_name: str
    location: str
    description: str

class FoundItem(BaseModel):
    item_name: str
    location: str
    description: str
