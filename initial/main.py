from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, Base, engine
from models import User, Order
from initial.schemas import UserCreate, UserOut, OrderCreate, OrderOut
from initial.auth import get_password_hash, get_current_user, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

class ProductModel(BaseModel):
    id: int
    title: str
    summary: str | None = None
    price: float | None = None
    quantity: int | None = None
    description: str | None = None
    
class ProductCreateRequest(BaseModel):
    title: str
    summary: str | None = None
    price: float | None = None
    quantity: int | None = None
    description: str | None = None

class ProductUpdateRequest(BaseModel):
    title: str
    summary: str | None = None
    price: float | None = None
    quantity: int | None = None
    description: str | None = None

app = FastAPI()

PRODUCTS = [
        {
            "id": 1,
            "title": "san pham Ao khoac Han Quoc",
            "summary": "san pham tu Han Quoc 2023",
            "price": 10000,
            "quantity": 88,
            "description": "Hello Summer"
            },
        {
            "id": 2,
            "title": "san pham ao Bong Da Han Quoc",
            "summary": "san pham tu Han Quoc 2019",
            "price": 8800,
            "quantity": 88,
            "description": "Hello Summer"
            },
        ]

@app.get("/api/products")
def get_products(db: Session = Depends(get_db)):
    query = text("SELECT * FROM products")
    result = db.execute(query)
    products = [ProductModel(**dict(zip(result.keys(), row))) for row in result]
    return products

@app.get("/api/products/{id}")
def get_product_detail(id: int, db: Session = Depends(get_db)):
    query = text("SELECT * FROM products WHERE id = :id")
    result = db.execute(query, {"id": id}) # Result object
    row = result.fetchone() # Fetch the row
    if not row:
        return HTTPException(status_code=404, detail="Not Found")
    keys = result.keys() # Get column names from "result"
    return ProductModel(**dict(zip(keys, row)))

    
### 2nd solution for get_product_detail
# @app.get("/api/products/{id}")
# def get_product_detail(id: int, db: Session = Depends(get_db)):
#     query = text("SELECT * FROM products WHERE id = :id")
#     result = db.execute(query, {"id": id}).fetchone()
#     if not result:
#         raise HTTPException(status_code=404, detail="Not Found")
#     return ProductModel(**result._mapping)


### Add more features with POST, PUT, DELETE APIs

# from fastapi.security import OAuth2PasswordRequestForm
# from .auth import verify_password, create_access_token
# User Registration (POST /users)
@app.post("/users",response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username = user.username, hashed_password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# User Login (POST /login)
# from fastapi.security import OAuth2PasswordRequestForm
# from .auth import verify_password, create_access_token

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Place Order (POST /orders)
# from .models import Order
# from .schemas import OrderCreate, OrderOut
# from .auth import get_current_user

@app.post("/orders", response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_order = Order(user_id=current_user.id, product_id=order.product_id, quantity=order.quantity)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

### ---- Lesson 4
@app.post("/api/products")
def create_product(product: ProductCreateRequest, db: Session = Depends(get_db)):
    query = text("""
    INSERT INTO products (
                  title, summary, price, quantity, description
                  )
    VALUES (:title, :summary, :price, :quantity, :description)
    """)
    # db.execute(query,
    #             {
    #                 "title": product.title,
    #                 "summary": product.summary,
    #                 "price": product.price,
    #                 "quantity": product.quantity,
    #                 "description": product.description
    #             })
    db.execute(query, product.model_dump())
    db.commit()
    return {'Product title': product.title}

# PUT apis
@app.put("/api/products/{id}")
def create_product(id: int, product: ProductCreateRequest, db: Session = Depends(get_db)):
    query = text("""
    UPDATE products
                 SET
                    summary = :summary,
                    price = :price,
                    quantity = :quantity,
                    description = :description
                 WHERE
                    id = :id
    """)
    values = product.dict()
    values['id'] = id
    try:
        db.execute(query, values)
        db.commit()
        return {'message': f"Product with id {id} updated successful."}
    except SQLAlchemyError as e:
        db.rollback()
        return {'error': str(e)}
# DELETE apis
@app.delete("/api/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    query = text ("""
                DELETE FROM products
                WHERE id = :id
    """)
    try:
        db.execute(query, {"id": id})
        db.commit()
        return {'message': f"Product with id {id} being deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        return {'error': str(e)}


#### In terms of database, in general, most ecommerce website creates its database by manually setting up in 
# database with SQL query instead of using ORM models, because when the application grows,
# it is harder to manage and maintain ORM than database model.
