# app/repositories/category_repo.py
from sqlalchemy import insert, select, update, delete, Table, MetaData
from sqlalchemy.engine import Result
from sqlalchemy.orm import Session
from models.category_dto import CategoryCreate, CategoryUpdate

metadata = MetaData()

def bind_tables(engine):
    metadata.reflect(bind=engine)
    global categories
    categories = metadata.tables["categories"]
    print("✅ categories columns:", categories.c.keys())

def create_category(db: Session, category: CategoryCreate):
    stmt = insert(categories).values(
        name=category.name,
        description=category.description
    )
    result = db.execute(stmt)
    db.commit()
    return get_category_by_id(db, result.lastrowid)

def get_all_categories(db: Session):
    stmt = select(categories).order_by(categories.c.id.desc())
    result: Result = db.execute(stmt)
    return result.fetchall()

def get_category_by_id(db: Session, category_id: int):
    stmt = select(categories).where(categories.c.id == category_id)
    result: Result = db.execute(stmt).first()
    return result

def update_category(db: Session, category_id: int, category: CategoryUpdate):
    stmt = (
        update(categories)
        .where(categories.c.id == category_id)
        .values({k: v for k, v in category.dict(exclude_unset=True).items()})
    )
    result = db.execute(stmt)
    db.commit()
    return get_category_by_id(db, category_id) if result.rowcount > 0 else None

def delete_category(db: Session, category_id: int):
    stmt = delete(categories).where(categories.c.id == category_id)
    result = db.execute(stmt)
    db.commit()
    return result.rowcount > 0