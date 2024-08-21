from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from app.models import ItemModel
from app.schemas import ItemCreate
from app.database import get_db
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/api/items",
    tags=["Items"]
)

@router.get("/")
async def get_all_items(db: Session = Depends(get_db)):
    items = db.query(ItemModel).all()
    return items


@router.post("/")
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = ItemModel(**item.model_dump())
    try:
        db.add(db_item)
    except IntegrityError:
        return None
    db.commit()
    return db_item


@router.delete("/{id}")
async def delete_item(id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemModel).filter(ItemModel.id == id).first()
    db.delete(db_item)
    db.commit()
    return db_item

@router.put("/{id}")
async def update_item(id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(ItemModel).filter(ItemModel.id == id).first()
    try:
        db_item.name = item.name
        db_item.description = item.description
    except IntegrityError:
        db.rollback()
        return None

    db.commit()
    return db_item
