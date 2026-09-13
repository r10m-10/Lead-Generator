from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.base import Base

db_url = "sqlite:///../data/platform.db"

engine = create_engine(db_url)

SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()