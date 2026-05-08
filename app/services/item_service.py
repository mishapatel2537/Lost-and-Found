from sqlalchemy.orm import Session
from app.models.item import Item

VALID_TYPES = ["lost", "found"]
VALID_STATUS = ["open", "claimed", "returned"]

def create_item(db: Session, item_data, user, image_url=None):
    if item_data.type not in VALID_TYPES:
        raise Exception("Invalid item type")

    item = Item(
        name=item_data.name,
        description=item_data.description,
        category=item_data.category,
        location=item_data.location,
        type=item_data.type,
        status="open",
        owner_id=user.id,
        organization_id=user.organization_id,
        image_url=image_url
    )

    db.add(item)
    db.commit()
    db.refresh(item)  # ← fixed: was db.refresh() with no argument
    return item


def get_items(db: Session, user, skip: int = 0, limit: int = 10,
              type: str = None, search: str = None,
              category: str = None, location: str = None, status: str = None):

    query = db.query(Item).filter(
        Item.organization_id == user.organization_id
    )

    if type:
        query = query.filter(Item.type == type)
    if status:
        query = query.filter(Item.status == status)
    if search:
        query = query.filter(Item.name.ilike(f"%{search}%"))  # ← fixed: was Item.title
    if category:
        query = query.filter(Item.category.ilike(f"%{category}%"))
    if location:
        query = query.filter(Item.location.ilike(f"%{location}%"))

    return query.offset(skip).limit(limit).all()


def get_item_by_id(db: Session, user, item_id: int):
    return db.query(Item).filter(
        Item.id == item_id,
        Item.organization_id == user.organization_id
    ).first()


def update_item_status(db: Session, user, item_id: int, status: str):
    if status not in VALID_STATUS:
        raise Exception("Invalid status")

    item = db.query(Item).filter(
        Item.id == item_id,
        Item.organization_id == user.organization_id
    ).first()

    if not item:
        raise Exception("Item not found")

    if item.owner_id != user.id:
        raise Exception("Not allowed")

    item.status = status
    db.commit()
    db.refresh(item)
    return item