from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClaimCreate(BaseModel):
    item_id: int
    proof: Optional[str] = None

class ClaimUpdate(BaseModel):
    status: str  # accepted / rejected

class ClaimOut(BaseModel):
    id: int
    item_id: int
    user_id: int
    proof: Optional[str]
    status: str

    class Config:
        from_attributes = True