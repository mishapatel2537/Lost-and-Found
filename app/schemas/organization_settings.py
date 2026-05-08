from pydantic import BaseModel

class OrganizationSettingsOut(BaseModel):
    require_proof: bool
    max_claims_per_item: int
    enable_matching: bool

    class Config:
        from_attributes = True
