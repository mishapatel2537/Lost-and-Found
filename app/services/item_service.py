from sqlalchemy.orm import Session
from app.models.item import Item

def create_item(db: Session, item_data, user_id: int, status: str):
    item = Item(
        title=item_data.title,
        description=item_data.description,
        category=item_data.category,
        location=item_data.location,
        status=status,
        owner_id=user_id
    )

    db.add(item)
    db.commit()
    db.refresh()

    return item

def get_items(db: Session, skip: int=0, limit: int=10, status=None, search=None, category=None, location=None):
    query = db.query(Item)

    if status:
        query = query.filter(Item.status == status)

    if search:
        query = query.filter(Item.title.ilike(f"%{search}%"))

    if category:
        query = query.filter(Item.category.ilike(f"%{category}%"))

    if location:
        query = query.filter(Item.location.ilike(f"%{location}%"))

    return query.offset(skip).limit(limit).all()

def get_item_by_id(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()