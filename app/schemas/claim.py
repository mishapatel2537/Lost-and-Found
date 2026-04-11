from pydantic import BaseModel

class ClaimCreate(BaseModel):
    item_id: int
    proof: str | None = None

class ClaimUpdate(BaseModel):
    status: str    # accepted / rejected