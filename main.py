# main.py
from fastapi import FastAPI
from controllers import category_controller, product_controller
from database import Base, engine
from repositories import category_repo, product_repo

app = FastAPI(title="FastAPI Store")

# Reflect table metadata
category_repo.bind_tables(engine)  # Bind the SQLAlchemy Core metadata
product_repo.bind_product_table(engine)

app.include_router(category_controller.router)
app.include_router(product_controller.router)
