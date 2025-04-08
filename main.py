from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

DB_CONNECT_STRING = "mysql+pymysql://root:root@localhost:3306/my-website"
engine = create_engine(DB_CONNECT_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ProductModel(BaseModel):
    id: int
    title: str
    summary: str | None = None
    price: float | None = None
    quantity: int | None = None
    description: str | None = None



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@app.get("/")
async def root():
    return {"message": "Hello World"}

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