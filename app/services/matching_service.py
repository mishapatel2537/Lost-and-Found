from sqlalchemy.orm import Session
from app.models.item import Item

def score_match(lost: Item, found: Item) -> int:
    score = 0
    if lost.name.lower() in found.name.lower() or found.name.lower() in lost.name.lower():
        score += 40
    if lost.category and lost.category == found.category:
        score += 30
    if lost.location and found.location:
        if lost.location.lower() in found.location.lower() or found.location.lower() in lost.location.lower():
            score += 30
    return score

def get_matches_for_item(db: Session, item_id: int, user):
    item = db.query(Item).filter(
        Item.id == item_id,
        Item.organization_id == user.organization_id
    ).first()
    if not item:
        return []

    opposite_type = "found" if item.type == "lost" else "lost"
    candidates = db.query(Item).filter(
        Item.organization_id == user.organization_id,
        Item.type == opposite_type,
        Item.status == "open"
    ).all()

    results = []
    for candidate in candidates:
        score = score_match(item, candidate)
        if score >= 40:  # threshold
            results.append({"item": candidate, "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results