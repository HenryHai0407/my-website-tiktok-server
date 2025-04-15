from pydantic import BaseModel
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
# from models.category_model import CategoryModel

class ProductModel(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    summary: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    description: Optional[str] = None

    category_id: int = Field(foreign_key="categories.id")
    category: Optional["CategoryModel"] = Relationship(
        back_populates="products")


class ProductBase(BaseModel):
    name: str
    summary: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    description: Optional[str] = None
    category_id: int


class ProductDTO(ProductBase):
    id: int

    class Config:
        from_attributes = True


class ProductDTOCreate(ProductBase):
    pass


class ProductDTOUpdate(ProductBase):
    pass