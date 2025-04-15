# app/controllers/category_controller.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services import category_service
from database import get_db
from models.category_dto import CategoryCreate, CategoryUpdate, CategoryResponse
from typing import List

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create_category(db, category)

@router.get("/", response_model=List[CategoryResponse])
def get_all(db: Session = Depends(get_db)):
    return category_service.get_categories(db)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_one(category_id: int, db: Session = Depends(get_db)):
    category = category_service.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=CategoryResponse)
def update(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    updated = category_service.update_category(db, category_id, category)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated

@router.delete("/{category_id}")
def delete(category_id: int, db: Session = Depends(get_db)):
    deleted = category_service.delete_category(db, category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": f"Category with ID {category_id} deleted."}
