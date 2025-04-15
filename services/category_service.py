# app/services/category_service.py
from sqlalchemy.orm import Session
from repositories import category_repo
from models.category_dto import CategoryCreate, CategoryUpdate

def create_category(db: Session, category: CategoryCreate):
    return category_repo.create_category(db, category)

def get_categories(db: Session):
    return category_repo.get_all_categories(db)

def get_category(db: Session, category_id: int):
    return category_repo.get_category_by_id(db, category_id)

def update_category(db: Session, category_id: int, category: CategoryUpdate):
    return category_repo.update_category(db, category_id, category)

def delete_category(db: Session, category_id: int):
    return category_repo.delete_category(db, category_id)
