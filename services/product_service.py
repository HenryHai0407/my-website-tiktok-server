from sqlalchemy.orm import Session
import repositories.product_repo as product_repo
from models.product_dto import ProductCreate, ProductUpdate

def get_products(db: Session):
    return product_repo.get_all_products(db)

def get_product(db: Session, product_id: int):
    return product_repo.get_product_by_id(db, product_id)

def create_product(db: Session, product: ProductCreate):
    return product_repo.create_product(db, product)

def update_product(db: Session, product_id: int, product: ProductUpdate):
    return product_repo.update_product(db, product_id, product)

def delete_product(db: Session, product_id: int):
    return product_repo.delete_product(db, product_id)
