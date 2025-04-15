# main.py
from fastapi import FastAPI
from controllers import category_controller
from database import Base, engine
from repositories import category_repo

category_repo.bind_tables(engine)  # Bind the SQLAlchemy Core metadata

app = FastAPI(title="FastAPI Store")

app.include_router(category_controller.router)
