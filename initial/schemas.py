from pydantic import BaseModel

# User Schemas
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True # Allows conversion from SQLAlchemy models

# Order Schemas
class OrderCreate(BaseModel):
    product_id: int
    quantity: int

class OrderOut(BaseModel):
    id: int
    user_id : int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True