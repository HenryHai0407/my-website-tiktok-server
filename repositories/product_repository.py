from sqlmodel import Session, text
from models.product_model import ProductModel
from typing import List


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list(self) -> List[ProductModel]:
        query = text("SELECT * FROM products")
        result = self.db.execute(query)
        return [ProductModel(**dict(row._mapping)) for row in result]

    def get_by_id(self, id: int) -> ProductModel:
        query = text("SELECT * FROM products WHERE id = :id")
        result = self.db.execute(query, {"id": id}).first()
        return ProductModel(**dict(result._mapping)) if result else None

    def create(self, model: ProductModel):
        query = text("""
            INSERT INTO products (
                name, summary, price, quantity, description, category_id
            ) VALUES (
                :name, :summary, :price, :quantity, :description, :category_id
            )
        """)
        self.db.execute(query, model.model_dump())
        self.db.commit()

        result = self.db.execute(text("SELECT LAST_INSERT_ID()")).scalar()
        return result

    def update(self, model: ProductModel):
        query = text("""
            UPDATE products
            SET name = :name,
                summary = :summary,
                price = :price,
                quantity = :quantity,
                description = :description,
                category_id = :category_id
            WHERE id = :id
        """)
        values = model.model_dump(exclude_unset=True)

        self.db.execute(query, values)
        self.db.commit()

    def delete(self, model: ProductModel) -> None:
        query = text("DELETE FROM products WHERE id = :id")
        self.db.execute(query, {"id": model.id})
        self.db.commit()
