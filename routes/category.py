from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database_conn import get_db
from models import Category
from schemas import CategoryCreate, CategoryResponse

Categories = APIRouter(prefix="/categories", tags=["Categories"])


@Categories.post("/", response_model=CategoryResponse)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    # Check if category already exists
    existing = db.query(Category).filter(Category.slug == payload.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category with this slug already exists")

    category = Category(**payload.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
