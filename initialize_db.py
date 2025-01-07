from models.database import engine
from sqlmodel import SQLModel

# Create all tables
SQLModel.metadata.create_all(engine)

print("Database initialized successfully!")
