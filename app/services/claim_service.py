from sqlalchemy.orm import Session
from app.models.claim import Claim
from app.models.item import Item
from app.services.notification_service import create_notification

def create_claim(db: Session, user, data, org):
    item = db.query(Item).filter(
        Item.id == data.item_id,
        Item.organization_id == user.organization_id
    ).first()

    if not item:
        raise Exception("Item not found")
    if item.owner_id == user.id:
        raise Exception("Cannot claim your own item")
    if item.status != "open":
        raise Exception("Only open items can be claimed")

    existing_claim = db.query(Claim).filter(
        Claim.item_id == item.id,
        Claim.user_id == user.id
    ).first()
    if existing_claim:
        raise Exception("You have already submitted a claim for this item")

    max_claims = org.max_claims_per_item or 3
    claim_count = db.query(Claim).filter(Claim.item_id == item.id).count()
    if claim_count >= max_claims:
        raise Exception("Max claims reached")

    accepted = db.query(Claim).filter(
        Claim.item_id == item.id, Claim.status == "accepted"
    ).first()
    if accepted:
        raise Exception("Item already claimed")

    if org.require_proof and not data.proof:
        raise Exception("Proof required by your organization")

    claim = Claim(item_id=item.id, user_id=user.id, proof=data.proof)
    db.add(claim)
    db.commit()
    db.refresh(claim)

    # Notify item owner
    create_notification(db, item.owner_id,
        f"Someone claimed your item: {item.name}")

    return claim


def update_claim_status(db: Session, user, claim_id: int, status: str):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise Exception("Claim not found")

    item = db.query(Item).filter(Item.id == claim.item_id).first()
    if not item:
        raise Exception("Item not found")
    if item.owner_id != user.id:
        raise Exception("Not allowed")

    if status not in ["accepted", "rejected"]:
        raise Exception("Invalid status")
    if claim.status != "pending":
        raise Exception("Only pending claims can be updated")

    if status == "accepted":
        existing = db.query(Claim).filter(
            Claim.item_id == item.id,
            Claim.status == "accepted",
            Claim.id != claim.id
        ).first()
        if existing:
            raise Exception("Already accepted claim exists")
        item.status = "claimed"

    claim.status = status
    db.commit()
    db.refresh(claim)

    # Notify the claimant
    create_notification(db, claim.user_id,
        f"Your claim on '{item.name}' was {status}.")

    return claim


def get_claims_for_item(db: Session, item_id: int, user):
    item = db.query(Item).filter(
        Item.id == item_id,
        Item.organization_id == user.organization_id
    ).first()
    if not item:
        raise Exception("Item not found")

    if item.owner_id != user.id:
        raise Exception("Not allowed")

    return db.query(Claim).filter(Claim.item_id == item_id).all()
