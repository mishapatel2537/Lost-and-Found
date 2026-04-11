from sqlalchemy.orm import Session
from app.models.claim import Claim
from app.models.item import Item

MAX_CLAIMS_PER_ITEM = 5

def create_claim(db: Session, user, data, org):

    item = db.query(Item).filter(
        Item.id == data.item_id,
        Item.organization_id == user.organization_id
    ).first()

    if not item:
        raise Exception("Item not found")
    
    if item.owner_id == user.id:
        raise Exception("Cannot claim your own item")
    
    claim_count = db.query(Claim).filter(
        Claim.item_id == item.id
    ).count()

    if claim_count >= MAX_CLAIMS_PER_ITEM:
        raise Exception("Max claims reached")
    
    accepted = db.query(Claim).filter(
        Claim.item_id == item.id,
        Claim.status == "accepted"
    ).first()

    if accepted:
        raise Exception("Item already claimed")
    
    if org.require_proof:
        if not data.proof:
            raise Exception("Proof required")

    claim = Claim(
        item_id=item.id,
        user_id=user.id,
        proof=data.proof
    )

    db.add(claim)
    db.commit()
    db.refresh(claim)

    return claim


def update_claim_status(db: Session, user, claim_id: int, status: str):

    claim = db.query(Claim).filter(Claim.id == claim_id).first()

    if not claim:
        raise Exception("Claim not found")

    item = db.query(Item).filter(Item.id == claim.item_id).first()

    if item.owner_id != user.id:
        raise Exception("Not allowed")

    if status not in ["accepted", "rejected"]:
        raise Exception("Invalid status")

    if status == "accepted":
        existing = db.query(Claim).filter(
            Claim.item_id == item.id,
            Claim.status == "accepted"
        ).first()

        if existing:
            raise Exception("Already accepted claim exists")

        item.status = "claimed"

    claim.status = status

    db.commit()
    db.refresh(claim)

    return claim


def get_claims_for_item(db: Session, item_id: int):
    return db.query(Claim).filter(Claim.item_id == item_id).all()