from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class ProductBase(BaseModel):
    category_id: int
    name: str
    description: Optional[str] = None
    price: Decimal
    stock: Optional[int] = 0

class ProductCreate(ProductBase):
    pass

# Explanation for pass in ProductCreate:
# These fields are exactly what you need when creating a product. 
# So instead of repeating the same attributes again in ProductCreate, we just do "pass".

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[Decimal]
    stock: Optional[int]
    category_id: Optional[int]

class ProductOut(ProductBase):
    id: int
    class Config:
        orm_mode = True
