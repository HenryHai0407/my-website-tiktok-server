from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from models.order_item_model import OrderItemModel, OrderItemDTO


class OrderModel(SQLModel, table=True):
    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_number: str
    customer_id: int
    user_id: Optional[int] = None
    status: str
    description: Optional[str] = None
    items: List["OrderItemModel"] = Relationship(back_populates="order")


class OrderBase(SQLModel):
    customer_id: int
    user_id: Optional[int] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class OrderDTO(OrderBase):
    id: int
    order_number: str
    status: Optional[str] = None
    total_price: Optional[float] = None
    items: List[OrderItemDTO]


class OrderDTOCreateItem(SQLModel):
    product_id: int
    quantity: int
    unit_price: float
    description: Optional[str] = None


class OrderDTOCreate(OrderBase):
    items: List[OrderDTOCreateItem]

class AddToCartDTO(SQLModel):
    customer_id: int
    product_id: int
    quantity: int = 1 # default quantity is 1 if not specified

class CheckoutCartDTO(SQLModel):
    customer_id: int