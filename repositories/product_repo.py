from sqlalchemy import insert, select, update, delete, Table, MetaData
from sqlalchemy.engine import Result
from sqlalchemy.orm import Session
from models.product_dto import ProductCreate, ProductUpdate

metadata = MetaData()
products = None  # Will be bound dynamically

def bind_product_table(engine):
    global products
    metadata.reflect(bind=engine)
    products = metadata.tables["products"]

def create_product(db: Session, product: ProductCreate):
    stmt = insert(products).values(**product.dict())
    result = db.execute(stmt)
    db.commit()
    return get_product_by_id(db, result.lastrowid)

def get_all_products(db: Session):
    stmt = select(products).order_by(products.c.id.desc())
    result: Result = db.execute(stmt)
    return result.fetchall()

def get_product_by_id(db: Session, product_id: int):
    stmt = select(products).where(products.c.id == product_id)
    return db.execute(stmt).first()

def update_product(db: Session, product_id: int, product: ProductUpdate):
    stmt = (
        update(products)
        .where(products.c.id == product_id)
        .values({k: v for k, v in product.dict(exclude_unset=True).items()})
    )
    result = db.execute(stmt)
    db.commit()
    return get_product_by_id(db, product_id) if result.rowcount > 0 else None

def delete_product(db: Session, product_id: int):
    stmt = delete(products).where(products.c.id == product_id)
    result = db.execute(stmt)
    db.commit()
    return result.rowcount > 0
