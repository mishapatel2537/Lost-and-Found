from fastapi import APIRouter
from app.schemas.item import LostItem, FoundItem

router = APIRouter(prefix="/items")

@router.post("/lost")
def report_lost_item(item: LostItem):
    return {"status":"received", 
            "item":item}

@router.post("/found")
def report_found_item(item: FoundItem):
    return {"status":"received",
            "item":item}