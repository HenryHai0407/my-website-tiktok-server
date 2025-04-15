from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services import product_service
from models.product_dto import ProductCreate, ProductUpdate, ProductOut
from typing import List

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductOut])
def get_all(db: Session = Depends(get_db)):
    return product_service.get_products(db)

@router.get("/{product_id}", response_model=ProductOut)
def get_one(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductOut)
def create(product: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, product)

@router.put("/{product_id}", response_model=ProductOut)
def update(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    updated = product_service.update_product(db, product_id, product)
    if updated is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db)):
    success = product_service.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"deleted": True}
