from pydantic import BaseModel

class OrganizationSettingsOut(BaseModel):
    require_proof: bool
    max_claims_per_item: int
    enable_chat: bool
    enable_matching: bool

    class Congig:
        from_attributes = True 