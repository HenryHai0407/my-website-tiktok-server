from database import Base, engine  # Import from database.py
from models import User, Order     # Import models to register them with Base

# Create all tables
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")